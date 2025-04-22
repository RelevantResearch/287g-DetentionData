import os
import re
import time
import requests
import pandas as pd
import pyttsx3
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Optional: slower speech rate

# Function to speak errors
def speak_error(message):
    print(f"[Voice] {message}")
    engine.say(message)
    engine.runAndWait()

# Folder to save Excel files
folder_name = "Participating Entities before feb 20"
os.makedirs(folder_name, exist_ok=True)

# Read snapshot URLs from Excel file
df = pd.read_excel("filtered_snapshots_every_4_days.xlsx")
total_urls = len(df)

print(f"Total snapshots to process: {total_urls}")

# Trackers
success_count = 0
failures = []

# Loop through each URL
for index, row in df.iterrows():
    url = row["Archive URL"]
    current_index = index + 1

    # Extract timestamp using regex
    timestamp_match = re.search(r'/web/(\d{14})/', url)
    timestamp = timestamp_match.group(1) if timestamp_match else f"unknown_{index}"

    # Output file path
    filename = f"ParticipatingEntities-{timestamp}.xlsx"
    file_path = os.path.join(folder_name, filename)

    # Skip if file already exists
    if os.path.exists(file_path):
        print(f"\n [{current_index}/{total_urls}] File already exists for timestamp {timestamp}, skipping...")
        continue

    print(f"\n[{current_index}/{total_urls}] Processing URL: {url}")
    print(f"Snapshot timestamp: {timestamp}")

    try:
        # Retry loop for HTTP request
        retries = 1
        for attempt in range(retries + 1):
            try:
                response = requests.get(url)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as req_err:
                if attempt < retries:
                    msg = f"Request error: {req_err}. Retrying in 10 seconds..."
                    print(msg)
                    speak_error("Request error. Retrying in ten seconds.")
                    time.sleep(10)
                else:
                    raise

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table")

        if not table:
            msg = f"No table found for this snapshot. Skipping..."
            print(msg)
            speak_error("No table found. Skipping.")
            failures.append((url, "No table found"))
            continue

        print("Table found. Extracting data...")

        # Extract headers
        headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

        # Extract rows
        rows = []
        for tr in table.find("tbody").find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            link_tag = tr.find("a")
            link_url = link_tag['href'] if link_tag else ""
            if cols:
                cols[-1] = link_url
                rows.append(cols)

        # Save to Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "287(g) Agreements"
        ws.append(headers)
        for row_data in rows:
            ws.append(row_data)

        wb.save(file_path)
        print(f"File saved to: {file_path}")
        success_count += 1

    except Exception as e:
        error_msg = f"Error processing snapshot: {e}"
        print(error_msg)
        speak_error(f"Error processing snapshot number {current_index}")
        failures.append((url, str(e)))

# Final summary
print("\n" + "=" * 50)
print(f"Total snapshots processed: {total_urls}")
print(f"Total successfully saved: {success_count}")
print(f"Total failed: {len(failures)}")

if failures:
    print("\nFailed Snapshots:")
    for failed_url, reason in failures:
        print(f"- {failed_url} -> {reason}")
