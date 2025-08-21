import os
import re
import pandas as pd

# Folder containing your Excel files
folder_path = "."  # change this to your folder path
output_file = "support_type_summary.xlsx"

# List of support types to count
support_types = [
    "Task Force Model",
    "Warrant Service Officer",
    "Jail Enforcement Model"
]

summary = []

# Function to extract date from filename
def extract_date(filename):
    # Match YYYYMMDD in filename
    match = re.search(r'(\d{8})', filename)
    if match:
        date_str = match.group(1)
        return f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
    # Match MMDDYYYY format like 05292025
    match2 = re.search(r'(\d{2})(\d{2})(\d{4})', filename)
    if match2:
        month, day, year = match2.groups()
        return f"{year}/{month}/{day}"
    return "unknown"

# Loop through all Excel files
for file_name in os.listdir(folder_path):
    if file_name.endswith(".xlsx"):
        file_path = os.path.join(folder_path, file_name)
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            row = {"date": extract_date(file_name)}
            total = 0
            for stype in support_types:
                if "SUPPORT TYPE" in df.columns:
                    count = df[df["SUPPORT TYPE"] == stype].shape[0]
                else:
                    count = 0
                row[stype] = count
                total += count
            row["Total"] = total
            summary.append(row)

# Convert to DataFrame and save
summary_df = pd.DataFrame(summary)
summary_df.to_excel(output_file, index=False)
print(f"Summary saved to {output_file}")
