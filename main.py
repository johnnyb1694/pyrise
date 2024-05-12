from pyrise import get_gmail_access_creds, compose_email, send_email
from pathlib import Path

CREDENTIALS_PATH = Path(__file__).parent / "auth" / "credentials.json"
TOKEN_PATH = Path(__file__).parent / "auth" / "token.json"

def main():
    creds = get_gmail_access_creds(CREDENTIALS_PATH, TOKEN_PATH)
    email_content = compose_email('Testing', 'johnnyb1694@gmail.com', 'Hello, World!')
    send_email(creds, email_content)

if __name__ == '__main__':
    main()