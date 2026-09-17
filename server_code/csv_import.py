import csv
import io
from datetime import datetime

import anvil.server
from anvil.tables import app_tables

# WooCommerce order exports use UK day/month/year ordering, e.g. "03/08/2026 11:58".
DATE_FORMAT = "%d/%m/%Y %H:%M"
REQUIRED_COLUMNS = {"Order", "Date", "Status", "Coupons Used", "Total"}


@anvil.server.callable
def import_orders_csv(csv_file):
    text = csv_file.get_bytes().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
    if missing_columns:
        return {
            "created": 0,
            "updated": 0,
            "errors": [
                {"row": 1, "reason": f"Missing column(s): {', '.join(sorted(missing_columns))}"}
            ],
        }

    created = 0
    updated = 0
    errors = []

    for row_number, row in enumerate(reader, start=2):
        order_number = (row.get("Order") or "").strip()
        if not order_number:
            errors.append({"row": row_number, "reason": "Missing order number"})
            continue

        try:
            order_date = datetime.strptime(row["Date"].strip(), DATE_FORMAT)
        except ValueError:
            errors.append({"row": row_number, "reason": f"Unrecognised date: {row['Date']!r}"})
            continue

        try:
            total = float(row["Total"].strip())
        except ValueError:
            errors.append({"row": row_number, "reason": f"Unrecognised total: {row['Total']!r}"})
            continue

        coupons = [c.strip() for c in (row.get("Coupons Used") or "").split(",") if c.strip()]
        status = (row.get("Status") or "").strip()

        existing = app_tables.orders.get(order_number=order_number)
        if existing:
            existing.update(order_date=order_date, status=status, total=total, coupons=coupons)
            updated += 1
        else:
            app_tables.orders.add_row(
                order_number=order_number,
                order_date=order_date,
                status=status,
                total=total,
                coupons=coupons,
            )
            created += 1

    return {"created": created, "updated": updated, "errors": errors}
