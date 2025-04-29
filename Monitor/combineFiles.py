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

    # Convert 'SIGNED' column to date only (no time)
    df1['SIGNED'] = pd.to_datetime(df1['SIGNED'], errors='coerce').dt.date
    df2['SIGNED'] = pd.to_datetime(df2['SIGNED'], errors='coerce').dt.date

    # Renaming columns to match for combining
    df1 = df1.rename(columns={
        'STATE': 'STATE',
        'LAW ENFORCEMENT AGENCY': 'LAW ENFORCEMENT AGENCY',
        'TYPE': 'TYPE',
        'COUNTY': 'COUNTY',
        'SUPPORT TYPE': 'SUPPORT TYPE',
        'SIGNED': 'SIGNED',
        'MOA': 'MOA',
        'EXTRACTED LINK': 'EXTRACTED LINK'
    })

    df2 = df2.rename(columns={
        'STATE': 'STATE',
        'LAW ENFORCEMENT AGENCY': 'LAW ENFORCEMENT AGENCY',
        'TYPE': 'TYPE',
        'SUPPORT TYPE': 'SUPPORT TYPE',
        'SIGNED': 'SIGNED',
        'MOA': 'MOA',
        'COUNTY': 'COUNTY',
        'EXTRACTED LINK': 'EXTRACTED LINK'
    })

    # Ensure both DataFrames have the same columns before concatenating
    df1_columns = df1.columns
    df2_columns = df2.columns

    # Align the columns by adding missing columns to either DataFrame
    for col in df1_columns:
        if col not in df2_columns:
            df2[col] = None  # Add missing columns in df2

    for col in df2_columns:
        if col not in df1_columns:
            df1[col] = None  # Add missing columns in df1

    # Reorder columns to match in both DataFrames
    df1 = df1[df2.columns]

    # Combine the DataFrames (latest hyperlink file and latest total agencies file)
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['STATE', 'LAW ENFORCEMENT AGENCY', 'SUPPORT TYPE', 'SIGNED'], keep='first')

    # Create the 'Total_with_Duplication' directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Save the combined DataFrame to the specified path
    final_output_path = os.path.join(save_dir, f"Total-{latest_file1_name}")
    combined_df.to_excel(final_output_path, index=False)

    print(f"✅ Successfully combined and saved the file: {final_output_path}")

# Add the following block to the bottom of the script:
if __name__ == "__main__":
    hyperlink_dir = 'Monitor/Hyperlink'
    total_dir = 'Total participatingAgencies'
    save_dir = 'Total participatingAgencies'

    combine_latest_files(hyperlink_dir, total_dir, save_dir)
