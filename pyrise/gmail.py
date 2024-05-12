"""Contains functionality to send emails using Google's API client in Python.

The key function exposed by this module is `send_email()`.
"""
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path


def get_gmail_access_creds(
    credentials_path: Path | str,
    token_path: Path | str
) -> Credentials:
    """Get access token for the Gmail API resource via OAuth 2.0 Flow:
    
    https://datatracker.ietf.org/doc/html/rfc6749#section-1.2

    Credentials (`credentials.json`) must be first initialised manually via 
    the Google Cloud console.
    """
    try:
        creds = Credentials.from_authorized_user_file(token_path)
    except FileNotFoundError:
        # Generate access token via the local browser
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path,  
            ["https://www.googleapis.com/auth/gmail.send"]
        )
        # Temporarily configures a local server to 'listen' for an authorization response
        creds = flow.run_local_server(port=0)

    # Token exists  
    if creds and creds.valid:
        pass

    # Token must be refreshed     
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    with open(token_path, "w") as token_file:
        token_file.write(creds.to_json())

    return creds


def compose_email(
    mail_subject: str, 
    email_recipient: str, 
    mail_body: str
) -> dict[str, bytes]:
    """Construct the email message to be sent by the Python client.

    TODO: add validation on the email recipient argument!

    Args:
        mail_subject (str): email subject
        email_recipient (str): email recipient
        mail_body (str): email contents
    """
    message = {
        'raw': base64.urlsafe_b64encode(
            f'MIME-Version: 1.0\n'
            f'Content-Type: text/html; charset="UTF-8"\n'
            f"From: pyrise.no.reply@gmail.com\n"
            f"To: {email_recipient}\n"
            f"Subject: {mail_subject}\n\n"
            f"{mail_body}"
            .encode("utf-8")
        ).decode("utf-8")
    }
    return message


def send_email(
    creds: Credentials, 
    content: dict[str, bytes]
) -> None:
    """Issue an email that has been composed with `compose_email()`

    Args:
        creds (Credentials): access credentials via `get_gmail_access_creds()`
        content (dict[str, bytes]): email data composed with `compose_email()`
    """
    service = build('gmail', 'v1', credentials=creds)
    try:
        service.users().messages().send(userId='me', body=content).execute()
        print('Email sent successfully.')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))


if __name__ == '__main__':
    pass