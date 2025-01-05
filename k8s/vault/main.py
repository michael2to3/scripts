import os
import subprocess

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

FLAG = None


def get_flag_from_vault():
    vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.environ.get("VAULT_TOKEN", "")
    secret_path = "secret/data/app"

    url = f"{vault_addr}/v1/{secret_path}"
    headers = {"X-Vault-Token": vault_token}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        secret_data = data["data"]["data"]
        return secret_data.get("flag", "FLAG_NOT_FOUND")
    except Exception as e:
        print(f"Error requesting Vault: {e}")
        return "ERROR"


@app.before_request
def load_flag_once():
    global FLAG
    if FLAG is None:
        FLAG = get_flag_from_vault()


@app.route("/")
def index():
    return "Hello from Flask! /flag or /exec?cmd=<command>"


@app.route("/flag")
def get_flag():
    return jsonify({"flag": FLAG})


@app.route("/exec")
def exec_cmd():
    cmd = request.args.get("cmd")
    if not cmd:
        return "Usage: /exec?cmd=<command>"
    try:
        r = subprocess.check_output(cmd, shell=True, text=True)
        return r
    except subprocess.CalledProcessError as e:
        return e


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
