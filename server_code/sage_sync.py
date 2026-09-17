import anvil.server
from anvil.tables import app_tables


@anvil.server.callable
def upsert_sage_accounts(records):
    """Called from the local Sage Uplink script to sync order-number -> account lookups."""
    created = 0
    updated = 0
    skipped = []

    for index, record in enumerate(records):
        order_number = str(record.get("order_number") or "").strip()
        account_code = str(record.get("account_code") or "").strip()
        customer_name = str(record.get("customer_name") or "").strip()

        if not order_number or not account_code:
            skipped.append({"index": index, "reason": "Missing order_number or account_code"})
            continue

        existing = app_tables.sage_order_accounts.get(order_number=order_number)
        if existing:
            existing.update(account_code=account_code, customer_name=customer_name)
            updated += 1
        else:
            app_tables.sage_order_accounts.add_row(
                order_number=order_number,
                account_code=account_code,
                customer_name=customer_name,
            )
            created += 1

    return {"created": created, "updated": updated, "skipped": skipped}
