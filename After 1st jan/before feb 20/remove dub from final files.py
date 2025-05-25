import pandas as pd

# Load the combined file
df = pd.read_excel('final_combined_file.xlsx')

# First, fix the 'SIGNED' column: keep only date part
df['SIGNED'] = pd.to_datetime(df['SIGNED']).dt.date

# Now remove duplicates based on LAW ENFORCEMENT AGENCY + SUPPORT TYPE + SIGNED
df_unique = df.drop_duplicates(subset=['LAW ENFORCEMENT AGENCY', 'SUPPORT TYPE', 'SIGNED'])

# Optional: Reset index
df_unique = df_unique.reset_index(drop=True)

# Save the cleaned data
df_unique.to_excel('final_combined_file_deduplicated.xlsx', index=False)

print("Removed duplicates based on LAW ENFORCEMENT AGENCY + SUPPORT TYPE + SIGNED.")
print("Saved as 'final_combined_file_deduplicated.xlsx'.")
