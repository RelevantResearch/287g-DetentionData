import os
import re
from datetime import datetime
import pandas as pd

# Define paths to both directories
base_directory = os.path.dirname(__file__)
participating_directory = os.path.join(base_directory, '..', 'participatingAgencies after feb 20')
pending_directory = os.path.join(base_directory, '..', 'pendingAgencies')

def find_latest_file(directory):
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
                    # Adjust for am/pm: artificially add 0:00 for AM and 12:00 for PM
                    if period == 'pm':
                        file_datetime = file_datetime.replace(hour=12)
                    if not latest_datetime or file_datetime > latest_datetime:
                        latest_datetime = file_datetime
                        latest_file = filename
                except ValueError:
                    continue  # Skip invalid formats

    return latest_file


def process_excel_file(file_path):
    """
    Read and process the Excel file.
    """
    df = pd.read_excel(file_path)
    

def main():
    # Find latest file in participatingAgencies
    latest_participating = find_latest_file(participating_directory)
    if latest_participating:
        latest_participating_path = os.path.join(participating_directory, latest_participating)
        print(f"Latest file in participatingAgencies: {latest_participating}")
        process_excel_file(latest_participating_path)
    else:
        print("No matching .xlsx files with timestamp found in participatingAgencies.")

    # Find latest file in pendingAgencies
    latest_pending = find_latest_file(pending_directory)
    if latest_pending:
        latest_pending_path = os.path.join(pending_directory, latest_pending)
        print(f"Latest file in pendingAgencies: {latest_pending}")
        process_excel_file(latest_pending_path)
    else:
        print("No matching .xlsx files with timestamp found in pendingAgencies.")

if __name__ == "__main__":
    main()
