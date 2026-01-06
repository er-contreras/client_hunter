"""
Internal operations dashboard.
Read-only view over data/ artifacts.
No delivery or mutation logic lives here.
"""

from flask import Flask, render_template
from pathlib import Path
import csv
from collections import Counter
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "web" / "templates")
)

DATA_DIR = Path("data")

def count_csv_rows(path):
    if not path.exists():
        return 0
    with path.open() as f:
        return sum(1 for _ in f)

def load_delivery_log(path):
    events = []
    if not path.exists():
        return events

    with path.open() as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 5:
                events.append({
                    "time": parts[0],
                    "phone": parts[1],
                    "channel": parts[2],
                    "status": parts[3],
                    "reason": parts[4],
                })

    return events[-20:][::-1] # last 20 newest first

@app.route("/")
def dashboard():
    ingested = count_csv_rows(DATA_DIR / "contacts.csv")
    raw = count_csv_rows(DATA_DIR / "leads_raw.csv")
    qualified = count_csv_rows(DATA_DIR / "leads_qualified.csv")

    delivery_events = load_delivery_log(DATA_DIR / "delivery.log")
    delivered = sum(1 for e in delivery_events if e["status"] == "sent")
    failed = sum(1 for e in delivery_events if e["status"] == "failed")

    success_rate = (
        round((delivered / qualified) * 100, 1)
        if qualified > 0 else 0
    )

    rejection_reasons = Counter()
    if (DATA_DIR / "leads_raw.csv").exists():
        with (DATA_DIR / "leads_raw.csv").open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") == "rejected":
                    rejection_reasons[row.get("reason", "unknown")] += 1

    return render_template(
        "dashboard.html",
        updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ingested=ingested,
        raw=raw,
        qualified=qualified,
        delivered=delivered,
        failed=failed,
        success_rate=success_rate,
        rejection_reasons=rejection_reasons,
        events=delivery_events,
    )

if __name__ == "__main__":
    app.run(debug=True)
