# Secure Password Manager

A small, secure password manager built as a CLI tool and extended with a lightweight web UI (Flask). It stores credentials encrypted with a key derived from a master password.

Features
- Master password protected (bcrypt hash stored in `config.json`).
- Credentials encrypted using Fernet (AES) with a key derived via PBKDF2-HMAC-SHA256.
- CLI interface (original) and a new minimal web UI (`webapp.py`) with basic CRUD for credentials.
- Password generator and clipboard copy functionality.

Requirements
- Python 3.10+
- See `requirements.txt` for exact package versions.

Quick setup
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Run the CLI

```bash
python main.py
```

Run the web app

```bash
python webapp.py
# open http://127.0.0.1:5000
```

Security notes
- The master password is never stored; only its bcrypt hash is saved in `config.json`.
- A persistent KDF salt is stored in `config.json` so the same derived key is produced across runs.
- The web UI currently stores the derived key in the session (base64). For production, avoid storing raw keys in sessions/cookies — use server-side secure storage or re-derive the key on each request after re-authentication.
- Keep `config.json` and `storage.json` protected; do not commit them to public repositories.

Development & contribution
- The project aims to preserve the CLI behavior. New web UI files were added and existing modules were not modified.
- To contribute: fork, add tests, and submit a pull request. For security-sensitive changes, provide rationale and tests.

Files of interest
- `main.py` — original CLI entrypoint
- `webapp.py` — new Flask-based web UI
- `vault.py`, `crypto.py`, `kdf.py`, `auth.py` — core security and storage logic
- `templates/` — Jinja templates for web UI



