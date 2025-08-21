# import os
# import re
# import pandas as pd

# # Folder containing Excel files
# folder_path = "."  # change this to your folder path
# output_file = "support_summary.xlsx"

# summary = []

# # Function to extract date from filename
# def extract_date(filename):
#     # Try to find a sequence of 8 digits like 20250317
#     match = re.search(r'(\d{8})', filename)
#     if match:
#         date_str = match.group(1)
#         return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
#     else:
#         # fallback if no date found
#         return "unknown"

# # Loop through all xlsx files
# for file_name in os.listdir(folder_path):
#     if file_name.endswith(".xlsx"):
#         file_path = os.path.join(folder_path, file_name)
#         xls = pd.ExcelFile(file_path)
#         for sheet_name in xls.sheet_names:
#             df = pd.read_excel(xls, sheet_name=sheet_name)
#             if 'SUPPORT TYPE' in df.columns:
#                 total = df['SUPPORT TYPE'].dropna().shape[0]
#                 summary.append({
#                     "date": extract_date(file_name),
#                     "total_agreement": total
#                 })

# # Save summary to Excel
# summary_df = pd.DataFrame(summary)
# summary_df.to_excel(output_file, index=False)
# print(f"Summary saved to {output_file}")

import pandas as pd

# Read Excel
df = pd.read_excel('TOTAL-participatingAgencies08132025am.xlsx')
df['SIGNED'] = pd.to_datetime(df['SIGNED'])

# Keep most recent entry per STATE and SUPPORT TYPE
df_latest = df.sort_values('SIGNED', ascending=False).drop_duplicates(subset=['STATE', 'SUPPORT TYPE'])

# Get unique states from the sheet
states = df['STATE'].unique()

# Summarize agreements by state
summary = []
for state in states:
    s = df_latest[df_latest['STATE'] == state]
    summary.append({
        'State': state,
        'Warrant Service Officer': s[s['SUPPORT TYPE']=='Warrant Service Officer'].shape[0],
        'Jail Enforcement Model': s[s['SUPPORT TYPE']=='Jail Enforcement Model'].shape[0],
        'Task Force Model': s[s['SUPPORT TYPE']=='Task Force Model'].shape[0]
    })

# Save
pd.DataFrame(summary).to_excel('graph/agreements_by_state.xlsx', index=False)
print("Table saved as 'agreements_by_state.xlsx'")
