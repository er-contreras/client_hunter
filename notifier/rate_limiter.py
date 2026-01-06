import csv
import os
import time
from datetime import datetime

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "call_logs.csv")
)

HOURLY_LIMIT = 5
DAILY_LIMIT = 20


def _read_logs():
    if not os.path.exists(LOG_PATH):
        return []

    with open(LOG_PATH, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _within_window(ts, seconds):
    return int(time.time()) - int(ts) <= seconds


def can_send(channel="email"):
    logs = _read_logs()

    sent_logs = [
        r for r in logs
        if r["channel"] == channel and r["status"] == "SENT"
    ]

    hourly = [
        r for r in sent_logs
        if _within_window(r["timestamp"], 3600)
    ]

    daily = [
        r for r in sent_logs
        if _within_window(r["timestamp"], 86400)
    ]

    if len(hourly) >= HOURLY_LIMIT:
        return False, "hourly-limit"

    if len(daily) >= DAILY_LIMIT:
        return False, "daily-limit"

    return True, None

