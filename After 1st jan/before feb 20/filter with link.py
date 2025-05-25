import pandas as pd

# Load the Excel file
input_file = 'combined_287g.xlsx'
output_file = 'after_deduplicated_links.xlsx'

df = pd.read_excel(input_file)

# Normalize MOA links by extracting the ICE.gov PDF URL
df['MOA_normalized'] = df['MOA'].str.extract(r'(https://www\.ice\.gov/doclib/287gMOA/[^/]+\.pdf)', expand=False)

# Drop duplicates based on STATE, AGENCY, SIGNED, and normalized MOA
deduplicated_df = df.drop_duplicates(subset=['STATE', 'LAW ENFORCEMENT AGENCY', 'SIGNED', 'MOA_normalized'])

# Drop the temporary normalized column
deduplicated_df = deduplicated_df.drop(columns=['MOA_normalized'])

# Save to a new Excel file
deduplicated_df.to_excel(output_file, index=False)

# Print summary
print(f"[INFO] Done. Original rows: {len(df)}, After deduplication: {len(deduplicated_df)}")
print(f"[INFO] Saved cleaned file to: {output_file}")
