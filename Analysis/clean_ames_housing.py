"""Clean AmesHousing-1.csv for analysis of sale price by half-bath increments."""

import csv
from pathlib import Path


SOURCE = Path(__file__).with_name("AmesHousing-1.csv")
OUTPUT = Path(__file__).with_name("AmesHousing_clean.csv")
BATH_COLUMNS = ("Bsmt Full Bath", "Bsmt Half Bath", "Full Bath", "Half Bath")
BASEMENT_EVIDENCE = ("Bsmt Qual", "Total Bsmt SF")


def is_missing(value):
    return value is None or not value.strip() or value.strip().upper() in {"NA", "N/A", "NULL"}


with SOURCE.open(newline="", encoding="utf-8-sig") as source_file:
    reader = csv.DictReader(source_file)
    fieldnames = [name.strip() for name in reader.fieldnames]
    rows = []
    seen_pid = set()
    seen_rows = set()
    for raw in reader:
        row = {key.strip(): (value.strip() if value is not None else "") for key, value in raw.items()}

        # Exact duplicate rows and repeated property IDs are redundant for this
        # property-level price analysis; keep the first occurrence if present.
        signature = tuple(row.get(name, "") for name in fieldnames)
        if signature in seen_rows:
            continue
        pid = row.get("PID", "")
        if pid and pid in seen_pid:
            continue

        # A missing basement bath count is zero only when the record indicates
        # there is no basement; otherwise it is unknown and cannot form the sum.
        basement_absent = (
            is_missing(row.get("Bsmt Qual", ""))
            and (is_missing(row.get("Total Bsmt SF", "")) or float(row["Total Bsmt SF"]) == 0)
        )
        invalid_bath = False
        for column in BATH_COLUMNS:
            value = row.get(column, "")
            if is_missing(value) and column.startswith("Bsmt ") and basement_absent:
                row[column] = "0"
            elif is_missing(value):
                invalid_bath = True
                break
            else:
                try:
                    number = float(value)
                    if number < 0 or not number.is_integer():
                        invalid_bath = True
                        break
                    row[column] = str(int(number))
                except ValueError:
                    invalid_bath = True
                    break
        if invalid_bath:
            continue

        try:
            price = float(row.get("SalePrice", ""))
            if price <= 0 or not price.is_integer():
                continue
            row["SalePrice"] = str(int(price))
        except ValueError:
            continue

        # Half Bath fields count half-bath rooms; each contributes 0.5 to the
        # total bathroom amount used to evaluate half-bath increments.
        total_bathrooms = (
            int(row["Bsmt Full Bath"])
            + 0.5 * int(row["Bsmt Half Bath"])
            + int(row["Full Bath"])
            + 0.5 * int(row["Half Bath"])
        )
        row["Total Bathrooms"] = f"{total_bathrooms:g}"
        rows.append(row)
        seen_rows.add(signature)
        if pid:
            seen_pid.add(pid)

fieldnames.append("Total Bathrooms")
with OUTPUT.open("w", newline="", encoding="utf-8") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {OUTPUT.name}")
