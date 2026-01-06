# import pandas as pd

# # Load merged sheet
# df = pd.read_excel("Total-participatingAgencies09102025am.xlsx")

# # Filter only rows where Status == "Present"
# df = df[df["Status"] == "Present"]

# # Convert SIGNED to datetime, assuming 2-digit years are 2000s
# df['SIGNED'] = pd.to_datetime(df['SIGNED'], format="%m/%d/%y")

# # Filter for dates on or after 2025-01-01
# df = df[df['SIGNED'] >= pd.Timestamp('2025-01-01')]

# # Count new agreements per date
# daily_counts = df.groupby('SIGNED').size().reset_index(name='new_agreements')

# # Calculate cumulative total
# daily_counts['cumulative_total'] = daily_counts['new_agreements'].cumsum()

# # Save to a new file
# output_file = "cumulative_agreements_after_2025.xlsx"
# daily_counts.to_excel(output_file, index=False)

# print(f"Cumulative file saved as {output_file}")


import pandas as pd

# Load the merged/cumulative file
df = pd.read_excel("cumulative_agreements_after_2025.xlsx")

# Ensure SIGNED is datetime
df['SIGNED'] = pd.to_datetime(df['SIGNED'], format='%Y/%m/%d')

# Create full date range from 2025-01-01 to today
full_dates = pd.date_range(start='2025-01-01', end=pd.Timestamp.today())

# Reindex to full date range
df_full = df.set_index('SIGNED').reindex(full_dates, fill_value=0).rename_axis('SIGNED').reset_index()

# Fill Cumulative Total for missing dates
df_full['cumulative_total'] = df_full['new_agreements'].cumsum()

# Format SIGNED as YYYY/MM/DD
df_full['SIGNED'] = df_full['SIGNED'].dt.strftime('%Y/%m/%d')

# Save to new file
output_file = "cumulative_agreements_daily_filled.xlsx"
df_full.to_excel(output_file, index=False)

print(f"Cumulative daily file with all dates saved as {output_file}")
