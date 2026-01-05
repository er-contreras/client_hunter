import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Lead:
    timestamp: int
    name: str
    phone: str
    email: Optional[str] = None
    message: Optional[str] = None
    source: str = "unknown"

SEEN_PHONES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "seen_phones.txt")
)

def parse_lead(csv_line):
    parts = [p.strip() for p in csv_line.split(",")]

    return Lead(
        timestamp=int(parts[0]) if len(parts) > 0 and parts[0] else 0,
        name=parts[1] if len(parts) > 1 else "",
        phone=parts[2] if len(parts) > 2 else "",
        email=parts[3] if len(parts) > 3 else None,
        message=parts[4] if len(parts) > 4 else None,
        source=parts[5] if len(parts) > 5 else "web",
    )

def normalize_phone(phone):
    return "".join(c for c in phone if c.isdigit())

def validate_lead(lead):
    reasons = []

    if not lead.name:
        reasons.append("missing name")

    phone = lead.phone
    if not phone or len(phone) < 8:
        reasons.append("invalid phone")

    if reasons:
        return False, reasons

    return True, []

def has_seen_phone(phone):
    if not os.path.exists(SEEN_PHONES_PATH):
        return False

    with open(SEEN_PHONES_PATH, "r", encoding="utf-8") as f:
        seen = {line.strip() for line in f if line.strip()}

    return phone in seen

def mark_phone_seen(phone):
    os.makedirs(os.path.dirname(SEEN_PHONES_PATH), exist_ok=True)
    with open(SEEN_PHONES_PATH, "a", encoding="utf-8") as f:
        f.write(phone + "\n")
