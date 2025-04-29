import os
import requests
from bs4 import BeautifulSoup

# Force the script to work in its own directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

LAST_FILENAMES = {
    "participating": "last-participating.txt",
    "pending": "last-pending.txt"
}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TARGET_FOLDERS = {
    "participating": os.path.join(BASE_DIR, "participatingAgencies after feb 20"),
    "pending": os.path.join(BASE_DIR, "pendingAgencies")
}

def get_excel_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=lambda href: href and href.endswith(".xlsx"))

    result = {}
    for link in links:
        href = link["href"]
        full_url = href if href.startswith("http") else "https://www.ice.gov" + href
        text = link.get_text(strip=True).lower()
        if "participating" in text:
            result["participating"] = full_url
        elif "pending" in text:
            result["pending"] = full_url
    return result

def download_file(file_url, label):
    folder = TARGET_FOLDERS[label]
    os.makedirs(folder, exist_ok=True)
    file_name = file_url.split("/")[-1]
    file_path = os.path.join(folder, f"{file_name}")

    response = requests.get(file_url)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {label} file to: {file_path}")
    return file_path, file_name

def monitor_and_download_all(webpage_url):
    links = get_excel_links(webpage_url)
    downloaded_files = []
    any_new_file = False

    for label, file_url in links.items():
        latest_filename = file_url.split("/")[-1]
        last_filename_file = LAST_FILENAMES[label]

        # Read the last saved filename if it exists
        last_filename = None
        if os.path.exists(last_filename_file):
            with open(last_filename_file, "r") as f:
                last_filename = f.read().strip()

        print(f"Checking {label.upper()} file:")
        print(f"- Latest on site: {latest_filename}")
        print(f"- Last saved:    {last_filename}")

        if latest_filename != last_filename:
            print(f"New {label} file detected. Downloading...")
            try:
                with open(last_filename_file, "w") as f:
                    f.write(latest_filename)
                print(f"Updated {last_filename_file} with: {latest_filename}")
            except Exception as e:
                print(f"Error writing to {last_filename_file}: {e}")
                continue

            file_path, _ = download_file(file_url, label)
            downloaded_files.append((label, file_path))
            any_new_file = True
        else:
            print(f"No updates for {label}.\n")

    return any_new_file

# Run the script
if __name__ == "__main__":
    url = "https://www.ice.gov/identify-and-arrest/287g"
    monitor_and_download_all(url)
