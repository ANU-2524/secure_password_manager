# vault.py
# Encrypted credential storage with CRUD operations

import json
import os
from crypto import encrypt, decrypt

STORAGE_FILE = "storage.json"


def _load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {}
    if os.path.getsize(STORAGE_FILE) == 0:
        return {}
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def _save_storage(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_credential(service, username, password, key):
    data = _load_storage()
    data[service] = {
        "username": encrypt(username, key),
        "password": encrypt(password, key)
    }
    _save_storage(data)


def get_credential(service, key):
    data = _load_storage()
    if service not in data:
        return None

    return {
        "username": decrypt(data[service]["username"], key),
        "password": decrypt(data[service]["password"], key)
    }


def delete_credential(service):
    data = _load_storage()
    if service in data:
        del data[service]
        _save_storage(data)


def list_services():
    return list(_load_storage().keys())
