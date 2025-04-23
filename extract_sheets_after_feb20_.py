import os
import pandas as pd
import requests
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Create directories if they don't exist
os.makedirs('participatingAgencies', exist_ok=True)
os.makedirs('pendingAgencies', exist_ok=True)

# Read the Excel file containing snapshot data
print("Reading ice_287g_snapshots.xlsx...")
df = pd.read_excel('ice_287g_snapshots.xlsx')

# Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Define the startup date
startup_date = datetime.strptime('2025-02-19 21:07:39', '%Y-%m-%d %H:%M:%S')

# Filter the DataFrame to only include snapshots after the startup date
df['Snapshot Date'] = pd.to_datetime(df['Snapshot Date'])
filtered_df = df[df['Snapshot Date'] > startup_date]

# Track downloaded files
downloaded_files = {
    'participating': 0,
    'pending': 0,
    'errors': 0
}

# Process each archive URL
for index, row in filtered_df.iterrows():
    url = row['Archive URL']
    snapshot_date = row['Snapshot Date']
    snapshot_timestamp = snapshot_date.strftime('%Y%m%d%H%M%S')  # Use timestamp for filename
    current_date = snapshot_date.strftime('%Y%m%d')
    print(f"\n Processing Snapshot {index+1}/{len(filtered_df)}: {url} ({snapshot_date})")
    print("-"*50)
    
    try:
        # Get the archived page
        print(" Fetching archived page...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all Excel download links
        excel_links = soup.find_all('a', href=lambda href: href and href.endswith('.xlsx'))
        
        if not excel_links:
            print("ℹ No Excel download links found on this page")
            continue
            
        for link in excel_links:
            excel_url = urljoin(url, link['href'])  # Handle relative links
            original_filename = os.path.basename(urlparse(excel_url).path)
            link_text = link.text.strip()
            
            print(f" Found Excel link: {link_text} ({original_filename})")
            
            # Determine which directory to save in and create new filename using timestamp
            if 'participating' in original_filename.lower():
                save_dir = 'participatingAgencies'
                key = 'participating'
                new_filename = f"participatingAgencies-{snapshot_timestamp}.xlsx"
            elif 'pending' in original_filename.lower():
                save_dir = 'pendingAgencies'
                key = 'pending'
                new_filename = f"pendingAgencies-{snapshot_timestamp}.xlsx"
            else:
                print("Skipping - Not a participating/pending agencies file")
                continue
                
            # Download the Excel file
            try:
                print(f"Downloading {original_filename}...")
                excel_response = requests.get(excel_url, timeout=15)
                excel_response.raise_for_status()
                
                save_path = f'{save_dir}/{new_filename}'
                with open(save_path, 'wb') as f:
                    f.write(excel_response.content)
                
                downloaded_files[key] += 1
                print(f"Saved as: {save_path}")
                
            except Exception as e:
                downloaded_files['errors'] += 1
                print(f"Download failed: {str(e)}")
                
    except Exception as e:
        downloaded_files['errors'] += 1
        print(f"Error processing URL: {str(e)}")

# Summary of downloads
print("\n" + "="*60)
print("Download Summary:")
print(f"Participating Agencies files: {downloaded_files['participating']}")
print(f"Pending Agencies files: {downloaded_files['pending']}")
print(f"Errors encountered: {downloaded_files['errors']}")

if downloaded_files['participating'] == 0 and downloaded_files['pending'] == 0:
    print("\n No xlsx files found matching criteria")
else:
    print("\n Download completed successfully!")
