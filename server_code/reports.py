from collections import defaultdict
from datetime import datetime

import anvil.server
from anvil.tables import app_tables

PAYOUT_PER_FIRST_TIME_USER = 3.00


@anvil.server.callable
def get_voucher_options():
    codes = set()
    for order in app_tables.orders.search():
        for coupon in order["coupons"] or []:
            if coupon.strip():
                codes.add(coupon.strip())
    return sorted(codes, key=str.lower)


@anvil.server.callable
def get_first_time_report(voucher_code):
    code_lower = voucher_code.strip().lower()
    sage_lookup = {row["order_number"]: row for row in app_tables.sage_order_accounts.search()}

    matching_orders = [
        order
        for order in app_tables.orders.search()
        if any(c.strip().lower() == code_lower for c in (order["coupons"] or []))
    ]
    matching_orders.sort(key=lambda order: order["order_date"])

    first_seen = {}
    unmatched_orders = []
    for order in matching_orders:
        account = sage_lookup.get(order["order_number"])
        if account is None:
            unmatched_orders.append(order["order_number"])
            continue

        account_code = account["account_code"]
        if account_code not in first_seen:
            first_seen[account_code] = {
                "account_code": account_code,
                "customer_name": account["customer_name"],
                "first_order_number": order["order_number"],
                "first_order_date": order["order_date"],
            }

    monthly_groups = defaultdict(list)
    for info in first_seen.values():
        monthly_groups[info["first_order_date"].strftime("%Y-%m")].append(info)

    monthly = []
    for month in sorted(monthly_groups):
        users = sorted(monthly_groups[month], key=lambda info: info["first_order_date"])
        for info in users:
            info["first_order_date"] = info["first_order_date"].strftime("%d %b %Y")

        count = len(users)
        total_owing = count * PAYOUT_PER_FIRST_TIME_USER
        monthly.append(
            {
                "month": month,
                "month_label": datetime.strptime(month, "%Y-%m").strftime("%B %Y"),
                "count": count,
                "total_owing_display": f"£{total_owing:.2f}",
                "users": users,
            }
        )

    return {
        "monthly": monthly,
        "unmatched_orders": sorted(set(unmatched_orders)),
    }
