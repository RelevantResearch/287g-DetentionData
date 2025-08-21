import os
import re
import pandas as pd


def normalize_agency_names(
    txt_path="last-participating.txt",
    directory="Hyperlink",
    output_dir="Agency_Name_Normalizer"
):
    # -------------------------
    # Load file
    # -------------------------
    with open(txt_path, "r") as f:
        txt_filename = f.read().strip()

    actual_filename = f"hyperlink_{txt_filename}"
    file_path = os.path.join(directory, actual_filename)
    print(f"\nProcessing file → {os.path.abspath(file_path)}")

    df = pd.read_excel(file_path)

    # -------------------------
    # Abbreviations & typo corrections
    # -------------------------
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

    typo_corrections = {
        "Greens Fork Police Department": "Greens Forks Police Department",
        "Quarryville Police Department": "Quarryville Borough Police Department",
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
        "Albermarle District Jail": "Albemarle District Jail",
        "Alachua Police Departent": "Alachua Police Department",
        "Boca Raton Police Department": "Boca Raton Police Services Department"
    }

    # -------------------------
    # Cleaning function
    # -------------------------
    def clean_agency_name(name):
        if pd.isna(name):
            return name

        name = name.strip()

        # Apply typo corrections
        if name in typo_corrections:
            return typo_corrections[name]

        # Remove anything after a slash
        cleaned = re.split(r'\s*/\s*', name)[0]

        # Replace abbreviations
        for pattern, repl in abbreviation_replacements:
            if repl not in cleaned:
                cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)

        return cleaned

    if 'Unnamed: 8' in df.columns:
        df = df.drop(columns=['Unnamed: 8'])

    df["Agency Validation"] = df["LAW ENFORCEMENT AGENCY"].apply(clean_agency_name)

    # -------------------------
    # Date handling & deduplication
    # -------------------------
    df["SIGNED"] = pd.to_datetime(df["SIGNED"], errors='coerce').dt.date
    df = df.sort_values(by="SIGNED", ascending=False)
    df = df.drop_duplicates(subset=["SUPPORT TYPE", "STATE", "Agency Validation"], keep="first")

    # -------------------------
    # Save output
    # -------------------------
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"TOTAL-{txt_filename}")
    df.to_excel(output_file, index=False)

    print(f"Done! Cleaned data saved to: {os.path.abspath(output_file)}")
