import os
import re
from datetime import datetime


def get_file_date(filename):
    """
    Supports:
      participatingAgencies-20250221214937.xlsx
      participatingAgencies09112026.xlsx
      pendingAgencies02272026am.xlsx
      pendingAgencies-20250221214937.xlsx
    """

    # New format:
    # participatingAgencies09112026.xlsx
    # pendingAgencies02272026am.xlsx
    match = re.search(r'(\d{2})(\d{2})(\d{4})(?:am|pm)?\.xlsx$', filename, re.I)

    if match:
        month, day, year = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            pass

    # Old format:
    # participatingAgencies-20250221214937.xlsx
    match = re.search(r'-(\d{4})(\d{2})(\d{2})(\d{6})\.xlsx$', filename, re.I)

    if match:
        year, month, day, _time = match.groups()
        try:
            return datetime(int(year), int(month), int(day))
        except ValueError:
            pass

    # If filename date cannot be determined, use file modification time
    return datetime.fromtimestamp(os.path.getmtime(filename))