import time
import os
from notifier.lead import (
    parse_lead,
    validate_lead,
    has_seen_phone,
    mark_phone_seen
)
from notifier.delivery import ConsoleDelivery
from notifier.email_delivery import EmailDelivery

CSV_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "contacts.csv"
)

CSV_PATH = os.path.abspath(CSV_PATH)

def tail_last_line(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in reversed(lines):
        line = line.strip()
        if line:
            return line

    return ""

def watch():
    delivery = EmailDelivery()

    print(f"Watching {CSV_PATH}")
    last_size = os.path.getsize(CSV_PATH)

    while True:
        time.sleep(1)
        current_size = os.path.getsize(CSV_PATH)

        if current_size > last_size:
            line = tail_last_line(CSV_PATH)

            lead = parse_lead(line)
            valid, reasons = validate_lead(lead)

            if not valid:
                print("REJECTED LEAD:")
                print(" reasons:", ", ".join(reasons))

            else:
                phone = lead.phone

                if has_seen_phone(phone):
                    print("DUPLICATED LEAD (ignored):", phone)
                else:
                    mark_phone_seen(phone)
                    delivery.send(lead)

            last_size = current_size

if __name__ == "__main__":
    watch()
