import pandas as pd

def assign_status(normalizer_df: pd.DataFrame, participating_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign Status column based on comparison between normalized sheet and previous participating sheet.

    Status rules:
    - Present: all 4 columns match exactly
    - Renewed: first 3 columns match but SIGNED differs
    - New: in normalizer_df but not in participating_df
    - Absent: in participating_df but not in normalizer_df
    """

    # -------------------------
    # Ensure SIGNED is datetime
    # -------------------------
    for df in [normalizer_df, participating_df]:
        if 'SIGNED' in df.columns:
            df['SIGNED'] = pd.to_datetime(df['SIGNED'], errors='coerce')

    exact_cols = ['STATE', 'SUPPORT TYPE', 'SIGNED', 'Agency Validation']
    partial_cols = ['STATE', 'SUPPORT TYPE', 'Agency Validation']

    # -------------------------
    # Start with all rows as 'New'
    # -------------------------
    normalizer_df['Status'] = 'New'

    # -------------------------
    # Present: exact matches
    # -------------------------
    exact_matches = pd.merge(normalizer_df, participating_df, on=exact_cols, how='inner')
    if not exact_matches.empty:
        mask = normalizer_df.set_index(exact_cols).index.isin(exact_matches.set_index(exact_cols).index)
        normalizer_df.loc[mask, 'Status'] = 'Present'

    # -------------------------
    # Renewed: partial match but SIGNED differs
    # -------------------------
    partial_matches = pd.merge(
        normalizer_df, participating_df, on=partial_cols, how='inner', suffixes=('_norm', '_part')
    )
    diff_signed_mask = partial_matches['SIGNED_norm'] != partial_matches['SIGNED_part']
    renewed_keys = partial_matches.loc[diff_signed_mask, partial_cols]

    for _, row in renewed_keys.iterrows():
        mask = (
            (normalizer_df['STATE'] == row['STATE']) &
            (normalizer_df['SUPPORT TYPE'] == row['SUPPORT TYPE']) &
            (normalizer_df['Agency Validation'] == row['Agency Validation']) &
            (normalizer_df['Status'] != 'Present')
        )
        normalizer_df.loc[mask, 'Status'] = 'Renewed'

    # -------------------------
    # Absent: in participating_df but not in normalizer_df
    # -------------------------
    absent_rows = pd.merge(participating_df, normalizer_df, on=exact_cols, how='outer', indicator=True)
    absent_rows = absent_rows[absent_rows['_merge'] == 'left_only']
    if not absent_rows.empty:
        absent_rows = absent_rows[participating_df.columns].copy()
        absent_rows['Status'] = 'Absent'
        normalizer_df = pd.concat([normalizer_df, absent_rows], ignore_index=True)

    # -------------------------
    # Format SIGNED as M/D/YY
    # -------------------------
    if 'SIGNED' in normalizer_df.columns:
        normalizer_df['SIGNED'] = normalizer_df['SIGNED'].dt.strftime('%-m/%-d/%y')

    return normalizer_df
