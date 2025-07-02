import os
import pandas as pd

def get_filename_from_txt(txt_path):
    with open(txt_path, 'r') as f:
        return f.read().strip()

def add_total_row(df, label="Total"):
    numeric_cols = df.select_dtypes(include="number").columns
    total_row = df[numeric_cols].sum()
    total_row = pd.DataFrame([total_row])
    total_row.insert(0, df.columns[0], label)
    return pd.concat([df, total_row], ignore_index=True)

def generate_pivot_report(filepath, output_dir):
    base_dir = os.getcwd()
    parent_dir = os.path.dirname(base_dir)
    df = pd.read_excel(filepath)
    filename = os.path.basename(filepath)
    print(f"📁 Processing file: {filename}")

    # Pivot 1: Count of STATUS by STATE
    status_pivot = pd.pivot_table(df, index='STATE', columns='STATUS', aggfunc='size', fill_value=0).reset_index()
    status_pivot = add_total_row(status_pivot)

    # Pivot 2: Number of agreements per STATE
    agreements_per_state = df.groupby("STATE").size().reset_index(name="Agreements")
    agreements_per_state = add_total_row(agreements_per_state)

    # Pivot 3: Agencies with more than one agreement
    multiple_agreements = df.groupby("LAW ENFORCEMENT AGENCY").size().reset_index(name="Agreement Count")
    multiple_agreements = multiple_agreements[multiple_agreements["Agreement Count"] > 1]
    multiple_agreements = add_total_row(multiple_agreements)

    # Pivot 4: Count by SUPPORT TYPE
    support_type_pivot = df.groupby("SUPPORT TYPE").size().reset_index(name="Count")
    support_type_pivot = add_total_row(support_type_pivot)

    # Pivot 5: Agreement percentage by STATE (no total row)
    total_agreements = df.groupby("STATE").size()
    signed_agreements = df[df["STATUS"] != "Absent"].groupby("STATE").size()
    agreement_percentage = pd.DataFrame({
        "Total": total_agreements,
        "Signed": signed_agreements
    }).fillna(0)
    agreement_percentage["Signed %"] = (agreement_percentage["Signed"] / agreement_percentage["Total"]) * 100
    agreement_percentage = agreement_percentage.reset_index()

    # Ensure output directory exists
    pivot_dir = os.path.join(parent_dir, 'Pivot PendingAgencies')
    os.makedirs(pivot_dir, exist_ok=True)

    # Output filename
    output_filename = f"pivot-{filename.replace('Total-', '')}"
    pivot_output_path = os.path.join(pivot_dir, output_filename)

    # Write to Excel
    with pd.ExcelWriter(pivot_output_path, engine='openpyxl') as writer:
        status_pivot.to_excel(writer, sheet_name="Status by State", index=False)
        agreements_per_state.to_excel(writer, sheet_name="Agreements per State", index=False)
        multiple_agreements.to_excel(writer, sheet_name="Multiple Agreements", index=False)
        support_type_pivot.to_excel(writer, sheet_name="By Support Type", index=False)
        agreement_percentage.to_excel(writer, sheet_name="Agreement % by State", index=False)

    print(f"Pivot report saved to: {pivot_output_path}")

def run_pending_agencies_pivot_report():
    base_dir = os.getcwd()
    parent_dir = os.path.dirname(base_dir)  # go one level up from Monitor folder
    txt_file = os.path.join(base_dir, 'last-pending.txt')
    total_pending_dir = os.path.join(parent_dir, 'Total pendingAgencies')

    print(f"Using base directory (Monitor folder): {base_dir}")
    print(f"Parent directory (base data folder): {parent_dir}")
    print(f"Looking for last-pending.txt at: {txt_file}")

    if not os.path.exists(txt_file):
        print("'last-pending.txt' not found.")
        return

    pending_name = get_filename_from_txt(txt_file)
    print(f"Filename read from txt file: '{pending_name}'")

    total_file_name = f"Total-{pending_name}"
    file_path = os.path.join(total_pending_dir, total_file_name)

    full_path = os.path.abspath(file_path)
    print(f"Looking for file at: {full_path}")

    if not os.path.exists(file_path):
        print(f"File not found: {total_file_name} in '{total_pending_dir}'")
        return

    generate_pivot_report(file_path, base_dir)
