import os

import pandas as pd

from openpyxl import load_workbook

from getFilename import find_latest_file


# -------------------------
# Extract hyperlinks from Excel file
# -------------------------
def extract_hyperlinks(
    folder_name: str,
    filename: str | None = None,
    save_hyperlink: bool = True
) -> pd.DataFrame | None:

    base_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_directory, '..', folder_name)

    # If filename was not provided, find the latest file
    if filename is None:
        filename = find_latest_file(folder_path)

    if not filename:
        print(f"No Excel file found in folder '{folder_name}'.")
        return None

    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        print(f"Excel file not found: {file_path}")
        return None

    print(f"Processing file: {filename}")

    # -------------------------
    # Load workbook and sheet
    # -------------------------
    wb = load_workbook(
        file_path,
        data_only=True
    )

    ws = wb.active

    df = pd.DataFrame(ws.values)

    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # -------------------------
    # Locate MOA and ADDENDUM columns
    # -------------------------
    moa_idx = df.columns.get_loc("MOA")
    add_idx = df.columns.get_loc("ADDENDUM")

    extracted_moa = []
    extracted_addendum = []

    # -------------------------
    # Extract hyperlinks row by row
    # -------------------------
    for row in ws.iter_rows(min_row=2):
        cell_moa = row[moa_idx]
        cell_add = row[add_idx]

        extracted_moa.append(
            cell_moa.hyperlink.target
            if cell_moa.hyperlink
            else None
        )

        extracted_addendum.append(
            cell_add.hyperlink.target
            if cell_add.hyperlink
            else None
        )

    # -------------------------
    # Add extracted links
    # -------------------------
    df["Extracted Link"] = extracted_moa
    df["Extracted Addendum"] = extracted_addendum

    # -------------------------
    # Save results
    # -------------------------
    if save_hyperlink:

        hyperlink_directory = os.path.join(
            base_directory,
            "Hyperlink"
        )

        os.makedirs(
            hyperlink_directory,
            exist_ok=True
        )

        save_path = os.path.join(
            hyperlink_directory,
            f"hyperlink_{filename}"
        )

        df.to_excel(
            save_path,
            index=False
        )

        print(
            f"Saved extracted hyperlinks to: {save_path}"
        )

    return df