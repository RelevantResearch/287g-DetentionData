import pandas as pd

# Load your Excel file
df = pd.read_excel("Total-participatingAgencies09102025am.xlsx")

# Convert SIGNED to datetime
df['SIGNED'] = pd.to_datetime(df['SIGNED'], format="%m/%d/%y")

# Filter rows: Status == "Present" and SIGNED after 01/01/2025
filtered_df = df[(df['Status'] == 'Present') & (df['SIGNED'] >= '2025-01-01')]

# Count agreements per state
state_counts = filtered_df.groupby('STATE').size().reset_index(name='Agreement_Count')

# Save to a new Excel file
state_counts.to_excel("state_agreement_counts.xlsx", index=False)

print("State counts saved to 'state_agreement_counts.xlsx'.")