import os
import pandas as pd
from pprint import pprint

# Folder path with your Excel files
folder_path = r"E:\Relevant Research\287g\After 1st jan\before"

# Output file name
output_file = os.path.join(folder_path, "combined_287g.xlsx")

# Store all dataframes
all_dataframes = []

print("Starting to process Excel files...\n")

# Loop through each file
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".xlsx"):
        full_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        
        # Read Excel file
        try:
            df = pd.read_excel(full_path)
            row_count = df.shape[0]
            print(f"  ➜ Rows extracted: {row_count}")
            all_dataframes.append(df)
        except Exception as e:
            print(f"  ⚠️ Error reading {filename}: {e}")

# Concatenate all dataframes
if all_dataframes:
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    print("\n✅ Successfully combined all files.")
    print(f"Total rows in combined dataset: {combined_df.shape[0]}")

    # Export to Excel
    combined_df.to_excel(output_file, index=False)
    print(f"\n📄 Output saved to: {output_file}")
else:
    print("\n⚠️ No Excel data was loaded.")
