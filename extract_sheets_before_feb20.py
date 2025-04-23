import os
import pandas as pd
import requests
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Create directories if they don't exist
os.makedirs('participatingAgencies', exist_ok=True)
os.makedirs('pendingAgencies', exist_ok=True)

# Read the Excel file
print("📂 Reading ice_287g_snapshots.xlsx...")
df = pd.read_excel('ice_287g_snapshots.xlsx')

# Filter URLs after February 20, 2025
cutoff_date = datetime(2025, 1, 1)
df['Date'] = pd.to_datetime(df['Date'])
filtered_df = df[df['Date'] > cutoff_date]

print(f"🔍 Found {len(filtered_df)} URLs after {cutoff_date.date()} to process")
print("="*60)

# Track downloaded files
downloaded_files = {
    'participating': 0,
    'pending': 0,
    'errors': 0
}

for index, row in filtered_df.iterrows():
    url = row['Link']
    print(f"\n🌐 Processing URL {index+1}/{len(filtered_df)}: {url}")
    print("-"*50)
    
    try:
        # Get the archived page
        print("⏳ Fetching archived page...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all Excel download links
        excel_links = soup.find_all('a', href=lambda href: href and href.endswith('.xlsx'))
        
        if not excel_links:
            print("ℹ️ No Excel download links found on this page")
            continue
            
        for link in excel_links:
            excel_url = link['href']
            filename = os.path.basename(urlparse(excel_url).path)
            link_text = link.text.strip()
            
            print(f"🔗 Found Excel link: {link_text} ({filename})")
            
            # Determine which directory to save in
            if 'participating' in filename.lower():
                save_dir = 'participatingAgencies'
                key = 'participating'
            elif 'pending' in filename.lower():
                save_dir = 'pendingAgencies'
                key = 'pending'
            else:
                print("⚠️  Skipping - Not a participating/pending agencies file")
                continue
                
            # Download the file
            try:
                print(f"⬇️  Downloading {filename}...")
                excel_response = requests.get(excel_url, timeout=15)
                excel_response.raise_for_status()
                
                save_path = f'{save_dir}/{filename}'
                with open(save_path, 'wb') as f:
                    f.write(excel_response.content)
                
                downloaded_files[key] += 1
                print(f"✅ Saved to: {save_path}")
                
            except Exception as e:
                downloaded_files['errors'] += 1
                print(f"❌ Download failed: {str(e)}")
                
    except Exception as e:
        downloaded_files['errors'] += 1
        print(f"❌ Error processing URL: {str(e)}")

print("\n" + "="*60)
print("📊 Download Summary:")
print(f"✅ Participating Agencies files: {downloaded_files['participating']}")
print(f"✅ Pending Agencies files: {downloaded_files['pending']}")
print(f"❌ Errors encountered: {downloaded_files['errors']}")

if downloaded_files['participating'] == 0 and downloaded_files['pending'] == 0:
    print("\n🚫 No xlsx files found matching criteria")
else:
    print("\n🎉 Download completed successfully!")