import pandas as pd

# Read the original Excel file
df = pd.read_excel("../../Monitor/Agency_Name_Normalizer/TOTAL-participatingAgencies08122025pm.xlsx", sheet_name="Sheet1")


# Select only the desired columns
columns_to_keep = [
    "STATE", "TYPE", "SUPPORT TYPE", "SIGNED", 
    "COUNTY", "EXTRACTED LINK", "LAST SEEN", 
    "Status", "Agency Validation"
]
new_df = df[columns_to_keep]

# Save to a new sheet
new_df.to_excel("extracted_sheet.xlsx", index=False)

