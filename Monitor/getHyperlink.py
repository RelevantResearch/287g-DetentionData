import openpyxl
import os

def extract_hyperlinks(file_path, save_dir, link_column_name='MOA', new_column_name='EXTRACTED LINK'):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    header_row = 1

    # Find the index of the 'MOA' column
    moa_col_idx = None
    for cell in ws[header_row]:
        if cell.value and cell.value.strip().lower() == link_column_name.lower():
            moa_col_idx = cell.column
            break

    if moa_col_idx is None:
        raise ValueError(f"Column '{link_column_name}' not found.")

    # Insert a new column just after the 'MOA' column
    insert_col_idx = moa_col_idx + 1
    ws.insert_cols(insert_col_idx)
    ws.cell(row=header_row, column=insert_col_idx).value = new_column_name

    # Process rows to extract hyperlinks
    extracted_count = 0
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=moa_col_idx)
        if cell.hyperlink:
            ws.cell(row=row, column=insert_col_idx).value = cell.hyperlink.target
            extracted_count += 1
        else:
            ws.cell(row=row, column=insert_col_idx).value = "-"

    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(file_path)
    new_file_path = os.path.join(save_dir, filename)
    wb.save(new_file_path)

    print(f"✅ Updated file saved as: {new_file_path} with {extracted_count} hyperlinks extracted.")
