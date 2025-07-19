# import openpyxl
# import os

# def extract_hyperlinks(file_path, save_dir, link_column_name='MOA', new_column_name='EXTRACTED LINK'):
#     wb = openpyxl.load_workbook(file_path)
#     ws = wb.active

#     header_row = 1

#     # Find the index of the 'MOA' column
#     moa_col_idx = None
#     for cell in ws[header_row]:
#         if cell.value and cell.value.strip().lower() == link_column_name.lower():
#             moa_col_idx = cell.column
#             break

#     if moa_col_idx is None:
#         raise ValueError(f"Column '{link_column_name}' not found.")

#     # Insert a new column just after the 'MOA' column
#     insert_col_idx = moa_col_idx + 1
#     ws.insert_cols(insert_col_idx)
#     ws.cell(row=header_row, column=insert_col_idx).value = new_column_name

#     # Process rows to extract hyperlinks
#     extracted_count = 0
#     for row in range(2, ws.max_row + 1):
#         cell = ws.cell(row=row, column=moa_col_idx)
#         if cell.hyperlink:
#             ws.cell(row=row, column=insert_col_idx).value = cell.hyperlink.target
#             extracted_count += 1
#         else:
#             ws.cell(row=row, column=insert_col_idx).value = "-"

#     os.makedirs(save_dir, exist_ok=True)
#     filename = os.path.basename(file_path)
#     new_file_path = os.path.join(save_dir, filename)
#     wb.save(new_file_path)

#     print(f"✅ Updated file saved as: {new_file_path} with {extracted_count} hyperlinks extracted.")


import openpyxl
import os

def extract_hyperlinks(file_path, save_dir):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    header_row = 1

    # Columns you want to extract from and their respective new columns
    columns_to_process = {
        "MOA": "EXTRACTED LINK",
        "ADDENDUM": "EXTRACTED_ADDENDUM"
    }

    # Find column indices
    col_indices = {}
    for cell in ws[header_row]:
        for col_name in columns_to_process:
            if cell.value and cell.value.strip().lower() == col_name.lower():
                col_indices[col_name] = cell.column

    # Check all required columns found
    for col in columns_to_process:
        if col not in col_indices:
            raise ValueError(f"Column '{col}' not found in the sheet.")

    # Sort columns in reverse to avoid shifting when inserting
    for original_col in sorted(col_indices, key=lambda c: col_indices[c], reverse=True):
        insert_col_idx = col_indices[original_col] + 1
        ws.insert_cols(insert_col_idx)
        ws.cell(row=header_row, column=insert_col_idx).value = columns_to_process[original_col]

        # Process each row for this column
        extracted_count = 0
        for row in range(2, ws.max_row + 1):
            cell = ws.cell(row=row, column=col_indices[original_col])
            if cell.hyperlink:
                ws.cell(row=row, column=insert_col_idx).value = cell.hyperlink.target
                extracted_count += 1
            else:
                ws.cell(row=row, column=insert_col_idx).value = "-"

        print(f"✅ {columns_to_process[original_col]}: {extracted_count} hyperlinks extracted.")

    # Save updated file
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.basename(file_path)
    new_file_path = os.path.join(save_dir, filename)
    wb.save(new_file_path)

    print(f"✅ Updated file saved as: {new_file_path}")
