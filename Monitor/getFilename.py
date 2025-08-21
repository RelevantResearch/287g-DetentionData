import os
import re
from datetime import datetime
import pandas as pd


# -------------------------
# Find latest Excel file in folder
# -------------------------
def find_latest_file(directory: str) -> str | None:
    pattern = re.compile(r'(\d{8})(am|pm)', re.IGNORECASE)
    latest_file, latest_datetime = None, None

    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            match = pattern.search(filename)
            if match:
                date_str, period = match.group(1), match.group(2).lower()
                try:
                    file_datetime = datetime.strptime(date_str, '%m%d%Y')
                    if period == 'pm':
                        file_datetime = file_datetime.replace(hour=12)
                    if not latest_datetime or file_datetime > latest_datetime:
                        latest_datetime, latest_file = file_datetime, filename
                except ValueError:
                    continue
    return latest_file


# -------------------------
# Load Excel into DataFrame
# -------------------------
def load_excel_file(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)
