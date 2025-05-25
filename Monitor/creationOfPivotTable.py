import pandas as pd
import os

def generate_agency_summary(input_folder="UniqueName", output_folder="../ParticipatingAgencieswithpivot", txt_filename="last-participating.txt"):
    # Read filename from last-participating.txt
    with open(txt_filename, "r") as f:
        txt_filename = f.read().strip()

    # Construct the actual filename
    input_filename = f"TOTAL-{txt_filename}"
    input_filepath = os.path.join(input_folder, input_filename)

    # Print the actual file being processed
    print(f"\n🛠️  Processing file → {os.path.abspath(input_filepath)}\n")

    # Load dataset
    df = pd.read_excel(input_filepath)

    # Convert SIGNED column to datetime
    df['SIGNED'] = pd.to_datetime(df['SIGNED'], errors='coerce')

    df = df[df['SIGNED'] >= pd.Timestamp("2025-01-01")]

    # Strip whitespaces and normalize case
    df['SUPPORT TYPE'] = df['SUPPORT TYPE'].str.strip()
    df['LAW ENFORCEMENT AGENCY'] = df['LAW ENFORCEMENT AGENCY'].str.strip().str.upper()

    # Define the list of support types
    support_types = ['Warrant Service Officer', 'Jail Enforcement Model', 'Task Force Model']

    # Create dictionary for pivot tables
    pivot_tables = {}

    # Generate pivot table for each support type
    for support_type in support_types:
        filtered_df = df[df['SUPPORT TYPE'].str.lower() == support_type.lower()].copy()
        filtered_df['YEAR'] = filtered_df['SIGNED'].dt.year
        summary = filtered_df.groupby(['STATE', 'YEAR']).size().reset_index(name='Agencies Count')
        # pivot_table = summary.pivot(index='YEAR', columns='STATE', values='Agencies Count').fillna(0).astype(int)
        pivot_table = summary.pivot(index='STATE', columns='YEAR', values='Agencies Count').fillna(0).astype(int)

        pivot_table['Total'] = pivot_table.sum(axis=1)
        total_row = pivot_table.sum(axis=0)
        total_row.name = 'Total'
        pivot_table = pd.concat([pivot_table, pd.DataFrame([total_row])])
        pivot_tables[support_type] = pivot_table

    # Weekly summary from Jan 1, 2025 to present
    weekly_df = df[
        (df['SIGNED'] >= pd.Timestamp("2025-01-01")) & 
        (df['SUPPORT TYPE'].isin(support_types))
    ].copy()
    weekly_df['WEEK'] = weekly_df['SIGNED'].dt.to_period('W').apply(lambda r: r.start_time)

    weekly_summary = weekly_df.groupby(['SUPPORT TYPE', 'WEEK']).size().reset_index(name='Agreements Signed')
    weekly_pivot = weekly_summary.pivot(index='WEEK', columns='SUPPORT TYPE', values='Agreements Signed').fillna(0).astype(int)
    # weekly_pivot = weekly_summary.pivot(index='SUPPORT TYPE', columns='WEEK', values='Agreements Signed').fillna(0).astype(int)

    weekly_pivot['Total'] = weekly_pivot.sum(axis=1)
    total_row = weekly_pivot.sum(axis=0)
    total_row.name = 'Total'
    weekly_pivot = pd.concat([weekly_pivot, pd.DataFrame([total_row])])

    # Agencies with more than one agreement
    agency_counts = df.groupby(['STATE', 'LAW ENFORCEMENT AGENCY']).size().reset_index(name='Agreement Count')
    multiple_agreements = agency_counts[agency_counts['Agreement Count'] > 1]

    # Calculate total number of agreements
    total_agreements = len(df)

    # Calculate the number of agreements per state
    state_agreements = df.groupby('STATE').size().reset_index(name='Agreements Count')
    state_agreements['Percentage'] = (state_agreements['Agreements Count'] / total_agreements) * 100
    
    
    df.columns = [col.upper() for col in df.columns]
    # STATUS Pivot Table
    if 'STATUS' in df.columns:
        status_summary = df['STATUS'].value_counts().reset_index()
        status_summary.columns = ['STATUS', 'Count']
    else:
        status_summary = pd.DataFrame(columns=['STATUS', 'Count'])

    # Define the output filename with the prefix 'Pivot-' and the name from last-participating.txt
    output_filename = f"Pivot-{txt_filename}"
    output_filepath = os.path.join(output_folder, output_filename)

    # Write everything to Excel
    with pd.ExcelWriter(output_filepath) as writer:
        # Write the pivot tables for each support type
        for support_type, table in pivot_tables.items():
            table.to_excel(writer, sheet_name=support_type)
        
        # Write the weekly pivot table
        weekly_pivot.to_excel(writer, sheet_name="Weekly_Agreements")
        
        # Write the multiple agreements sheet
        multiple_agreements.to_excel(writer, sheet_name="Multiple_Agreements", index=False)
        
        # Write the state percentages to a new sheet
        state_agreements.to_excel(writer, sheet_name="State_Percentages", index=False)
        
        # Write the STATUS summary sheet
        status_summary.to_excel(writer, sheet_name="STATUS", index=False)

    # Confirmation message
    print(f"✅ Processed data saved to: {output_filepath}\n")
