# import os
# import boto3
# import base64
# from botocore.exceptions import ClientError
# from dotenv import load_dotenv
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# # Load environment variables
# load_dotenv()

# SES_REGION = os.getenv("SES_REGION")
# SES_FROM_EMAIL = os.getenv("SES_FROM_EMAIL")
# RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")

# def send_email(file_path=None, file_url=None, attachments=None):
#     ses_client = boto3.client("ses", region_name=SES_REGION)

#     # Email body
#     if file_url:
#         html_content = f"<h1>New file available: <a href='{file_url}'>{file_url}</a></h1>"
#     else:
#         html_content = "<h4>Attached are the latest updated files for participating and pending agencies.</h4>"

#     subject = "ALERT! New 287(g) Spreadsheet"

#     try:
#         if (file_path and os.path.exists(file_path)) or attachments:
#             # If only single file_path is given, wrap it in a list
#             if file_path and not attachments:
#                 attachments = [file_path]

#             msg = MIMEMultipart()
#             msg["Subject"] = subject
#             msg["From"] = SES_FROM_EMAIL
#             msg["To"] = ", ".join(RECIPIENT_EMAILS)

#             msg.attach(MIMEText(html_content, "html"))

#             # Attach files
#             for path in attachments:
#                 with open(path, "rb") as f:
#                     part = MIMEBase("application", "octet-stream")
#                     part.set_payload(f.read())
#                     encoders.encode_base64(part)
#                     part.add_header(
#                         "Content-Disposition",
#                         f'attachment; filename="{os.path.basename(path)}"',
#                     )
#                     msg.attach(part)

#             # Send raw email
#             ses_client.send_raw_email(
#                 Source=SES_FROM_EMAIL,
#                 Destinations=RECIPIENT_EMAILS,
#                 RawMessage={"Data": msg.as_string()},
#             )

#         else:
#             # Send simple HTML email without attachment
#             ses_client.send_email(
#                 Source=SES_FROM_EMAIL,
#                 Destination={"ToAddresses": RECIPIENT_EMAILS},
#                 Message={
#                     "Subject": {"Data": subject, "Charset": "UTF-8"},
#                     "Body": {
#                         "Html": {"Data": html_content, "Charset": "UTF-8"}
#                     },
#                 },
#             )

#         print("Email sent successfully via SES.")

#     except ClientError as e:
#         print("Error sending email:", e.response["Error"]["Message"])


# # Example usage
# # send_email(file_path="main.py")  # With attachment
# # send_email(file_url="https://example.com/file.xlsx")  # With link
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables
load_dotenv()

SES_REGION = os.getenv("SES_REGION")
SES_FROM_EMAIL = os.getenv("SES_FROM_EMAIL")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS").split(",")

def send_email(file_path=None, file_url=None, api_key=None, from_email=None, recipients=None, attachments=None):
    """
    SES-based email sender that keeps the old SendGrid-style signature
    so main.py doesn't need changes.
    """
    ses_client = boto3.client("ses", region_name=SES_REGION)

    if file_url:
        html_content = f"<h1>New file available: <a href='{file_url}'>{file_url}</a></h1>"
    else:
        html_content = "<h4>Attached are the latest updated files for participating and pending agencies.</h4>"

    subject = "ALERT! New 287(g) Spreadsheet"

    try:
        if (file_path and os.path.exists(file_path)) or attachments:
            if file_path and not attachments:
                attachments = [file_path]

            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = SES_FROM_EMAIL
            msg["To"] = ", ".join(RECIPIENT_EMAILS)

            msg.attach(MIMEText(html_content, "html"))

            for path in attachments:
                with open(path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{os.path.basename(path)}"',
                    )
                    msg.attach(part)

            ses_client.send_raw_email(
                Source=SES_FROM_EMAIL,
                Destinations=RECIPIENT_EMAILS,
                RawMessage={"Data": msg.as_string()},
            )

        else:
            ses_client.send_email(
                Source=SES_FROM_EMAIL,
                Destination={"ToAddresses": RECIPIENT_EMAILS},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Html": {"Data": html_content, "Charset": "UTF-8"}},
                },
            )

        print("✅ Email sent successfully via SES.")

    except ClientError as e:
        print("❌ Error sending email:", e.response["Error"]["Message"])
