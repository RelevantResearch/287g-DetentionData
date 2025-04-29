import pandas as pd
import os

# Use relative paths
file1 = 'after_deduplicated_removal.xlsx'
file2 = 'combine_without_duplicates.xlsx'

# Read both Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Make columns match: Rename columns in df1 to match df2 style if needed
df1 = df1.rename(columns={
    'SUPPORT TYPE': 'SUPPORT TYPE',
    'SIGNED': 'SIGNED',
    'MOA': 'MOA',
    'STATE': 'STATE',
    'LAW ENFORCEMENT AGENCY': 'LAW ENFORCEMENT AGENCY'
})

# If needed, add missing columns to df1
for col in df2.columns:
    if col not in df1.columns:
        df1[col] = ''

# Same for df2
for col in df1.columns:
    if col not in df2.columns:
        df2[col] = ''

# Reorder columns to match
df1 = df1[df2.columns]

# Merge them
combined_df = pd.concat([df1, df2], ignore_index=True)

# Optional: Drop exact duplicates (if any)
combined_df = combined_df.drop_duplicates()

# Save to new file
combined_df.to_excel('final_combined_file.xlsx', index=False)

print("Successfully combined into 'final_combined_file.xlsx'")
