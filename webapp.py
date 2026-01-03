from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
import base64
import bcrypt

import kdf
import vault
import generator

app = Flask(__name__)
app.secret_key = os.urandom(24)

CONFIG_FILE = "config.json"


def _load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def _save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_master_password_set():
    return "password_hash" in _load_config()


def verify_password(plain_password: str) -> bool:
    cfg = _load_config()
    if "password_hash" not in cfg:
        return False
    stored = cfg["password_hash"].encode("utf-8")
    return bcrypt.checkpw(plain_password.encode("utf-8"), stored)


@app.route("/")
def index():
    if not is_master_password_set():
        return redirect(url_for("setup"))
    if "key" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if is_master_password_set():
        return redirect(url_for("login"))

    if request.method == "POST":
        pwd = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if pwd != confirm:
            flash("Passwords do not match", "danger")
            return render_template("setup.html")
        if len(pwd) < 8:
            flash("Password must be at least 8 characters", "danger")
            return render_template("setup.html")

        # Ensure KDF salt exists (kdf will create if missing)
        kdf.get_or_create_salt()

        password_hash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt(rounds=15)).decode("utf-8")
        cfg = _load_config()
        cfg["password_hash"] = password_hash
        _save_config(cfg)

        flash("Master password set. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("setup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pwd = request.form.get("password", "")
        if not verify_password(pwd):
            flash("Incorrect password", "danger")
            return render_template("login.html")

        # derive key and store in session (base64) for use by vault
        key = kdf.derive_key(pwd)
        session["key"] = base64.b64encode(key).decode("utf-8")
        flash("Logged in", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


def get_key_from_session():
    b = session.get("key")
    if not b:
        return None
    return base64.b64decode(b)


@app.route("/logout")
def logout():
    session.pop("key", None)
    flash("Logged out", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "key" not in session:
        return redirect(url_for("login"))
    services = vault.list_services()
    return render_template("dashboard.html", services=services)


@app.route("/add", methods=["GET", "POST"])
def add():
    if "key" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        service = request.form.get("service")
        username = request.form.get("username")
        password = request.form.get("password")
        key = get_key_from_session()
        vault.add_credential(service, username, password, key)
        flash("Credential added", "success")
        return redirect(url_for("dashboard"))
    return render_template("add.html")


@app.route("/view/<service>")
def view(service):
    if "key" not in session:
        return redirect(url_for("login"))
    key = get_key_from_session()
    cred = vault.get_credential(service, key)
    if not cred:
        flash("Not found", "warning")
        return redirect(url_for("dashboard"))
    return render_template("view.html", service=service, cred=cred)


@app.route("/delete/<service>")
def delete(service):
    if "key" not in session:
        return redirect(url_for("login"))
    vault.delete_credential(service)
    flash("Deleted", "info")
    return redirect(url_for("dashboard"))


@app.route("/generate", methods=["GET", "POST"])
def generate():
    if "key" not in session:
        return redirect(url_for("login"))
    pwd = None
    if request.method == "POST":
        length = int(request.form.get("length", 16))
        try:
            pwd = generator.generate_password(length)
        except Exception as e:
            flash(str(e), "danger")
    return render_template("generate.html", pwd=pwd)


if __name__ == "__main__":
    app.run(debug=True)
