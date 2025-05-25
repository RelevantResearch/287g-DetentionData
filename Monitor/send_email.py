from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import os
import base64

def send_email(file_path, file_url, api_key, from_email, recipients, attachments=None):
    print("API Key Loaded:", api_key[:5] + "****")

    if file_url:
        html_content = f"<h1>New file available: <a href='{file_url}'>{file_url}</a></h1>"
    else:
        html_content = "<h4>Attached are the latest updated files for participating and pending agencies.</h4>"

    message = Mail(
        from_email=from_email,
        to_emails=recipients,
        subject="ALERT! Detention Statistics Updated",
        html_content=html_content
    )

    all_attachments = []
    
    # Handle backward compatibility for single file_path
    if file_path and os.path.exists(file_path):
        attachments = [file_path]

    if attachments:
        for path in attachments:
            with open(path, 'rb') as f:
                data = f.read()
            encoded = base64.b64encode(data).decode()

            attachment = Attachment(
                FileContent(encoded),
                FileName(os.path.basename(path)),
                FileType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                Disposition("attachment")
            )
            all_attachments.append(attachment)

        message.attachment = all_attachments

    sg = SendGridAPIClient(api_key)
    sg.send(message)
    print("Email sent successfully.")
