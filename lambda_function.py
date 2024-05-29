import os
import boto3
import logging
from pyrise import (
    get_gmail_access_creds, 
    compose_email, 
    send_email, 
    generate_email_body,
    get_recipes
)
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger()
log.setLevel('INFO')


def lambda_handler(
    event, 
    context
) -> None:
    """Lambda handler for email service.
    """
    s3 = boto3.client('s3')

    log.info('Downloading Google API access credentials')
    s3.download_file("pyrise", "credentials.json", "/tmp/credentials.json")
    s3.download_file("pyrise", "token.json", "/tmp/token.json")
    creds = get_gmail_access_creds("/tmp/credentials.json", "/tmp/token.json")

    log.info('Downloading recipes of interest')
    recipes = get_recipes(
        app_id=os.environ.get("EDAMAM_APP_ID"),
        app_key=os.environ.get("EDAMAM_API_KEY"),
        n = 5
    )

    log.info('Generating dynamic email template')
    email_body = generate_email_body(
        context={"recipes": recipes},
        template_root="templates",
        template_name="email.html"
    )
    content = compose_email(
        "pyrise - Daily Email", 
        "johnnyb1694@gmail.com", 
        email_body
    )

    log.info('Issuing email to recipients')
    send_email(creds, content)
    
    log.info('Refreshing Google API access credentials')
    s3.upload_file("/tmp/credentials.json", "pyrise", "credentials.json")
    s3.upload_file("/tmp/token.json", "pyrise", "token.json")

if __name__ == '__main__':
    pass