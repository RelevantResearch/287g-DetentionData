import pandas as pd
import os

# Path to your combined Excel file
root_dir = r"pendingAgencies"
combined_file = os.path.join(root_dir, "combined_result.xlsx")

# Load the combined Excel file
df = pd.read_excel(combined_file)

# Drop duplicates based on specific columns
deduped_df = df.drop_duplicates(subset=["SUPPORT TYPE", "STATE", "LAW ENFORCEMENT AGENCY"])

# Save the cleaned dataframe back to Excel
output_file = os.path.join(root_dir, "combined_result_deduped.xlsx")
deduped_df.to_excel(output_file, index=False)

print(f"✅ Duplicates removed. Clean file saved to: {output_file}")
