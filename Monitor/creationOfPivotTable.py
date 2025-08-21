# import pandas as pd
# import os
# import traceback

# def generate_agency_summary(
#     input_folder="CleanParticipatingAgencies",
#     output_folder="../pivotParticipatingAgencies",
#     txt_filename="last-participating.txt"
# ):
#     # Read filename from last-participating.txt
#     with open(txt_filename, "r") as f:
#         txt_filename = f.read().strip()
#         print(f"Filename from txt: {txt_filename}")

#     # Construct actual Excel file path
#     input_filename = f"Total-{txt_filename}"
#     input_filepath = os.path.join(input_folder, input_filename)
#     print(f"\nProcessing file → {os.path.abspath(input_filepath)}\n")

#     # Load dataset
#     df = pd.read_excel(input_filepath)
#     print(f"Loaded {len(df)} rows")

#     # Ensure SIGNED and LAST SEEN are datetime
#     if "SIGNED" in df.columns:
#         df['SIGNED'] = pd.to_datetime(df['SIGNED'], format="%m/%d/%y", errors='coerce')
#     if "LAST SEEN" in df.columns:
#         df['LAST SEEN'] = pd.to_datetime(df['LAST SEEN'], format="%m/%d/%y", errors='coerce')

#     # Filter from 2025 onwards
#     df = df[df['SIGNED'] >= pd.Timestamp("2025-01-01")]
#     print(f"After filtering ≥ 2025-01-01 → {len(df)} rows remain")

#     # Normalize string columns
#     if "SUPPORT TYPE" in df.columns:
#         df['SUPPORT TYPE'] = df['SUPPORT TYPE'].str.strip()
#     if "Agency Validation" in df.columns:
#         df['Agency Validation'] = df['Agency Validation'].str.strip().str.upper()

#     # Define support types
#     support_types = ['Warrant Service Officer', 'Jail Enforcement Model', 'Task Force Model']
#     pivot_tables = {}

#     # Per-support pivot
#     print("Creating per-support-type pivot tables...")
#     for support_type in support_types:
#         filtered_df = df[df['SUPPORT TYPE'].str.lower() == support_type.lower()].copy()
#         if filtered_df.empty:
#             print(f"No rows found for {support_type}")
#             continue

#         filtered_df['YEAR'] = filtered_df['SIGNED'].dt.year
#         summary = filtered_df.groupby(['STATE', 'YEAR']).size().reset_index(name='Agencies Count')
#         pivot_table = summary.pivot(index='STATE', columns='YEAR', values='Agencies Count').fillna(0).astype(int)

#         pivot_table['Total'] = pivot_table.sum(axis=1)
#         total_row = pivot_table.sum(axis=0)
#         total_row.name = 'Total'
#         pivot_table = pd.concat([pivot_table, pd.DataFrame([total_row])])
#         pivot_tables[support_type] = pivot_table
#         print(f"   {support_type}: {len(filtered_df)} rows processed")

#     # Weekly summary
#     print("Creating weekly pivot table...")
#     weekly_df = df[df['SUPPORT TYPE'].isin(support_types)].copy()
#     weekly_df['WEEK'] = weekly_df['SIGNED'].dt.to_period('W').apply(lambda r: r.start_time)

#     weekly_summary = weekly_df.groupby(['SUPPORT TYPE', 'WEEK']).size().reset_index(name='Agreements Signed')
#     weekly_pivot = weekly_summary.pivot(index='WEEK', columns='SUPPORT TYPE', values='Agreements Signed').fillna(0).astype(int)

#     weekly_pivot['Total'] = weekly_pivot.sum(axis=1)
#     total_row = weekly_pivot.sum(axis=0)
#     total_row.name = 'Total'
#     weekly_pivot = pd.concat([weekly_pivot, pd.DataFrame([total_row])])
#     print(f"Weekly pivot with {len(weekly_pivot)} rows")

#     # Multiple agreements
#     agency_counts = df.groupby(['STATE', 'Agency Validation']).size().reset_index(name='Agreement Count')
#     multiple_agreements = agency_counts[agency_counts['Agreement Count'] > 1]

#     # State % agreements
#     total_agreements = len(df)
#     state_agreements = df.groupby('STATE').size().reset_index(name='Agreements Count')
#     state_agreements['Percentage'] = (state_agreements['Agreements Count'] / total_agreements) * 100

#     # STATUS
#     df.columns = [col.upper() for col in df.columns]
#     # STATUS - ensure all four categories are included
#     all_statuses = ['Renewed', 'Present', 'New', 'Absent']
#     if 'STATUS' in df.columns:
#         status_counts = df['STATUS'].value_counts()
#         status_summary = pd.DataFrame({
#             'STATUS': all_statuses,
#             'Count': [status_counts.get(s, 0) for s in all_statuses]
#         })
#     else:
#         status_summary = pd.DataFrame({
#             'STATUS': all_statuses,
#             'Count': [0, 0, 0, 0]
#         })


#     # Output file
#     output_filename = f"Pivot-{txt_filename}"
#     output_filepath = os.path.join(output_folder, output_filename)

#     # Write Excel
#     print(f"Writing results to {output_filepath} ...")
#     with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
#         workbook = writer.book
#         date_fmt = workbook.add_format({'num_format': 'm/d/yy'})

#         # Pivot tables
#         for support_type, table in pivot_tables.items():
#             table.to_excel(writer, sheet_name=support_type)

#         # Weekly pivot
#         weekly_pivot.to_excel(writer, sheet_name="Weekly_Agreements")
#         ws_weekly = writer.sheets["Weekly_Agreements"]
#         ws_weekly.set_column(0, 0, 12, date_fmt)

#         # Multiple agreements
#         multiple_agreements.to_excel(writer, sheet_name="Multiple_Agreements", index=False)

#         # State percentages
#         state_agreements.to_excel(writer, sheet_name="State_Percentages", index=False)

#         # STATUS
#         status_summary.to_excel(writer, sheet_name="STATUS", index=False)

#         # Raw Data
#         df.to_excel(writer, sheet_name="Raw_Data", index=False)
#         ws_raw = writer.sheets["Raw_Data"]
#         if "SIGNED" in df.columns:
#             col_idx = df.columns.get_loc("SIGNED")
#             ws_raw.set_column(col_idx, col_idx, 12, date_fmt)
#         if "LAST SEEN" in df.columns:
#             col_idx = df.columns.get_loc("LAST SEEN")
#             ws_raw.set_column(col_idx, col_idx, 12, date_fmt)

#     print(f"Processed data saved to: {output_filepath}\n")


import pandas as pd
import os


def generate_agency_summary(
    input_folder="CleanParticipatingAgencies",
    output_folder="../pivotParticipatingAgencies",
    txt_filename="last-participating.txt"
):
    # -------------------------
    # Input file setup
    # -------------------------
    with open(txt_filename, "r") as f:
        txt_filename = f.read().strip()
        print(f"Filename from txt: {txt_filename}")

    input_filename = f"Total-{txt_filename}"
    input_filepath = os.path.join(input_folder, input_filename)
    print(f"\nProcessing file → {os.path.abspath(input_filepath)}\n")

    df = pd.read_excel(input_filepath)
    print(f"Loaded {len(df)} rows")

    # -------------------------
    # Preprocessing
    # -------------------------
    if "SIGNED" in df.columns:
        df['SIGNED'] = pd.to_datetime(df['SIGNED'], format="%m/%d/%y", errors='coerce')
    if "LAST SEEN" in df.columns:
        df['LAST SEEN'] = pd.to_datetime(df['LAST SEEN'], format="%m/%d/%y", errors='coerce')

    df = df[df['SIGNED'] >= pd.Timestamp("2025-01-01")]
    print(f"After filtering ≥ 2025-01-01 → {len(df)} rows remain")

    if "SUPPORT TYPE" in df.columns:
        df['SUPPORT TYPE'] = df['SUPPORT TYPE'].str.strip()
    if "Agency Validation" in df.columns:
        df['Agency Validation'] = df['Agency Validation'].str.strip().str.upper()

    # -------------------------
    # Pivot tables by support type
    # -------------------------
    support_types = ['Warrant Service Officer', 'Jail Enforcement Model', 'Task Force Model']
    pivot_tables = {}

    print("Creating per-support-type pivot tables...")
    for support_type in support_types:
        filtered_df = df[df['SUPPORT TYPE'].str.lower() == support_type.lower()].copy()
        if filtered_df.empty:
            print(f"No rows found for {support_type}")
            continue

        filtered_df['YEAR'] = filtered_df['SIGNED'].dt.year
        summary = filtered_df.groupby(['STATE', 'YEAR']).size().reset_index(name='Agencies Count')
        pivot = summary.pivot(index='STATE', columns='YEAR', values='Agencies Count').fillna(0).astype(int)

        pivot['Total'] = pivot.sum(axis=1)
        total_row = pivot.sum(axis=0)
        total_row.name = 'Total'
        pivot = pd.concat([pivot, pd.DataFrame([total_row])])

        pivot_tables[support_type] = pivot
        print(f"   {support_type}: {len(filtered_df)} rows processed")

    # -------------------------
    # Weekly agreements
    # -------------------------
    print("Creating weekly pivot table...")
    weekly_df = df[df['SUPPORT TYPE'].isin(support_types)].copy()
    weekly_df['WEEK'] = weekly_df['SIGNED'].dt.to_period('W').apply(lambda r: r.start_time)

    weekly_summary = weekly_df.groupby(['SUPPORT TYPE', 'WEEK']).size().reset_index(name='Agreements Signed')
    weekly_pivot = weekly_summary.pivot(index='WEEK', columns='SUPPORT TYPE', values='Agreements Signed').fillna(0).astype(int)

    weekly_pivot['Total'] = weekly_pivot.sum(axis=1)
    total_row = weekly_pivot.sum(axis=0)
    total_row.name = 'Total'
    weekly_pivot = pd.concat([weekly_pivot, pd.DataFrame([total_row])])
    print(f"Weekly pivot with {len(weekly_pivot)} rows")

    # -------------------------
    # Other summaries
    # -------------------------
    agency_counts = df.groupby(['STATE', 'Agency Validation']).size().reset_index(name='Agreement Count')
    multiple_agreements = agency_counts[agency_counts['Agreement Count'] > 1]

    total_agreements = len(df)
    state_agreements = df.groupby('STATE').size().reset_index(name='Agreements Count')
    state_agreements['Percentage'] = (state_agreements['Agreements Count'] / total_agreements) * 100

    df.columns = [col.upper() for col in df.columns]
    all_statuses = ['Renewed', 'Present', 'New', 'Absent']
    if 'STATUS' in df.columns:
        counts = df['STATUS'].value_counts()
        status_summary = pd.DataFrame({
            'STATUS': all_statuses,
            'Count': [counts.get(s, 0) for s in all_statuses]
        })
    else:
        status_summary = pd.DataFrame({'STATUS': all_statuses, 'Count': [0, 0, 0, 0]})

    # -------------------------
    # Write output
    # -------------------------
    output_filename = f"Pivot-{txt_filename}"
    output_filepath = os.path.join(output_folder, output_filename)
    print(f"Writing results to {output_filepath} ...")

    with pd.ExcelWriter(output_filepath, engine="xlsxwriter") as writer:
        workbook = writer.book
        date_fmt = workbook.add_format({'num_format': 'm/d/yy'})

        for support_type, table in pivot_tables.items():
            table.to_excel(writer, sheet_name=support_type)

        weekly_pivot.to_excel(writer, sheet_name="Weekly_Agreements")
        ws_weekly = writer.sheets["Weekly_Agreements"]
        ws_weekly.set_column(0, 0, 12, date_fmt)

        multiple_agreements.to_excel(writer, sheet_name="Multiple_Agreements", index=False)
        state_agreements.to_excel(writer, sheet_name="State_Percentages", index=False)
        status_summary.to_excel(writer, sheet_name="STATUS", index=False)

        df.to_excel(writer, sheet_name="Raw_Data", index=False)
        ws_raw = writer.sheets["Raw_Data"]
        if "SIGNED" in df.columns:
            col_idx = df.columns.get_loc("SIGNED")
            ws_raw.set_column(col_idx, col_idx, 12, date_fmt)
        if "LAST SEEN" in df.columns:
            col_idx = df.columns.get_loc("LAST SEEN")
            ws_raw.set_column(col_idx, col_idx, 12, date_fmt)

    print(f"Processed data saved to: {output_filepath}\n")
