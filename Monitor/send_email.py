# sendgrid.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import os
import base64

def send_email(file_path, file_url, api_key, from_email, recipients):
    print("API Key Loaded:", api_key[:5] + "****")

    if file_url:
        html_content = f"<p>New file available: <a href='{file_url}'>{file_url}</a></p>"
    else:
        html_content = "<p>New detention statistics file is attached. Please see the attachment.</p>"

    message = Mail(
        from_email=from_email,
        to_emails=recipients,
        subject="ALERT! Detention Statistics Updated",
        html_content=html_content
    )

    with open(file_path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    attachment = Attachment(
        FileContent(encoded),
        FileName(os.path.basename(file_path)),
        FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        Disposition("attachment")
    )
    message.attachment = attachment

    sg = SendGridAPIClient(api_key)
    sg.send(message)
    print("Email sent successfully.")
