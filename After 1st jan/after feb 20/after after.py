import pandas as pd

# Load the Excel file
file_path = 'combine with links.xlsx'

# Read the data into a DataFrame
df = pd.read_excel(file_path)

# Remove duplicates in the 'Extracted Link' column
df['Extracted Link'] = df['Extracted Link'].apply(lambda x: list(set(x.split('\n')))[0] if isinstance(x, str) else x)

# Drop duplicates in the 'Extracted Link' column to keep only unique links
df.drop_duplicates(subset=['Extracted Link'], keep='first', inplace=True)

# Save the cleaned DataFrame to a new Excel file
output_file = 'combine_without_duplicates.xlsx'
df.to_excel(output_file, index=False)

print(f"Duplicates removed. The cleaned data is saved in '{output_file}'.")
