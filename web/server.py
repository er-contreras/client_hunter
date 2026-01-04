from flask import Flask, request, render_template
from pathlib import Path
import csv
import time

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "contacts.csv"


@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "")
        phone = request.form.get("phone", "")

        exists = DATA_FILE.exists()

        with DATA_FILE.open("a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["timestamp", "name", "phone"])
            writer.writerow([int(time.time()), name, phone])

        return "OK"

    return render_template("contact.html")


if __name__ == "__main__":
    print("Flask server running on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=False)

