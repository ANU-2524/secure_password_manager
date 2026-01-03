# kdf.py
# Key Derivation using PBKDF2-HMAC-SHA256

import os
import json
import base64
import hashlib

CONFIG_FILE = "config.json"


def _load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def _save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_or_create_salt():
    """
    Generates a salt once and stores it.
    Same salt must be reused for correct key derivation.
    """
    config = _load_config()

    if "kdf_salt" in config:
        return base64.b64decode(config["kdf_salt"])

    salt = os.urandom(16)
    config["kdf_salt"] = base64.b64encode(salt).decode("utf-8")
    _save_config(config)

    return salt


def derive_key(master_password: str) -> bytes:
    """
    Derives a 256-bit key from master password
    """
    salt = get_or_create_salt()

    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=master_password.encode("utf-8"),
        salt=salt,
        iterations=200_000,
        dklen=32
    )

    return key
