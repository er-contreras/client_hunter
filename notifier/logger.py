import csv
import os
import time

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "call_logs.csv")
)

HEADERS = ["timestamp", "channel", "lead_phone", "lead_email", "status", "details"]

def log_delivery(channel, lead, status, details=""):
    file_exists = os.path.exists(LOG_PATH)

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(HEADERS)

        writer.writerow([
            int(time.time()),
            channel,
            lead.phone,
            lead.email,
            status,
            details
        ])
