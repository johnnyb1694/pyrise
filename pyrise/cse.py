"""Module responsible for implementing client-side encryption of sensitive data.
"""
from cryptography.fernet import Fernet
from pathlib import Path

def persist(content: bytes, path: Path | str | None) -> None:
    """Save content to a file, if path is provided

    Args:
        content (bytes): The content to save
        path (Path | str | None): The file path to save the content to
    """
    if path:
        with open(path, 'wb') as file:
            file.write(content)


def generate_key(
    path: Path | str | None = None
) -> None:
    """Generate (symmetric) encryption key

    Args:
        path (Path | str): storage location
    """
    key = Fernet.generate_key()
    persist(key, path)
    return key


def encrypt(
    key: str,
    content: str, 
    path: Path | str | None = None
) -> None:
    """Encrypt an input string

    Args:
        key (str): encryption key
        content (str): string to encrypt
    """
    fernet = Fernet(key)
    encryption = fernet.encrypt(content)
    persist(encryption, path)
    return encryption


def decrypt(
    key: str,
    content: str,
    path: Path | str | None = None
) -> str:
    """Decrypt an input string

    Args:
        key (str): encryption key
        content (str): string to decrypt
    """
    fernet = Fernet(key)
    decryption = fernet.decrypt(content)
    persist(decryption, path)
    return decryption


if __name__ == '__main__':
    pass

