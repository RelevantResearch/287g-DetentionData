import os
import sys
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("log.txt", mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add current directory to sys.path to import local modules
sys.path.append(os.path.dirname(__file__))

# Imports for Participating Agencies
from getFilename import find_latest_file
from getHyperlink import extract_hyperlinks
from combineFiles import combine_latest_files
from monitorSheets import monitor_and_download_all
from pushGithub import push_to_github
from send_email import send_email

# Imports for Pending Agencies
from combinePendingAgencies import main as combine_pending_agencies
from deduplicate_pending_combined import deduplicate_pending_combined


def process_participating_agencies():
    logging.info("Processing Participating Agencies...")

    load_dotenv()
    base_dir = os.path.dirname(__file__)
    data_directory = os.path.join(base_dir, '..', 'participatingAgencies after feb 20')
    save_hyperlink_dir = os.path.join(base_dir, '..', 'Monitor', 'Hyperlink')
    total_agencies_dir = os.path.join(base_dir, '..', 'Total participatingAgencies')

    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
    RECIPIENTS = os.getenv('RECIPIENTS').split(',')

    latest_filename = find_latest_file(data_directory)
    if not latest_filename:
        logging.warning("No matching .xlsx files found in participatingAgencies after feb 20.")
        return

    latest_file_path = os.path.join(data_directory, latest_filename)
    logging.info(f"Found latest file: {latest_filename}")

    extract_hyperlinks(latest_file_path, save_hyperlink_dir)
    combined_file_path = combine_latest_files(save_hyperlink_dir, total_agencies_dir, total_agencies_dir)

    latest_hyperlink_file = find_latest_file(save_hyperlink_dir)
    hyperlink_file_to_delete = os.path.join(save_hyperlink_dir, latest_hyperlink_file)
    if os.path.exists(hyperlink_file_to_delete):
        os.remove(hyperlink_file_to_delete)
        logging.info(f"Removed processed file from Hyperlink folder: {hyperlink_file_to_delete}")
    else:
        logging.warning(f"File to delete not found: {hyperlink_file_to_delete}")


def process_pending_agencies():
    logging.info("Step 1: Combining Pending Agencies...")
    combine_pending_agencies()

    logging.info("Step 2: Deduplicating Combined Pending Agencies...")
    deduplicate_pending_combined()

    logging.info("Step 3: Cleaning up duplicated file...")
    base_dir = os.path.dirname(__file__)
    total_with_dup_dir = os.path.abspath(os.path.join(base_dir, '..', 'Total pendingAgencies', 'Total_with_Duplication'))

    try:
        latest_dup_file = find_latest_file(total_with_dup_dir)
        if latest_dup_file:
            duplicated_file_path = os.path.join(total_with_dup_dir, latest_dup_file)
            if os.path.exists(duplicated_file_path):
                os.remove(duplicated_file_path)
                logging.info(f"Removed duplicated file: {duplicated_file_path}")
            else:
                logging.warning(f"Duplicated file not found: {duplicated_file_path}")
        else:
            logging.warning("No duplicated file found to remove.")
    except Exception as e:
        logging.error(f"Cleanup failed: {e}")


def broadcast_email(base_dir, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, RECIPIENTS):
    participating_path = None
    pending_path = None

    latest_participating_file = find_latest_file(os.path.join(base_dir, '..', 'Total participatingAgencies'))
    if latest_participating_file:
        participating_path = os.path.join(base_dir, '..', 'Total participatingAgencies', latest_participating_file)

    latest_pending_file = find_latest_file(os.path.join(base_dir, '..', 'Total pendingAgencies'))
    if latest_pending_file:
        pending_path = os.path.join(base_dir, '..', 'Total pendingAgencies', latest_pending_file)

    if participating_path or pending_path:
        attachments = []
        if participating_path:
            attachments.append(participating_path)
        if pending_path:
            attachments.append(pending_path)

        logging.info("Sending email with attachments...")
        send_email(
            file_path=None,
            file_url=None,
            api_key=SENDGRID_API_KEY,
            from_email=SENDGRID_FROM_EMAIL,
            recipients=RECIPIENTS,
            attachments=attachments
        )
        logging.info("Email sent successfully.")
    else:
        logging.warning("No files available to attach in email.")


def main():
    logging.info("Step 0: Monitoring and downloading latest Excel files...")
    url = "https://www.ice.gov/identify-and-arrest/287g"
    has_new_file = monitor_and_download_all(url)

    load_dotenv()
    base_dir = os.path.dirname(__file__)
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL')
    RECIPIENTS = os.getenv('RECIPIENTS').split(',')

    if has_new_file:
        process_participating_agencies()
        process_pending_agencies()
        broadcast_email(base_dir, SENDGRID_API_KEY, SENDGRID_FROM_EMAIL, RECIPIENTS)

        logging.info("Step 4: Pushing files to GitHub...")
        push_to_github()

        logging.info("All steps completed successfully!")
    else:
        logging.info("No new files detected. Skipping processing steps.")


if __name__ == "__main__":
    main()
