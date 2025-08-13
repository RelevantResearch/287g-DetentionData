import os
import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')

client = WebClient(token=SLACK_API_TOKEN)

def send_file_to_slack_via_external_upload(file_path, message=None):
    try:
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Step 1: Get upload URL
        upload_response = client.files_getUploadURLExternal(
            filename=filename,
            length=file_size
        )
        upload_url = upload_response['upload_url']
        file_id = upload_response['file_id']

        # Step 2: Upload file to given URL
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f, 'application/octet-stream')}
            upload_result = requests.post(upload_url, files=files)
        if upload_result.status_code != 200:
            print(f"❌ Failed to upload file: {upload_result.text}")
            return

        # Step 3: Complete upload
        client.files_completeUploadExternal(
            channel_id=SLACK_CHANNEL_ID,
            initial_comment=message or "",
            files=[{"id": file_id}]
        )

        print(f"✅ File '{filename}' uploaded to Slack.")

    except SlackApiError as e:
        print(f"❌ Slack API error: {e.response['error']}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    send_file_to_slack_via_external_upload("testSheetjustIgnoreIt.xlsx", "Test Sheet Just Ignore It.")

