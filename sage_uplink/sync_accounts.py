"""Run this script locally (not part of the Anvil app) to sync order-number ->
Sage account/customer-name lookups into the app, from a Sage CSV export with
columns: Date, Name, A/C, Customer Order No.

Setup:
  pip install anvil-uplink
  Get your Uplink key from the Anvil IDE (Settings -> Uplink) and set it below
  or in the ANVIL_UPLINK_KEY environment variable.

Usage:
  python sync_accounts.py path/to/sage_export.csv
"""

import csv
import os
import sys

import anvil.server

UPLINK_KEY = os.environ.get("ANVIL_UPLINK_KEY", "")
BATCH_SIZE = 500


def read_accounts_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_number = (row.get("Customer Order No") or "").strip()
            account_code = (row.get("A/C") or "").strip()
            customer_name = (row.get("Name") or "").strip()
            if not order_number or not account_code:
                continue
            yield {
                "order_number": order_number,
                "account_code": account_code,
                "customer_name": customer_name,
            }


def chunks(records, size):
    for i in range(0, len(records), size):
        yield records[i : i + size]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python sync_accounts.py path/to/sage_export.csv")

    anvil.server.connect(UPLINK_KEY)

    records = list(read_accounts_csv(sys.argv[1]))
    created = updated = 0
    skipped = []

    for batch in chunks(records, BATCH_SIZE):
        result = anvil.server.call("upsert_sage_accounts", batch)
        created += result["created"]
        updated += result["updated"]
        skipped.extend(result["skipped"])

    print(f"Created {created}, updated {updated}, skipped {len(skipped)}")
    for entry in skipped:
        print(f"  skipped: {entry}")


if __name__ == "__main__":
    main()
