# import os
# import re
# import pandas as pd
# from datetime import datetime
# import sys

# sys.path.append(os.path.dirname(__file__))

# from getFilename import find_latest_file


# # Correct base path (go up one level from Monitor)
# base_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# # Correct paths
# pending_dir = os.path.join(base_path, "pendingAgencies")
# total_pending_dir = os.path.join(base_path, "Total pendingAgencies")
# output_subdir = os.path.join(total_pending_dir, "Total_with_Duplication")

# # Make sure output folder exists
# os.makedirs(output_subdir, exist_ok=True)

# def load_dataframe(file_path):
#     """
#     Load an Excel file into a pandas DataFrame.
#     """
#     try:
#         return pd.read_excel(file_path)
#     except Exception as e:
#         print(f"Error loading {file_path}: {e}")
#         return None

# def main():
#     # Find latest file in pendingAgencies
#     latest_pending_filename = find_latest_file(pending_dir)
#     if not latest_pending_filename:
#         print("❌ No latest file found in pendingAgencies.")
#         return
#     pending_file_path = os.path.join(pending_dir, latest_pending_filename)
#     print(f"✅ Latest Pending Agencies File: {latest_pending_filename}")

#     # Find latest file in Total pendingAgencies
#     latest_total_filename = find_latest_file(total_pending_dir)
#     if not latest_total_filename:
#         print("❌ No latest file found in Total pendingAgencies.")
#         return
#     total_pending_path = os.path.join(total_pending_dir, latest_total_filename)
#     print(f"✅ Latest Total Pending Agencies File: {latest_total_filename}")

#     # Load both DataFrames
#     pending_df = load_dataframe(pending_file_path)
#     total_pending_df = load_dataframe(total_pending_path)

#     if pending_df is None or total_pending_df is None:
#         print("❌ Could not load one or both files.")
#         return

#     # Align columns
#     all_columns = set(pending_df.columns).union(set(total_pending_df.columns))

#     # Normalize both DataFrames
#     for col in all_columns:
#         if col not in pending_df.columns:
#             pending_df[col] = ''
#         if col not in total_pending_df.columns:
#             total_pending_df[col] = ''

#     pending_df = pending_df[list(all_columns)]
#     total_pending_df = total_pending_df[list(all_columns)]

#     # Combine them
#     final_combined_df = pd.concat([pending_df, total_pending_df], ignore_index=True)
#     total_rows = len(final_combined_df)
#     print(f"\n✅ Final total rows: {total_rows}")

#     # Build output filename
#     output_filename = f"Total_with-dup-{latest_pending_filename}"
#     output_file_path = os.path.join(output_subdir, output_filename)

#     # Save final file
#     final_combined_df.to_excel(output_file_path, index=False)
#     print(f"✅ Final combined file saved at: {output_file_path}")

# if __name__ == "__main__":
#     main()

import os
import re
import pandas as pd
from datetime import datetime
import sys

sys.path.append(os.path.dirname(__file__))
from getFilename import find_latest_file

# Set base path
base_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Directories
pending_dir = os.path.join(base_path, "pendingAgencies")
total_pending_dir = os.path.join(base_path, "Total pendingAgencies")
output_subdir = os.path.join(total_pending_dir, "Total_with_Duplication")
os.makedirs(output_subdir, exist_ok=True)

def load_dataframe(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def extract_date_from_filename(filename):
    match = re.search(r'(\d{8})', filename)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%m%d%Y").strftime("%Y/%m/%d")
    return None


def main():
    # Get latest filenames
    latest_pending_filename = find_latest_file(pending_dir)
    if not latest_pending_filename:
        print("❌ No latest file found in pendingAgencies.")
        return
    pending_file_path = os.path.join(pending_dir, latest_pending_filename)
    print(f"✅ Latest Pending File: {latest_pending_filename}")

    latest_total_filename = find_latest_file(total_pending_dir)
    if not latest_total_filename:
        print("❌ No latest file found in Total pendingAgencies.")
        return
    total_pending_path = os.path.join(total_pending_dir, latest_total_filename)
    print(f"✅ Latest Total File: {latest_total_filename}")

    # Load data
    pending_df = load_dataframe(pending_file_path)
    total_pending_df = load_dataframe(total_pending_path)
    if pending_df is None or total_pending_df is None:
        print("❌ Could not load one or both files.")
        return

    # Extract current date from filename
    current_date = extract_date_from_filename(latest_pending_filename)
    if not current_date:
        print("❌ Could not extract date from filename.")
        return

    # Add ROW_SIGNATURE for comparison
    key_cols = ["SUPPORT TYPE", "LAW ENFORCEMENT AGENCY", "STATE"]
    def get_signature(df): return df[key_cols].astype(str).agg('|'.join, axis=1)

    pending_df["ROW_SIGNATURE"] = get_signature(pending_df)
    total_pending_df["ROW_SIGNATURE"] = get_signature(total_pending_df)

    # Map of previous LAST SEENs
    prev_last_seen_map = dict(zip(total_pending_df["ROW_SIGNATURE"], total_pending_df.get("LAST SEEN", "")))

    # Assign STATUS
    def determine_status(sig):
        return "New" if sig not in total_pending_df["ROW_SIGNATURE"].values else "Present"
    pending_df["STATUS"] = pending_df["ROW_SIGNATURE"].apply(determine_status)

    # Set LAST SEEN for Present & New → today's date
    pending_df["LAST SEEN"] = current_date

    # Get Absent rows from previous file
    absent_df = total_pending_df[~total_pending_df["ROW_SIGNATURE"].isin(pending_df["ROW_SIGNATURE"])]
    absent_df["STATUS"] = "Absent"
    absent_df["LAST SEEN"] = absent_df["ROW_SIGNATURE"].map(prev_last_seen_map)

    # Combine all rows
    final_df = pd.concat([pending_df, absent_df], ignore_index=True)
    final_df.drop(columns=["ROW_SIGNATURE"], inplace=True)

    # Save result
    output_filename = f"Total_with-dup-{latest_pending_filename}"
    output_file_path = os.path.join(output_subdir, output_filename)
    final_df.to_excel(output_file_path, index=False)
    print(f"✅ Final file saved with STATUS & LAST SEEN: {output_file_path}")


if __name__ == "__main__":
    main()
