import pandas as pd
import os

def process_latest_agency_file():
    # Path to .txt and directory
    txt_path = "last-participating.txt"
    directory = "../Total participatingAgencies"

    # Read filename from last-participating.txt
    with open(txt_path, "r") as f:
        txt_filename = f.read().strip()

    # Construct real filename in the folder
    actual_filename = "Total-" + txt_filename
    file_path = os.path.join(directory, actual_filename)

    # Print the actual file being processed
    print(f"\n🛠️  Processing file → {os.path.abspath(file_path)}\n")

    # Load Excel file
    df = pd.read_excel(file_path)

    # Mappings
    type_map = {'County': 'CON', 'State Agency': 'SA', 'Municipality': 'MUN'}
    support_map = {
        'Warrant Service Officer': 'WSO',
        'Jail Enforcement Model': 'JEM',
        'Task Force Model': 'TFM'
    }

    # Function to extract initials from agency name
    def get_agency_code(name):
        excluded_words = {"of", "the", "and"}
        words = str(name).replace("'", "").replace("-", " ").split()
        valid_words = [word for word in words if word.lower() not in excluded_words]

        if not valid_words:
            return ""

        first = valid_words[0][:2].capitalize()
        rest = ''.join(word[0].upper() for word in valid_words[1:])

        return first + rest

    # Convert "Crenshaw County" → "CrenshawCon", fallback if missing
    def get_county_code(county, type_):
        if pd.notna(county) and "County" in county:
            return county.replace(" County", "") + "Con"
        elif type_ == "State Agency":
            return "SA"
        elif type_ == "Municipality":
            return "MUN"
        else:
            return "UNK"

    # Create Unique ID
    def create_unique_id(row):
        state = str(row['STATE']).strip()
        agency = str(row['LAW ENFORCEMENT AGENCY']).strip()
        type_ = str(row['TYPE']).strip()
        support = str(row['SUPPORT TYPE']).strip()
        county = str(row['COUNTY']).strip() if pd.notna(row['COUNTY']) else ''
        signed = pd.to_datetime(row['SIGNED']).strftime('%Y-%m-%d') if pd.notna(row['SIGNED']) else ''

        state_code = 'ALA' if state.upper() == 'ALABAMA' else state[:3].upper()
        agency_code = get_agency_code(agency)
        type_code = type_map.get(type_, type_[:3].upper())
        support_code = support_map.get(support, support[:3].upper())
        county_code = get_county_code(county, type_)

        return f"{state_code}_{agency_code}_{support_code}_{county_code}_{signed}"

    # Apply the function
    df['Unique identifier'] = df.apply(create_unique_id, axis=1)

    # Remove rows with undesired unique identifier
    df = df[df['Unique identifier'] != "NAN_Na_NAN_UNK_"]

    # Save result
    output_filename = f"UniqueName/TOTAL-{txt_filename}"
    df.to_excel(output_filename, index=False)

    # Confirmation message
    print(f"✅ Processed data saved to: {output_filename}\n")
