# 🔐 SecureVault | Premium Password Manager

> **"Security meets Simplicity."**
> *Developed during the Winter Internship '25 at console.success.*

**SecureVault** is a robust, self-hosted password manager designed for those who value both security and aesthetics. Built with a **Python/Flask** backend and a **Modern Dark Mode** frontend, it ensures your credentials are stored safely using industry-standard encryption while providing a premium user experience.

---

##  Key Features

### 🛡️ Iron-Clad Security
*   **Zero-Knowledge Architecture**: Your passwords are encrypted using **AES-256 (Fernet)**. Even if the database is stolen, it's useless without your master key.
*   **Secure Authentication**: Master passwords are hashed using **bcrypt** (slow hashing) to resist brute-force attacks.
*   **PBKDF2 Key Derivation**: Uses unique salts and high iteration counts to derive encryption keys securely.

###  Premium User Experience
*   **Modern Dark UI**: A sleek, distraction-free interface designed for extended use.
*   **Glassmorphism Design**: Beautiful, responsive layout with smooth transitions.
*   **Instant Search**: Filter through your credentials instantly.

###  Smart Utilities
*   **Auto-Clear Clipboard**: Copies passwords to your clipboard and **automatically clears them after 10 seconds** to prevent leaks.
*   **Password Generator**: Create strong, random passwords (8-64 chars) with a single click.
*   **Strength Meter**: Real-time visual feedback on password strength.

---

##  Tech Stack

*   **Backend**: Python 3.10+, Flask
*   **Security**: `cryptography` (Fernet), `bcrypt`
*   **Frontend**: HTML5, Vanilla CSS3 (Variables, Flexbox/Grid), JavaScript (ES6+)
*   **Storage**: JSON (Encrypted)

---

## Getting Started

Follow these steps to set up your own secure vault in minutes.

### Prerequisites
*   Python 3.10 or higher installed.

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd secure_password_manager
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Server**
    ```bash
    python webapp.py
    ```

2.  **Access the Vault**
    *   Open your browser and navigate to: `http://127.0.0.1:5000`
    *   **First Run**: You will be redirected to the **Setup** page to create your Master Password.

---

##  Usage Guide

1.  **Setup**: Create a strong Master Password. This key encrypts your entire vault. **Do not lose it!**
2.  **Dashboard**: View all your services in a grid layout. Use the search bar to find specific accounts.
3.  **Add Credential**: Click "Add New", enter the service name, username, and password. Watch the strength meter!
4.  **Copy & Go**: Click the "Copy" button next to any password. It will be in your clipboard for **10 seconds** before vanishing.
5.  **Generate**: Need a new password? Go to the "Generator" tab, slide to your desired length, and copy.

---

##  Security Architecture

*   **Storage**: All data is stored in `storage.json`.
*   **Encryption**:
    *   **Usernames & Passwords**: Encrypted with Fernet (AES-128 in CBC mode with PKCS7 padding, HMAC-SHA256 for integrity).
    *   **Master Password**: Never stored. Only a bcrypt hash is saved to verify login.
    *   **Key Management**: The encryption key is derived from your master password using PBKDF2-HMAC-SHA256 with a unique, random salt.

---

## Disclaimer

This tool is designed for educational and personal use. While it uses industry-standard encryption libraries, always ensure you have backups of your critical data.

---

*Made with ❤️ and Python.*
