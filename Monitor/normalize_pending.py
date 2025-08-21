
# normalize_agency_names_pending.py
import os
import re
from datetime import datetime
import pandas as pd
from getFilename import find_latest_file  # import the function


def find_latest_file(directory: str) -> str | None:
    """
    Scan a directory for Excel files with MMDDYYYYam/pm pattern
    and return the latest filename.
    """
    pattern = re.compile(r'(\d{8})(am|pm)', re.IGNORECASE)
    latest_file = None
    latest_datetime = None

    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            match = pattern.search(filename)
            if match:
                date_str = match.group(1)
                period = match.group(2).lower()
                try:
                    file_datetime = datetime.strptime(date_str, '%m%d%Y')
                    # Adjust for PM
                    if period == 'pm':
                        file_datetime = file_datetime.replace(hour=12)
                    if not latest_datetime or file_datetime > latest_datetime:
                        latest_datetime = file_datetime
                        latest_file = filename
                except ValueError:
                    continue

    return latest_file

def normalize_agency_names_pending(
    pending_dir="Total-pendingAgencies",
    output_dir="Agency_Name_pendingAgencies"
):
    # Resolve relative paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pending_dir = os.path.join(base_dir, pending_dir)
    output_dir = os.path.join(base_dir, output_dir)

    # Find latest pending file
    latest_file = find_latest_file(pending_dir)
    if not latest_file:
        print("No pending files found.")
        return

    file_path = os.path.join(pending_dir, latest_file)
    print(f"\nProcessing latest file → {os.path.abspath(file_path)}\n")

    # Load Excel
    df = pd.read_excel(file_path)

    # Abbreviations and typos (can extend as needed)
    abbreviation_replacements = [
        (r'\bPD\b', 'Police Department'),
        (r'\bFt\.(?=\s)', 'Fort'),
        (r'[Dd]ept\.', 'Department'),
        (r'\bBOCC\b', 'Board of County Commissioners'),
        (r'\bAggricultural\b', 'Agricultural'),
        (r'\bPymathuning\b', 'Pymatuning'),
        (r'\bSt Johns County\b', 'St. Johns County'),
        (r'\bGreens Fork Police Department\b', 'Greens Forks Police Department'),
        (r'\bQuarryville Police Department\b', 'Quarryville Borough Police Department'),
        (r"\bGreene Township Constables's Office\b", "Greene Township Constable's Office"),
        (r'\bCounty of Franklin\b', 'County of Franklin / Franklin County Jail '),
        (r'\bLouisiana State Patrol\b', 'Louisiana State Police Department'),
        (r'\bOffice of the Attorney General\b', 'Texas Office of the Attorney General'),
        (r'\bWyoming State Highway Patrol \b', 'Wyoming Highway State Patrol '),
        (r"\bCoolspring Township Constbales Office\b", "Coolspring Township Constable's Office"),
        (r"\bLexington County Sheriff's Office\b", "Lexington County Sheriff's Department"),
        (r'\bMiami Dade Corrections and Rehabilitation\b', 'Miami-Dade Corrections and Rehabilitation'),
        (r'\bMiami Dade\b', 'Miami-Dade'),
        (r'\bLake Clark Shores Police Department\b', 'Lake Clarke Shores Police Department'),
        (r'\bFlorida Department of Financial Services , Criminal Investigation Division,\b', 'Florida Department of Financial Services, Criminal Investigation Division'),
        (r'\bOkaloosa County Board of County Commissioners\b', 'Okaloosa County Board of County Commissioners/ Department of Corrections'),
        (r'\bPasco County Board of County Commissioners/ Pasco County Corrections \b', 'Pasco County Board of County Commissioners/ Pasco County Corrections '),
        (r'\bFlorida Department of Financial Services\b', 'Florida Department of Financial Services, Criminal Investigation Division'),
        (r'\bFlorida Fish and Wildlife Conservation Commission\b', 'Florida Fish & Wildlife Conservation Commission'),
        (r'\bGulf County Board of County Commissioners\b', 'Gulf County Board of County Commissioners /Detention Facility'),
        (r'\bEscambia County Board of County Commissioners\b', 'Escambia County Board of County Commissioners/ Department of Corrections'),
        (r'\bFlorida Department of Environmental Protection\b', 'Florida Department of Environmental Protection, Division of Law Enforcement'),
    ]

    # Define specific typo corrections
    typo_corrections = {
        "Greens Fork Police Department": "Greens Forks Police Department",
        "Atlantis Police Department": "Atlantic Beach Police Department",
        "Christian County Sherrif's Office ": "Christian County Sherrif's Office",
        "Somerset County District Attorney'S Office": "Somerset County District Attorney's Office",
        "Quarryville Police Department": "Quarryville Borough Police Department",
        "Cartert County Sheriff's Office": "Carteret County Sheriff's Office",
        "Greene Township Constables's Office": "Greene Township Constable's Office",
        "County of Franklin": "County of Franklin / Franklin County Jail",
        "Louisiana State Patrol": "Louisiana State Police Department",
        "Office of the Attorney General": "Texas Office of the Attorney General",
        "Wyoming State Highway Patrol": "Wyoming Highway State Patrol",
        "Coolspring Township Constbales Office": "Coolspring Township Constable's Office",
        "Lexington County Sheriff's Office": "Lexington County Sheriff's Department",
        "Miami Dade Corrections and Rehabilitation": "Miami-Dade Corrections and Rehabilitation",
        "Miami Dade": "Miami-Dade",
        "Lake Clark Shores Police Department": "Lake Clarke Shores Police Department",
        "Florida Department of Financial Services , Criminal Investigation Division,": "Florida Department of Financial Services, Criminal Investigation Division",
        "Okaloosa County Board of County Commissioners": "Okaloosa County Board of County Commissioners/ Department of Corrections",
        "Pasco County Board of County Commissioners/ Pasco County Corrections": "Pasco County Board of County Commissioners/ Pasco County Corrections",
        "Florida Department of Financial Services": "Florida Department of Financial Services, Criminal Investigation Division",
        "Florida Fish and Wildlife Conservation Commission": "Florida Fish & Wildlife Conservation Commission",
        "Gulf County Board of County Commissioners": "Gulf County Board of County Commissioners /Detention Facility",
        "Escambia County Board of County Commissioners": "Escambia County Board of County Commissioners/ Department of Corrections",
        "Florida Department of Environmental Protection": "Florida Department of Environmental Protection, Division of Law Enforcement",
        
        # Keep extra known typos too
        "Albermarle District Jail": "Albemarle District Jail",
        "Alachua Police Departent": "Alachua Police Department",
        "Boca Raton Police Department": "Boca Raton Police Services Department"
    }

    # Cleaning function
    def clean_agency_name(name):
        if pd.isna(name):
            return name
        original = name.strip()
        if original in typo_corrections:
            return typo_corrections[original]
        cleaned = re.split(r'\s*/\s*', original)[0]
        for pattern, repl in abbreviation_replacements:
            if repl not in cleaned:
                cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)
        return cleaned

    if 'Unnamed: 8' in df.columns:
        df = df.drop(columns=['Unnamed: 8'])

    df["Agency Validation"] = df["LAW ENFORCEMENT AGENCY"].apply(clean_agency_name)
    df = df.drop_duplicates(subset=["SUPPORT TYPE", "STATE", "Agency Validation"], keep="first")

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{latest_file}")
    df.to_excel(output_file, index=False)
    print(f"Done! Cleaned data saved to: {os.path.abspath(output_file)}")
