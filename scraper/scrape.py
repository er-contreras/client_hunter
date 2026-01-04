import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data_dir = BASE_DIR / "data"
data_dir.mkdir(exist_ok=True)

file = data_dir / "leads_raw.csv"

exists = file.exists()

with file.open("a", newline="") as f:
    writer = csv.writer(f)
    if not exists:
        writer.writerow([
            "business_name",
            "industry",
            "city",
            "phone",
            "email",
            "website",
            "notes"
        ])

    writer.writerow([
        "Test Plumbing Co",
        "Plumbing",
        "Test City",
        "555-1234",
        "test@example.com",
        "http://example.com",
        "manual test entry"
    ])

print("lead written")

