import os
import re
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Original Wayback Machine URL
url = "https://web.archive.org/web/20210113002027/https://www.ice.gov/identify-and-arrest/287g"

# Extract timestamp using regex (equivalent to `cut -d '/' -f5`)
timestamp_match = re.search(r'/web/(\d{14})/', url)
timestamp = timestamp_match.group(1) if timestamp_match else "unknown"

# Folder path
folder_name = "Participating Entities before feb 20"
os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist

# Final filename with folder
filename = f"ParticipatingEntities-{timestamp}.xlsx"
file_path = os.path.join(folder_name, filename)

# Request page
response = requests.get(url)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="table")

# Extract headers
headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

# Extract data rows
rows = []
for tr in table.find("tbody").find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    link_tag = tr.find("a")
    link_url = link_tag['href'] if link_tag else ""
    cols[-1] = link_url
    rows.append(cols)

# Write to Excel
wb = Workbook()
ws = wb.active
ws.title = "287(g) Agreements"
ws.append(headers)

for row in rows:
    ws.append(row)

wb.save(file_path)
print(f"✅ File saved at: {file_path}")
