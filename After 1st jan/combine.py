import os
import pandas as pd

# Define the root directory
root_dir = r"E:\Relevant Research\287g\After 1st jan"
output_file = os.path.join(root_dir, "combined_result.xlsx")

# Skip "before" directory
excluded_dir = os.path.join(root_dir, "before")

# List to store all dataframes
dataframes = []

# Set to collect all unique column names
all_columns = set()

# Traverse directory
for file in os.listdir(root_dir):
    full_path = os.path.join(root_dir, file)
    if os.path.isfile(full_path) and file.endswith('.xlsx') and not full_path.startswith(excluded_dir):
        try:
            df = pd.read_excel(full_path)
            row_count = len(df)
            print(f"Processed: {file} | Rows: {row_count}")
            all_columns.update(df.columns)
            dataframes.append((file, df))
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Normalize all dataframes to have same columns
normalized_dfs = []
for file, df in dataframes:
    normalized_df = df.copy()
    for col in all_columns:
        if col not in normalized_df.columns:
            normalized_df[col] = ''
    normalized_df = normalized_df[list(all_columns)]  # Ensure column order
    normalized_dfs.append(normalized_df)

# Combine all
if normalized_dfs:
    combined_df = pd.concat(normalized_dfs, ignore_index=True)
    total_rows = len(combined_df)
    print(f"\n✅ Total combined rows: {total_rows}")
    combined_df.to_excel(output_file, index=False)
    print(f"✅ Combined file saved to: {output_file}")
else:
    print("❌ No valid Excel files found.")
