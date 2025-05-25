import pandas as pd
import os
from getFilename import find_latest_file

def deduplicate_pending_combined():
    base_directory = os.path.dirname(__file__)
    total_pending_dir = os.path.join(base_directory, '..', 'Total pendingAgencies')

    # Get latest pending filename dynamically
    latest_pending_file = find_latest_file(os.path.join(base_directory, '..', 'pendingAgencies'))
    if not latest_pending_file:
        print("❌ No valid pending file found.")
        return

    # Extract just the timestamp part to reuse for naming
    pending_filename = os.path.basename(latest_pending_file)

    # Construct paths
    input_file_path = os.path.join(total_pending_dir, 'Total_with_Duplication', f"Total_with-dup-{pending_filename}")
    output_file_path = os.path.join(total_pending_dir, f"Total-{pending_filename}")

    # Check if input file exists
    if not os.path.exists(input_file_path):
        print(f"❌ Input file not found: {input_file_path}")
        return

    # Read and process the Excel file
    df = pd.read_excel(input_file_path)


    # Deduplicate
    df_unique = df.drop_duplicates(subset=['LAW ENFORCEMENT AGENCY', 'SUPPORT TYPE', 'STATE']).reset_index(drop=True)

    # Save output
    df_unique.to_excel(output_file_path, index=False)
    print(f"✅ Deduplicated file saved as: {output_file_path}")

if __name__ == "__main__":
    deduplicate_pending_combined()
