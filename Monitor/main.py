import os
import sys
from dotenv import load_dotenv

# Add current directory to sys.path to import local modules
sys.path.append(os.path.dirname(__file__))

# Imports for Participating Agencies
from getFilename import find_latest_file
from getHyperlink import extract_hyperlinks
from combineFiles import combine_latest_files
from monitorSheets import monitor_and_download_all
from pushGithub import push_to_github

# Imports for Pending Agencies
from combinePendingAgencies import main as combine_pending_agencies
from deduplicate_pending_combined import deduplicate_pending_combined

def process_participating_agencies():
    print("\nProcessing Participating Agencies...")
    
    load_dotenv()
    base_dir = os.path.dirname(__file__)
    data_directory = os.path.join(base_dir, '..', 'participatingAgencies after feb 20')
    save_hyperlink_dir = os.path.join(base_dir, '..', 'Monitor', 'Hyperlink')
    total_agencies_dir = os.path.join(base_dir, '..', 'Total participatingAgencies')

    # Email Info (optional)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
    RECIPIENTS = os.getenv('RECIPIENTS').split(',')

    latest_filename = find_latest_file(data_directory)
    if not latest_filename:
        print(" No matching .xlsx files found in participatingAgencies after feb 20.")
        return

    latest_file_path = os.path.join(data_directory, latest_filename)
    print(f"Found latest file: {latest_filename}")

    extract_hyperlinks(latest_file_path, save_hyperlink_dir)
    combined_file_path = combine_latest_files(save_hyperlink_dir, total_agencies_dir, total_agencies_dir)

    latest_hyperlink_file = find_latest_file(save_hyperlink_dir)
    hyperlink_file_to_delete = os.path.join(save_hyperlink_dir, latest_hyperlink_file)
    if os.path.exists(hyperlink_file_to_delete):
        os.remove(hyperlink_file_to_delete)
        print(f"Removed processed file from Hyperlink folder: {hyperlink_file_to_delete}")
    else:
        print(f"File to delete not found: {hyperlink_file_to_delete}")

def process_pending_agencies():
    print("\nStep 1: Combining Pending Agencies...")
    combine_pending_agencies()

    print("\nStep 2: Deduplicating Combined Pending Agencies...")
    deduplicate_pending_combined()

    print("\nStep 3: Cleaning up duplicated file...")
    base_dir = os.path.dirname(__file__)
    total_with_dup_dir = os.path.abspath(os.path.join(base_dir, '..', 'Total pendingAgencies', 'Total_with_Duplication'))

    try:
        latest_dup_file = find_latest_file(total_with_dup_dir)
        if latest_dup_file:
            duplicated_file_path = os.path.join(total_with_dup_dir, latest_dup_file)
            if os.path.exists(duplicated_file_path):
                os.remove(duplicated_file_path)
                print(f"Removed duplicated file: {duplicated_file_path}")
            else:
                print(f"Duplicated file not found: {duplicated_file_path}")
        else:
            print("No duplicated file found to remove.")
    except Exception as e:
        print(f"Cleanup failed: {e}")

def main():
    print("Step 0: Monitoring and downloading latest Excel files...")
    url = "https://www.ice.gov/identify-and-arrest/287g"
    has_new_file = monitor_and_download_all(url)

    if has_new_file:
        process_participating_agencies()
        process_pending_agencies()
        print("\nStep 4: Pushing files to GitHub...")
        push_to_github()

        print("\nAll steps completed successfully!")
    else:
        print("No new files detected. Skipping processing steps.")


if __name__ == "__main__":
    main()
