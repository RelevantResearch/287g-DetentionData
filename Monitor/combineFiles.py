import os
import pandas as pd
import re
from datetime import datetime

def find_latest_file(directory):
    pattern = re.compile(r'(\d{8})(am|pm)', re.IGNORECASE)
    latest_file = None
    latest_datetime = None

    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            match = pattern.search(filename)
            if match:
                date_str = match.group(1)
                period = match.group(2).lower()
                try:
                    file_datetime = datetime.strptime(date_str, '%m%d%Y')
                    # Adjust for am/pm: artificially add 0:00 for AM and 12:00 for PM
                    if period == 'pm':
                        file_datetime = file_datetime.replace(hour=12)
                    if not latest_datetime or file_datetime > latest_datetime:
                        latest_datetime = file_datetime
                        latest_file = filename
                except ValueError:
                    continue  # Skip invalid formats

    return latest_file

def extract_date_from_filename(filename):
    # Extract MMDDYYYY part from filename and format as YYYY/MM/DD
    match = re.search(r'(\d{8})(am|pm)', filename, re.IGNORECASE)
    if match:
        date_str = match.group(1)  # e.g., '05202025'
        try:
            dt = datetime.strptime(date_str, '%m%d%Y')
            return dt.strftime('%Y/%m/%d')  # Format as 'YYYY/MM/DD'
        except ValueError:
            pass
    return None

def remove_and_save_nan_rows(df, filename_prefix, save_dir):
    if 'Unique identifier' in df.columns:
        nan_rows = df[df['Unique identifier'] == "NAN_Na_NAN_UNK_"]
        if not nan_rows.empty:
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"{filename_prefix}_removed_nan_rows.xlsx")
            nan_rows.to_excel(save_path, index=False)
            print(f"⚠️ Removed {len(nan_rows)} rows with 'NAN_Na_NAN_UNK_' from {filename_prefix} and saved to {save_path}")
        df = df[df['Unique identifier'] != "NAN_Na_NAN_UNK_"]
    return df

def combine_latest_files(hyperlink_dir, total_dir, save_dir):
    # Fetch the latest hyperlink file
    latest_file1_name = find_latest_file(hyperlink_dir)
    if not latest_file1_name:
        print("❌ No file found in Monitor/Hyperlink folder.")
        return

    file1_path = os.path.join(hyperlink_dir, latest_file1_name)
    print(f"✅ Fetching latest hyperlink file: {latest_file1_name}")
    
    # Fetch the latest total agencies file
    latest_file2_name = find_latest_file(total_dir)
    if not latest_file2_name:
        print("❌ No file found in Total participatingAgencies folder.")
        return

    file2_path = os.path.join(total_dir, latest_file2_name)
    print(f"✅ Fetching latest total agencies file: {latest_file2_name}")

    if not os.path.exists(file1_path):
        print(f"❌ File not found: {file1_path}")
        return

    if not os.path.exists(file2_path):
        print(f"❌ File not found: {file2_path}")
        return

    # Read the latest files
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)

    # Remove rows with 'NAN_Na_NAN_UNK_' in 'Unique identifier' and save separately
    df1 = remove_and_save_nan_rows(df1, 'file1', save_dir)
    df2 = remove_and_save_nan_rows(df2, 'file2', save_dir)

    # Print the total rows in both files after removal
    print(f"File A ({latest_file1_name}) total rows after removal: {len(df1)}")
    print(f"File B ({latest_file2_name}) total rows after removal: {len(df2)}")

    # Convert 'SIGNED' column to date only (no time)
    df1['SIGNED'] = pd.to_datetime(df1['SIGNED'], errors='coerce').dt.date
    df2['SIGNED'] = pd.to_datetime(df2['SIGNED'], errors='coerce').dt.date

    # Rename columns to align (if necessary)
    for col in df1.columns:
        if col not in df2.columns:
            df2[col] = ''
    for col in df2.columns:
        if col not in df1.columns:
            df1[col] = ''

    # Reorder df1 columns to match df2
    df1 = df1[df2.columns]

    # Define key columns for comparison
    key_cols = ['STATE', 'LAW ENFORCEMENT AGENCY', 'SUPPORT TYPE', 'SIGNED']

    # Create sets of keys from both DataFrames
    df1_keys = set(df1[key_cols].apply(tuple, axis=1))
    df2_keys = set(df2[key_cols].apply(tuple, axis=1))

    # Load previous combined file to persist absent labels
    previous_combined_path = os.path.join(save_dir, f"Total-{latest_file1_name}")
    previous_absent_map = {}

    if os.path.exists(previous_combined_path):
        df_prev = pd.read_excel(previous_combined_path)
        for _, row in df_prev.iterrows():
            key = tuple(row[col] for col in key_cols)
            status = row.get('Status', '')
            if status.startswith('Absent'):
                previous_absent_map[key] = status
        print(f"Loaded previous absence labels from {previous_combined_path}")

    # Function to get status with persistence of old absent labels
    def get_status_with_persistence(row, source):
        key = tuple(row[col] for col in key_cols)
        if source == 'df1':
            if key in df2_keys:
                return 'Present'
            else:
                return 'New'
        else:  # source == 'df2'
            if key not in df1_keys:
                if key in previous_absent_map:
                    return previous_absent_map[key]
                else:
                    return f'Absent'
            else:
                return 'Present'

    # Assign status using the function
    df1['Status'] = df1.apply(lambda row: get_status_with_persistence(row, 'df1'), axis=1)
    df2['Status'] = df2.apply(lambda row: get_status_with_persistence(row, 'df2'), axis=1)

    # Combine and drop duplicates based on key columns
    # Combine and drop duplicates based on key columns
    combined_df = pd.concat([df1, df2], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=key_cols, keep='first')

    print(f"Total rows after merging: {len(combined_df)}")

    new_rows_count = (combined_df['Status'] == 'New').sum()
    print(f"New rows added during merge: {new_rows_count}")

    # Remove rows containing 'NAN_Na_NAN_UNK_'
    combined_df = combined_df[~combined_df.apply(lambda row: row.astype(str).str.contains('NAN_Na_NAN_UNK_').any(), axis=1)]

    # Extract last seen date from filename
    last_seen_date = extract_date_from_filename(latest_file1_name)
    print(f"Using last seen date: {last_seen_date}")

    # Assign LAST SEEN column based on Status
    def assign_last_seen(row):
        if row['Status'] in ['New', 'Present']:
            return last_seen_date
        else:
            # For absent or others, keep existing if present or empty
            return row.get('LAST SEEN', '')

    combined_df['LAST SEEN'] = combined_df.apply(assign_last_seen, axis=1)


    # Format LAST SEEN column to consistent string dates (or empty)
    def format_last_seen(val):
        if pd.isna(val):
            return ''
        if isinstance(val, datetime):
            return val.strftime('%Y/%m/%d')
        if isinstance(val, pd.Timestamp):
            return val.strftime('%Y/%m/%d')
        return str(val)

    combined_df['LAST SEEN'] = combined_df['LAST SEEN'].apply(format_last_seen)
    combined_df['SIGNED'] = combined_df['SIGNED'].apply(format_last_seen)

    # Final cleanup to ensure no 'NAN_Na_NAN_UNK_' rows before saving
    if 'Unique identifier' in combined_df.columns:
        combined_df = combined_df[combined_df['Unique identifier'] != "NAN_Na_NAN_UNK_"]

    os.makedirs(save_dir, exist_ok=True)
    final_output_path = os.path.join(save_dir, f"Total-{latest_file1_name}")
    combined_df.to_excel(final_output_path, index=False)

    print(f"✅ Successfully combined and saved the file: {final_output_path}")


if __name__ == "__main__":
    hyperlink_dir = 'Monitor/Hyperlink'
    total_dir = 'Total participatingAgencies'
    save_dir = 'Total participatingAgencies'

    combine_latest_files(hyperlink_dir, total_dir, save_dir)
