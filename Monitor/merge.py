import os
import re
import pandas as pd
from datetime import datetime
from getFilename import find_latest_file, load_excel_file


# -------------------------
# Extract date from filename
# -------------------------
def extract_date_from_filename(filename: str) -> str:
    match = re.search(r'(\d{2})(\d{2})(\d{4})', filename)
    if match:
        month, day, year = match.groups()
        return datetime.strptime(f"{month}{day}{year}", "%m%d%Y").strftime("%-m/%-d/%y")
    return ""


# -------------------------
# Assign status and last seen
# -------------------------
def assign_status_and_last_seen(norm_df: pd.DataFrame, prev_df: pd.DataFrame, last_seen_date: str) -> pd.DataFrame:
    key_cols_exact = ['STATE', 'SUPPORT TYPE', 'SIGNED', 'Agency Validation']
    key_cols_partial = ['STATE', 'SUPPORT TYPE', 'Agency Validation']

    # Convert SIGNED to datetime for comparison
    for df in [norm_df, prev_df]:
        if 'SIGNED' in df.columns:
            df['SIGNED'] = pd.to_datetime(df['SIGNED'], errors='coerce')

    # Initialize all rows as New
    norm_df['Status'] = 'New'
    norm_df['Last Seen'] = last_seen_date

    # 1. Present: exact match
    exact_matches = pd.merge(norm_df, prev_df, on=key_cols_exact, how='inner')
    if not exact_matches.empty:
        mask = norm_df.set_index(key_cols_exact).index.isin(exact_matches.set_index(key_cols_exact).index)
        norm_df.loc[mask, 'Status'] = 'Present'
        norm_df.loc[mask, 'Last Seen'] = last_seen_date

    # 2. Renewed: partial match but SIGNED differs
    partial_matches = pd.merge(norm_df, prev_df, on=key_cols_partial, how='inner', suffixes=('_norm', '_prev'))
    diff_signed_mask = partial_matches['SIGNED_norm'] != partial_matches['SIGNED_prev']
    renewed_keys = partial_matches.loc[diff_signed_mask, key_cols_partial]

    for _, row in renewed_keys.iterrows():
        mask = (
            (norm_df['STATE'] == row['STATE']) &
            (norm_df['SUPPORT TYPE'] == row['SUPPORT TYPE']) &
            (norm_df['Agency Validation'] == row['Agency Validation']) &
            (norm_df['Status'] != 'Present')
        )
        norm_df.loc[mask, 'Status'] = 'Renewed'
        norm_df.loc[mask, 'Last Seen'] = last_seen_date

    # 3. Absent: rows in prev_df but not in norm_df
    absent_rows = pd.merge(prev_df, norm_df, on=key_cols_exact, how='outer', indicator=True)
    absent_rows = absent_rows[absent_rows['_merge'] == 'left_only'].copy()

    if not absent_rows.empty:
        absent_rows.drop(columns=['_merge'], inplace=True, errors='ignore')
        absent_rows = prev_df.loc[
            prev_df.set_index(key_cols_exact).index.isin(absent_rows.set_index(key_cols_exact).index)
        ].copy()
        absent_rows['Status'] = 'Absent'
        absent_rows['Last Seen'] = absent_rows['SIGNED'].dt.strftime('%-m/%-d/%y')
        norm_df = pd.concat([norm_df, absent_rows], ignore_index=True)

    # Format SIGNED for output
    if 'SIGNED' in norm_df.columns:
        norm_df['SIGNED'] = pd.to_datetime(norm_df['SIGNED'], errors='coerce').dt.strftime('%-m/%-d/%y')

    # Final column order
    final_columns = [
        'STATE', 'LAW ENFORCEMENT AGENCY', 'TYPE', 'COUNTY', 'SUPPORT TYPE', 'SIGNED',
        'MOA', 'ADDENDUM', 'Extracted Link', 'Extracted Addendum',
        'Agency Validation', 'Status', 'Last Seen'
    ]
    norm_df = norm_df[final_columns]

    return norm_df


# -------------------------
# Merge normalizer with participating
# -------------------------
def merge_latest_normalizer_with_participating(normalizer_folder, participating_folder, merge_folder, last_participating_file):
    os.makedirs(merge_folder, exist_ok=True)

    latest_norm_file = find_latest_file(normalizer_folder)
    latest_part_file = find_latest_file(participating_folder)

    if not latest_norm_file or not latest_part_file:
        raise FileNotFoundError("Could not find latest files in folders")

    norm_df = load_excel_file(os.path.join(normalizer_folder, latest_norm_file))
    prev_df = load_excel_file(os.path.join(participating_folder, latest_part_file))

    # Extract last seen date from last-participating.txt
    with open(last_participating_file, 'r') as f:
        last_file = f.read().strip().splitlines()[-1]
    last_seen_date = extract_date_from_filename(last_file)

    # Assign status and last seen
    merged_df = assign_status_and_last_seen(norm_df, prev_df, last_seen_date)

    # Save merged file
    merged_filename = f"Total-{last_file}"
    merged_path = os.path.join(merge_folder, merged_filename)
    merged_df.to_excel(merged_path, index=False)

    return merged_path
