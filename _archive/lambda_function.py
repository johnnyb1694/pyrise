import os
import boto3
from pyrise import (
    get_gmail_access_creds, 
    compose_email, 
    send_email, 
    generate_email_body,
    get_recipes,
    encrypt,
    decrypt
)
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

S3_CLIENT = boto3.client('s3')
AUTH_KEY = os.environ.get('AUTH_KEY')

def download_gmail_access_token(
    bucket_name: str = 'pyrise',
    object_key: str = './token.json', 
    local_path: Path | str = '/tmp/token.json'
) -> None:
    S3_CLIENT.download_file(bucket_name, object_key, local_path)
    with open(local_path, 'rb') as token_file:
        encrypted = token_file.read()
        decrypt(AUTH_KEY, encrypted, local_path)

def upload_gmail_access_token(
    bucket_name: str = 'pyrise',
    object_key: str = './token.json', 
    local_path: Path | str = '/tmp/token.json'
) -> None:
    with open(local_path, 'rb') as token_file:
        decrypted = token_file.read()
        encrypt(AUTH_KEY, decrypted, local_path)
        S3_CLIENT.upload_file(bucket_name, object_key, local_path)

def lambda_handler(
    event, 
    context
) -> None:
    """Lambda handler for email service.
    """
    download_gmail_access_token('', '')

    creds = get_gmail_access_creds('./auth/credentials.json', '/tmp/token.json')
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

    upload_gmail_access_token('', '')

if __name__ == '__main__':
    pass