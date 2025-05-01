import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Slack API token and channel ID from the environment
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')
SLACK_CHANNEL_ID = os.getenv('SLACK_CHANNEL_ID')

def send_message_to_slack(message, attachments=None):
    url = "https://slack.com/api/chat.postMessage"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_API_TOKEN}"
    }

    payload = {
        "channel": SLACK_CHANNEL_ID,
        "text": message
    }

    if attachments:
        payload["attachments"] = attachments

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 and response.json().get("ok"):
        print("Message sent successfully to Slack.")
    else:
        print(f"Error sending message to Slack: {response.text}")

if __name__ == "__main__":
    # This part can be used to test the message
    message = "Test message to Slack"
    send_message_to_slack(message)
