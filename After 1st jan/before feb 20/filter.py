import pandas as pd

# Replace with your actual file name
input_file = 'combined_287g.xlsx'
output_file = 'after_deduplicated_removal.xlsx'

# Read Excel file
df = pd.read_excel(input_file)

# Keep all columns and drop duplicates based on LAW ENFORCEMENT AGENCY and SIGNED date
deduplicated_df = df.drop_duplicates(subset=['STATE', 'LAW ENFORCEMENT AGENCY', 'SIGNED'])

# Optional: sort for easier review (by agency and date)
deduplicated_df = deduplicated_df.sort_values(by=['STATE', 'LAW ENFORCEMENT AGENCY', 'SIGNED'])

# Save to new Excel file
deduplicated_df.to_excel(output_file, index=False)

print(f"[INFO] Done. Original rows: {len(df)}, After deduplication: {len(deduplicated_df)}")
print(f"[INFO] Saved cleaned file to: {output_file}")
