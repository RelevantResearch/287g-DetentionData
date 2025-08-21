# import os
# from datetime import datetime
# import pandas as pd


# def find_latest_file(directory: str) -> str | None:
#     import re
#     from datetime import datetime

#     pattern = re.compile(r'(\d{8})(am|pm)', re.IGNORECASE)
#     latest_file = None
#     latest_datetime = None

#     for filename in os.listdir(directory):
#         if filename.endswith('.xlsx'):
#             match = pattern.search(filename)
#             if match:
#                 date_str = match.group(1)
#                 period = match.group(2).lower()
#                 try:
#                     file_datetime = datetime.strptime(date_str, '%m%d%Y')
#                     if period == 'pm':
#                         file_datetime = file_datetime.replace(hour=12)
#                     if not latest_datetime or file_datetime > latest_datetime:
#                         latest_datetime = file_datetime
#                         latest_file = filename
#                 except ValueError:
#                     continue
#     return latest_file


# def merge_pending_agencies():
#     folder = "Normalized_Total_pendingAgencies"
#     latest_file = find_latest_file(folder)
#     if not latest_file:
#         print("No Excel file found.")
#         return

#     latest_path = os.path.join(folder, latest_file)
#     print(f"Latest file found: {latest_path}")

#     with open("last-pending.txt", "r") as f:
#         normalizer_file = f.read().strip()

#     normalizer_path = os.path.join("Agency_Pending_Normalizer", normalizer_file)
#     print(f"Using normalizer file: {normalizer_path}")

#     df_latest = pd.read_excel(latest_path, sheet_name=0)
#     df_normalizer = pd.read_excel(normalizer_path, sheet_name=0)

#     today = datetime.now().strftime('%Y/%m/%d')

#     # --- Step 1: STATUS and LAST SEEN for df_latest ---
#     status_list = []
#     last_seen_list = []

#     for _, row in df_latest.iterrows():
#         match = df_normalizer[
#             (df_normalizer['STATE'] == row['STATE']) &
#             (df_normalizer['Agency Validation'] == row['Agency Validation']) &
#             (df_normalizer['SUPPORT TYPE'] == row['SUPPORT TYPE'])
#         ]
#         if not match.empty:
#             status_list.append('present')
#             last_seen_list.append(today)
#         else:
#             status_list.append('absent')
#             # Keep old LAST SEEN if exists, else blank
#             last_seen_list.append(row['LAST SEEN'] if 'LAST SEEN' in row and pd.notna(row['LAST SEEN']) else '')

#     df_latest['STATUS'] = status_list
#     df_latest['LAST SEEN'] = last_seen_list

#     # --- Step 2: STATUS and LAST SEEN for new rows from normalizer ---
#     latest_keys = set(
#         zip(df_latest['STATE'], df_latest['Agency Validation'], df_latest['SUPPORT TYPE'])
#     )

#     new_rows = []
#     for _, row in df_normalizer.iterrows():
#         key = (row['STATE'], row['Agency Validation'], row['SUPPORT TYPE'])
#         if key not in latest_keys:
#             row['STATUS'] = 'new'
#             row['LAST SEEN'] = today
#             new_rows.append(row)

#     df_new = pd.DataFrame(new_rows)

#     # --- Step 3: Merge all ---
#     merged_df = pd.concat([df_latest, df_new], ignore_index=True)

#     # --- Step 4: Remove duplicates ---
#     merged_df = merged_df.drop_duplicates(
#         subset=['STATE', 'TYPE', 'SUPPORT TYPE', 'Agency Validation'],
#         keep='first'
#     )

#     dest_folder = "Normalized_Total_pendingAgencies"
#     os.makedirs(dest_folder, exist_ok=True)
#     output_name = "Total-" + os.path.splitext(normalizer_file)[0] + ".xlsx"
#     output_file = os.path.join(dest_folder, output_name)

#     merged_df.to_excel(output_file, index=False)
#     print(f"Merged file saved directly to: {output_file}")


import os
import pandas as pd
from datetime import datetime


# -------------------------
# Find latest Excel file in folder
# -------------------------
def find_latest_file(directory: str) -> str | None:
    import re

    pattern = re.compile(r'(\d{8})(am|pm)', re.IGNORECASE)
    latest_file, latest_datetime = None, None

    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            match = pattern.search(filename)
            if match:
                date_str, period = match.group(1), match.group(2).lower()
                try:
                    file_datetime = datetime.strptime(date_str, '%m%d%Y')
                    if period == 'pm':
                        file_datetime = file_datetime.replace(hour=12)
                    if not latest_datetime or file_datetime > latest_datetime:
                        latest_datetime, latest_file = file_datetime, filename
                except ValueError:
                    continue
    return latest_file


# -------------------------
# Merge pending agencies
# -------------------------
def merge_pending_agencies():
    folder = "Normalized_Total_pendingAgencies"
    latest_file = find_latest_file(folder)
    if not latest_file:
        print("No Excel file found.")
        return

    latest_path = os.path.join(folder, latest_file)
    print(f"Latest file found: {latest_path}")

    with open("last-pending.txt", "r") as f:
        normalizer_file = f.read().strip()

    normalizer_path = os.path.join("Agency_Pending_Normalizer", normalizer_file)
    print(f"Using normalizer file: {normalizer_path}")

    df_latest = pd.read_excel(latest_path, sheet_name=0)
    df_normalizer = pd.read_excel(normalizer_path, sheet_name=0)
    today = datetime.now().strftime('%Y/%m/%d')

    # --- Step 1: Update STATUS and LAST SEEN in df_latest
    status, last_seen = [], []
    for _, row in df_latest.iterrows():
        match = df_normalizer[
            (df_normalizer['STATE'] == row['STATE']) &
            (df_normalizer['Agency Validation'] == row['Agency Validation']) &
            (df_normalizer['SUPPORT TYPE'] == row['SUPPORT TYPE'])
        ]
        if not match.empty:
            status.append('present')
            last_seen.append(today)
        else:
            status.append('absent')
            last_seen.append(row['LAST SEEN'] if 'LAST SEEN' in row and pd.notna(row['LAST SEEN']) else '')

    df_latest['STATUS'] = status
    df_latest['LAST SEEN'] = last_seen

    # --- Step 2: Add new rows from normalizer
    latest_keys = set(zip(df_latest['STATE'], df_latest['Agency Validation'], df_latest['SUPPORT TYPE']))
    new_rows = []
    for _, row in df_normalizer.iterrows():
        key = (row['STATE'], row['Agency Validation'], row['SUPPORT TYPE'])
        if key not in latest_keys:
            row['STATUS'], row['LAST SEEN'] = 'new', today
            new_rows.append(row)

    df_new = pd.DataFrame(new_rows)

    # --- Step 3: Merge and clean
    merged_df = pd.concat([df_latest, df_new], ignore_index=True)
    merged_df = merged_df.drop_duplicates(
        subset=['STATE', 'TYPE', 'SUPPORT TYPE', 'Agency Validation'],
        keep='first'
    )

    # --- Step 4: Save result
    dest_folder = "Normalized_Total_pendingAgencies"
    os.makedirs(dest_folder, exist_ok=True)
    output_name = "Total-" + os.path.splitext(normalizer_file)[0] + ".xlsx"
    output_file = os.path.join(dest_folder, output_name)

    merged_df.to_excel(output_file, index=False)
    print(f"Merged file saved directly to: {output_file}")
