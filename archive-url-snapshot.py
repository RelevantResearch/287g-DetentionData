from waybackpy import WaybackMachineCDXServerAPI
from datetime import datetime
from openpyxl import Workbook

# Target URL and user agent
url = "https://www.ice.gov/identify-and-arrest/287g"
user_agent = "Mozilla/5.0"
wayback = WaybackMachineCDXServerAPI(url, user_agent)

# Create workbook and worksheet
wb = Workbook()
ws = wb.active
ws.title = "Snapshots"
ws.append(["Snapshot Date", "Archive URL"])

# Fetch all snapshot metadata
snapshots = list(wayback.snapshots())

print(f"Found {len(snapshots)} snapshots for the page...")

# Process each snapshot
for snapshot in snapshots:
    try:
        timestamp = snapshot.timestamp  # <--- FIXED: No parentheses
        date_str = datetime.strptime(timestamp, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        archive_url = snapshot.archive_url

        ws.append([date_str, archive_url])
    except Exception as e:
        print(f"Error processing snapshot: {e}")
        continue

# Save the Excel file
wb.save("ice_287g_snapshots.xlsx")
print("File saved as 'ice_287g_snapshots.xlsx'")
