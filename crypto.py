# crypto.py
# Handles encryption and decryption using Fernet (AES)

import base64
from cryptography.fernet import Fernet


def _key_to_fernet_key(key: bytes) -> bytes:
    """
    Fernet requires a base64-encoded 32-byte key
    """
    return base64.urlsafe_b64encode(key)


def encrypt(plain_text: str, key: bytes) -> str:
    fernet_key = _key_to_fernet_key(key)
    f = Fernet(fernet_key)
    encrypted = f.encrypt(plain_text.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt(cipher_text: str, key: bytes) -> str:
    fernet_key = _key_to_fernet_key(key)
    f = Fernet(fernet_key)
    decrypted = f.decrypt(cipher_text.encode("utf-8"))
    return decrypted.decode("utf-8")
