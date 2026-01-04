import csv
from pathlib import Path

THRESHOLD = 0.7
BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "leads_raw.csv"
output_file = BASE_DIR / "data" / "leads_qualified.csv"

print(f"Reading from: {input_file}")
print(f"Writing to: {output_file}")

with input_file.open() as f_in, output_file.open("w", newline="") as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.writer(f_out)

    writer.writerow([
        "business_name",
        "phone",
        "score",
        "reason"
    ])

    for row in reader:
        score = 0.0
        reasons = []

        if row["industry"]:
            score += 0.3
            reasons.append("has industry")

        if row["website"].startswith("http"):
            score += 0.3
            reasons.append("has website")

        if not row["email"]:
            score += 0.2
            reasons.append("no email listed")

        if row["city"]:
            score += 0.2
            reasons.append("local business")

        if score < THRESHOLD:
            print(
                f"SKIP {row['business_name']} "
                f"(score={round(score, 2)})"
            )
            continue

        writer.writerow([
            row["business_name"],
            row["phone"],
            round(score, 2),
            "; ".join(reasons)
        ])

print("qualification complete")
