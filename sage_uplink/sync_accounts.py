"""Run this script locally (not part of the Anvil app) to sync order-number ->
Sage account/customer-name lookups into the app.

Setup:
  pip install anvil-uplink
  Get your Uplink key from the Anvil IDE (Settings -> Uplink) and set it below
  or in the ANVIL_UPLINK_KEY environment variable.

Usage:
  python sync_accounts.py
"""

import os

import anvil.server

UPLINK_KEY = os.environ.get("ANVIL_UPLINK_KEY", "")
BATCH_SIZE = 500


def fetch_accounts_from_sage():
    """Return an iterable of dicts: {order_number, account_code, customer_name}.

    Replace this with your real Sage extraction (ODBC query, export file read,
    Sage API call, etc.). One row per WooCommerce order number that Sage can
    identify, mapped to the account that placed it.
    """
    raise NotImplementedError("Fill in fetch_accounts_from_sage() for your Sage setup")


def chunks(records, size):
    for i in range(0, len(records), size):
        yield records[i : i + size]


def main():
    anvil.server.connect(UPLINK_KEY)

    records = list(fetch_accounts_from_sage())
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
