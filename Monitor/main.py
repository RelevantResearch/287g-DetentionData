import os
import sys
import logging
from dotenv import load_dotenv
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

base_dir = os.path.dirname(__file__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(base_dir, 'log.txt'), mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

sys.path.append(base_dir)

from normalize_agencies import normalize_agency_names
from getFilename import find_latest_file
from getHyperlink import extract_hyperlinks
from combineFiles import combine_latest_files
from monitorSheets import monitor_and_download_all
from pushGithub import push_to_github
from send_email import send_email  # SES only now
from messageToSlack import send_message_to_slack
from combinePendingAgencies import main as combine_pending_agencies
from deduplicate_pending_combined import deduplicate_pending_combined
from tryUniqueName import process_latest_agency_file
from creationOfPivotTable import generate_agency_summary
from getPendingPivot import run_pending_agencies_pivot_report

load_dotenv()
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
client = WebClient(token=SLACK_API_TOKEN)

def get_upload_url(file_path):
    try:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        response = client.files_getUploadURLExternal(filename=filename, length=file_size)
        return response['upload_url'], response['file_id']
    except SlackApiError as e:
        logging.error(f"Slack upload URL error: {e.response['error']}")
        return None, None

def upload_file_to_slack_via_sdk(file_path, title="Updated file"):
    upload_url, file_id = get_upload_url(file_path)
    if not upload_url or not file_id:
        return
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f,
                              'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(upload_url, files=files)
        if response.status_code == 200:
            logging.info("Upload to Slack successful. Finalizing...")
            client.files_completeUploadExternal(
                channel_id=SLACK_CHANNEL_ID,
                initial_comment=title,
                files=[{"id": file_id}]
            )
            logging.info(f"File posted to Slack: {file_path}")
        else:
            logging.error(f"Upload failed: {response.text}")
    except Exception as e:
        logging.error(f"Slack SDK file upload error: {e}")

def process_participating_agencies():
    logging.info("Processing Participating Agencies...")
    data_directory = os.path.join(base_dir, '..', 'participatingAgencies after feb 20')
    save_hyperlink_dir = os.path.join(base_dir, '..', 'Monitor', 'Hyperlink')
    total_agencies_dir = os.path.join(base_dir, '..', 'Total participatingAgencies')

    latest_filename = find_latest_file(data_directory)
    if not latest_filename:
        logging.warning("No .xlsx files found.")
        return

    latest_file_path = os.path.join(data_directory, latest_filename)
    extract_hyperlinks(latest_file_path, save_hyperlink_dir)
    combine_latest_files(save_hyperlink_dir, total_agencies_dir, total_agencies_dir)

    latest_hyperlink_file = find_latest_file(save_hyperlink_dir)
    if latest_hyperlink_file:
        os.remove(os.path.join(save_hyperlink_dir, latest_hyperlink_file))
        logging.info(f"Removed intermediate file: {latest_hyperlink_file}")

def process_pending_agencies():
    logging.info("Processing Pending Agencies...")
    combine_pending_agencies()
    deduplicate_pending_combined()

    total_with_dup_dir = os.path.abspath(os.path.join(base_dir, '..', 'Total pendingAgencies', 'Total_with_Duplication'))
    latest_dup_file = find_latest_file(total_with_dup_dir)
    if latest_dup_file:
        os.remove(os.path.join(total_with_dup_dir, latest_dup_file))
        logging.info(f"Removed duplicate file: {latest_dup_file}")

def broadcast_email_and_slack(updated_labels):
    attachments = []

    if "participating" in updated_labels:
        file = find_latest_file(os.path.join(base_dir, 'Agency_Name_Normalizer'))
        if file:
            attachments.append(os.path.join(base_dir, 'Agency_Name_Normalizer', file))

        pivot_file = find_latest_file(os.path.join(base_dir, '..', 'ParticipatingAgencieswithpivot'))
        if pivot_file:
            attachments.append(os.path.join(base_dir, '..', 'ParticipatingAgencieswithpivot', pivot_file))

    if "pending" in updated_labels:
        file = find_latest_file(os.path.join(base_dir, '..', 'Total pendingAgencies'))
        if file:
            attachments.append(os.path.join(base_dir, '..', 'Total pendingAgencies', file))

        pivot_file = find_latest_file(os.path.join(base_dir, '..', 'Pivot PendingAgencies'))
        if pivot_file:
            attachments.append(os.path.join(base_dir, '..', 'Pivot PendingAgencies', pivot_file))

    if attachments:
        logging.info("Sending email via SES...")
        send_email(file_path=None, file_url=None, attachments=attachments)
        logging.info("Email sent.")

def clean_unique_name_folder():
    unique_name_dir = os.path.join(base_dir, 'UniqueName')
    if os.path.exists(unique_name_dir):
        for filename in os.listdir(unique_name_dir):
            file_path = os.path.join(unique_name_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    logging.info(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                    logging.info(f"Deleted directory: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")
    else:
        logging.warning(f"Directory does not exist: {unique_name_dir}")

def main():
    logging.info("===== Script Start =====")
    updated_labels = monitor_and_download_all("https://www.ice.gov/identify-and-arrest/287g")

    if updated_labels:
        if "participating" in updated_labels:
            process_participating_agencies()
            process_latest_agency_file()
            normalize_agency_names()
            generate_agency_summary()
            clean_unique_name_folder()
        if "pending" in updated_labels:
            process_pending_agencies()
            run_pending_agencies_pivot_report()

        broadcast_email_and_slack(updated_labels)
        logging.info("Pushing updates to GitHub...")
        push_to_github()
    else:
        logging.info("No new files to process.")
    logging.info("===== Script End =====")

if __name__ == "__main__":
    main()
