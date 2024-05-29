import os
from pyrise import (
    get_gmail_access_creds, 
    compose_email, 
    send_email, 
    generate_email_body,
    get_recipes
)
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_PATH = Path(__file__).parent / "auth" / "credentials.json"
TOKEN_PATH = Path(__file__).parent / "auth" / "token.json"

def local_handler():
    """Local handler for email service.
    """
    creds = get_gmail_access_creds(CREDENTIALS_PATH, TOKEN_PATH)
    
    recipes = get_recipes(
        app_id=os.environ.get("EDAMAM_APP_ID"),
        app_key=os.environ.get("EDAMAM_API_KEY"),
        n = 5
    )
    email_body = generate_email_body(
        context={"recipes": recipes}
    )
    content = compose_email(
        "pyrise - Daily Email", 
        "johnnyb1694@gmail.com", 
        email_body
    )
    send_email(creds, content)


if __name__ == '__main__':
    local_handler()