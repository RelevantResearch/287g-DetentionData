import pandas as pd
from datetime import datetime

# Load the Excel file
df = pd.read_excel("ice_287g_snapshots.xlsx")

# Convert the 'Snapshot Date' column to datetime
df['Snapshot Date'] = pd.to_datetime(df['Snapshot Date'])

# Sort by Snapshot Date
df = df.sort_values('Snapshot Date').reset_index(drop=True)

# Create an empty list for filtered rows
filtered_rows = []

# Track the last added snapshot date
last_date = None

# Iterate through each row
for index, row in df.iterrows():
    current_date = row['Snapshot Date'].date()

    # Keep if it's the first row or 4+ days from the last added snapshot
    if last_date is None or (current_date - last_date).days >= 3:
        filtered_rows.append(row)
        last_date = current_date  # Update last saved date

# Convert filtered rows to DataFrame
filtered_df = pd.DataFrame(filtered_rows)

# Save to Excel
filtered_df.to_excel("filtered_snapshots_every_3_days.xlsx", index=False)

# Print to verify
print(filtered_df)
