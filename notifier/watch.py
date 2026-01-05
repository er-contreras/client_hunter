import time
import os
from notifier.lead import (
    parse_lead,
    validate_lead,
    has_seen_phone,
    mark_phone_seen
)
from notifier.delivery import ConsoleDelivery, WebhookDelivery, WhatsAppDelivery

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
    # delivery = ConsoleDelivery()
    # delivery = WebhookDelivery(url="https://your-webhook-endpoint.com/receive_lead")

    # Replace with your credentials
    phone_number_id = "988725430981915"
    access_token = "EAATpH4GNaJgBQaVqkcaQlY6UOa4zfpZAZCKc58JgUt6bFlaL2NqoSaOtnQZC4QsveoSSKKU5EJodJALrg2cVrpLZA0DVlZC1KFtkR9dRuMsSzBMXuebxii1zCTetyZAMxdVh8ZBMwb7xiKJBtrVAedGB2qnZAxtQuRMXbdMQZCTYkxxNLl4HK9PsU6nF6b3j14k6B8hhLDqZBiXQpS6YVE1V4DmtK7L21213qJZBZBtyKiIX1QxaZCD6Ok1VXSMJFsIFZAGxrMZBKGHi82lmVFdWZCFKl9TEHZCpU"
    template_name = "Erick Contreras"
    
    delivery = WhatsAppDelivery(
        phone_number_id=phone_number_id,
        access_token=access_token,
        template_name=template_name
    )

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
