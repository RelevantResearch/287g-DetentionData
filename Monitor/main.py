import os
import logging
import pandas as pd
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import traceback
from pushGithub import push_to_github
from getPendingPivot import run_pending_agencies_pivot_report
from getFilename import find_latest_file, load_excel_file
from monitorSheets import monitor_and_download_all
from getHyperlink import extract_hyperlinks
from normalize_agencies import normalize_agency_names
from merge import merge_latest_normalizer_with_participating
from normalize_pending import normalize_agency_names_pending
from combinePendingAgencies import merge_pending_agencies
from creationOfPivotTable import generate_agency_summary
from cleanFolder import cleanFolder
from send_email import send_email

load_dotenv()
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
client = WebClient(token=SLACK_API_TOKEN)


# -------------------------
# Helper functions
# -------------------------

def get_latest_filename(folder_name: str) -> tuple[str | None, pd.DataFrame | None]:
    """Return the latest Excel file and its DataFrame from a folder."""
    base_directory = os.path.dirname(__file__)
    folder_path = os.path.join(base_directory, '..', folder_name)

    latest_file = find_latest_file(folder_path)
    if not latest_file:
        print(f"No matching Excel files found in folder '{folder_name}'.")
        return None, None

    file_path = os.path.join(folder_path, latest_file)
    df = load_excel_file(file_path)
    return latest_file, df


def send_file_to_slack_via_external_upload(file_path, message=None):
    """Upload a file to Slack using external upload."""
    try:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Get upload URL
        upload_response = client.files_getUploadURLExternal(
            filename=filename,
            length=file_size
        )
        upload_url = upload_response['upload_url']
        file_id = upload_response['file_id']

        # Upload file to URL
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            response = requests.post(upload_url, files=files)
        if response.status_code != 200:
            logging.error(f"Failed to upload file: {response.text}")
            return

        # Complete upload
        client.files_completeUploadExternal(
            channel_id=SLACK_CHANNEL_ID,
            initial_comment=message or "",
            files=[{"id": file_id}]
        )

        logging.info(f"File '{filename}' uploaded to Slack.")

    except SlackApiError as e:
        logging.error(f"Slack API error: {e.response['error']}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def broadcast_email_and_slack(updated_labels):
    """Send updated files via email and Slack."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    attachments = []

    if "participating" in updated_labels:
        file = find_latest_file(os.path.join(base_dir, 'CleanParticipatingAgencies'))
        if file:
            attachments.append(os.path.join(base_dir, 'CleanParticipatingAgencies', file))

        pivot_file = find_latest_file(os.path.join(base_dir, '..', 'pivotParticipatingAgencies'))
        if pivot_file:
            attachments.append(os.path.join(base_dir, '..', 'pivotParticipatingAgencies', pivot_file))

    if "pending" in updated_labels:
        file = find_latest_file(os.path.join(base_dir, '..', 'Normalized_Total_pendingAgencies'))
        if file:
            attachments.append(os.path.join(base_dir, '..', 'Normalized_Total_pendingAgencies', file))

        pivot_file = find_latest_file(os.path.join(base_dir, '..', 'pivotPendingAgencies'))
        if pivot_file:
            attachments.append(os.path.join(base_dir, '..', 'pivotPendingAgencies', pivot_file))

    if attachments:
        logging.info("Sending email with attachments...")
        send_email(file_path=None, file_url=None, attachments=attachments)
        logging.info("Email sent.")

        logging.info("Sending Slack alert...")
        try:
            client.chat_postMessage(
                channel=SLACK_CHANNEL_ID,
                text="ALERT! New 287(g) Spreadsheet"
            )
        except SlackApiError as e:
            logging.error(f"Slack message error: {e.response['error']}")

        logging.info("Uploading files to Slack...")
        for file_path in attachments:
            send_file_to_slack_via_external_upload(file_path)
        logging.info("Slack upload complete.")


# -------------------------
# Main pipeline
# -------------------------

def monitor_sheets():
    """Monitor ICE 287(g) site, process updates, and broadcast results."""
    url = "https://www.ice.gov/identify-and-arrest/287g"
    updated = monitor_and_download_all(url)

    if not updated:
        print("No new updates found.")
        return

    updated_labels = []

    # Pending agencies pipeline
    if "pending" in updated:
        print("\nProcessing pending agencies...")
        normalize_agency_names_pending(
            pending_dir="pendingAgencies",
            output_dir="Monitor/Agency_Pending_Normalizer"
        )
        merge_pending_agencies()
        print("Finished pending pipeline.\n")
        updated_labels.append("pending")

        print("Generating pivot table for pending agencies...")
        try:
            run_pending_agencies_pivot_report()
            print("Finished successfully!\n")
        except Exception:
            traceback.print_exc()

    # Participating agencies pipeline
    if "participating" in updated:
        print("\nProcessing participating agencies...")
        folder_name = "participatingAgencies"

        filename, df = get_latest_filename(folder_name)
        if df is not None:
            print(f"Latest file: {filename} ({len(df)} rows, {len(df.columns)} columns)")

        df = extract_hyperlinks(folder_name)

        normalize_agency_names(
            txt_path="last-participating.txt",
            directory="Hyperlink",
            output_dir="Agency_Name_Normalizer"
        )

        merge_latest_normalizer_with_participating(
            normalizer_folder="Agency_Name_Normalizer",
            participating_folder="CleanParticipatingAgencies",
            merge_folder="CleanParticipatingAgencies",
            last_participating_file="last-participating.txt"
        )

        print("Generating pivot table for participating agencies...")
        try:
            generate_agency_summary()
            print("Finished participating pipeline!\n")
        except Exception:
            traceback.print_exc()

        cleanFolder("Hyperlink")
        updated_labels.append("participating")

    # Broadcast updates
    if updated_labels:
        print(f"Broadcasting updates: {updated_labels}")
        # broadcast_email_and_slack(updated_labels)
    
    push_to_github()


if __name__ == "__main__":
    monitor_sheets()
