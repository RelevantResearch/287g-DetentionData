import pandas as pd
import re, os

def normalize_agency_names(txt_path="last-participating.txt", directory="UniqueName", output_dir="Agency_Name_Normalizer"):
    # Read filename from last-participating.txt
    with open(txt_path, "r") as f:
        txt_filename = f.read().strip()

    # Construct full input file path
    actual_filename = "TOTAL-" + txt_filename
    file_path = os.path.join(directory, actual_filename)

    # Confirm the file being processed
    print(f"\n🛠️  Processing file → {os.path.abspath(file_path)}\n")

    # Load Excel file
    df = pd.read_excel(file_path)

    # Define general abbreviation replacements
    abbreviation_replacements = [
        (r'\bPD\b', 'Police Department'),
        (r'[Dd]ept\.', 'Department'),
        (r'\bBOCC\b', 'Board of County Commissioners'),
    ]

    # Define specific typo corrections
    typo_corrections = {
        "Albermarle District Jail": "Albemarle District Jail"
    }

    # Cleaning function
    def clean_agency_name(name):
        if pd.isna(name):
            return name
        original = name.strip()

        # Apply typo corrections
        if original in typo_corrections:
            return typo_corrections[original]

        # Remove anything after a slash
        cleaned = re.split(r'\s*/\s*', original)[0]

        # Replace abbreviations
        for pattern, repl in abbreviation_replacements:
            cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)

        return cleaned

    # Apply the cleaning function
    # Apply the cleaning function
    df["Agency Validation"] = df["LAW ENFORCEMENT AGENCY"].apply(clean_agency_name)

    # Convert SIGNED column to datetime (if not already)
    df["SIGNED"] = pd.to_datetime(df["SIGNED"], errors='coerce')

    df["SIGNED"] = df["SIGNED"].dt.date
    
    # Sort so latest dates come first
    df = df.sort_values(by="SIGNED", ascending=False)

    # Drop duplicates based on SUPPORT TYPE, STATE, Agency Validation; keep the latest date
    df = df.drop_duplicates(subset=["SUPPORT TYPE", "STATE", "Agency Validation"], keep="first")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save to file
    # output_file = os.path.join(output_dir, f"TOTAL-{txt_filename}")
    output_file = os.path.join(output_dir, f"TOTAL-{txt_filename}")
    df.to_excel(output_file, index=False)


    print(f"✅ Done! Cleaned data saved to: {os.path.abspath(output_file)}")
