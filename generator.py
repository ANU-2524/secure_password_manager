# generator.py
# Strong password generator

import secrets
import string


def generate_password(length=16):
    if length < 8:
        raise ValueError("Password length must be at least 8")

    chars = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    return ''.join(secrets.choice(chars) for _ in range(length))
