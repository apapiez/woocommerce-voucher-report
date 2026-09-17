from collections import defaultdict
from datetime import datetime, timedelta

import anvil.server
from anvil.tables import app_tables

PAYOUT_PER_FIRST_TIME_USER = 3.00


def _orders_by_voucher():
    grouped = defaultdict(list)
    display_names = {}
    for order in app_tables.orders.search():
        for coupon in order["coupons"] or []:
            code = coupon.strip()
            if not code:
                continue
            key = code.lower()
            display_names.setdefault(key, code)
            grouped[key].append(order)

    for orders in grouped.values():
        orders.sort(key=lambda order: order["order_date"])

    return grouped, display_names


def _first_time_orders(orders, sage_lookup):
    first_seen = {}
    unmatched_orders = []
    for order in orders:
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

    return first_seen, unmatched_orders


@anvil.server.callable(require_user=True)
def get_voucher_summaries():
    grouped, display_names = _orders_by_voucher()
    sage_lookup = {row["order_number"]: row for row in app_tables.sage_order_accounts.search()}

    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    last_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    summaries = []
    for key, orders in grouped.items():
        first_seen, _unmatched = _first_time_orders(orders, sage_lookup)
        first_time_months = [info["first_order_date"].strftime("%Y-%m") for info in first_seen.values()]
        this_month_count = first_time_months.count(current_month)
        last_month_count = first_time_months.count(last_month)

        summaries.append(
            {
                "voucher_code": display_names[key],
                "total_purchases": len(orders),
                "total_payable_display": f"£{len(first_seen) * PAYOUT_PER_FIRST_TIME_USER:.2f}",
                "payable_last_month_display": f"£{last_month_count * PAYOUT_PER_FIRST_TIME_USER:.2f}",
                "payable_this_month_display": f"£{this_month_count * PAYOUT_PER_FIRST_TIME_USER:.2f}",
            }
        )

    summaries.sort(key=lambda summary: summary["voucher_code"].lower())
    return summaries


@anvil.server.callable(require_user=True)
def get_first_time_report(voucher_code):
    grouped, _display_names = _orders_by_voucher()
    orders = grouped.get(voucher_code.strip().lower(), [])
    sage_lookup = {row["order_number"]: row for row in app_tables.sage_order_accounts.search()}

    total_orders_by_month = defaultdict(int)
    for order in orders:
        total_orders_by_month[order["order_date"].strftime("%Y-%m")] += 1

    first_seen, unmatched_orders = _first_time_orders(orders, sage_lookup)

    first_time_by_month = defaultdict(list)
    for info in first_seen.values():
        first_time_by_month[info["first_order_date"].strftime("%Y-%m")].append(info)

    monthly = []
    for month in sorted(total_orders_by_month):
        users = sorted(first_time_by_month.get(month, []), key=lambda info: info["first_order_date"])
        for info in users:
            info["first_order_date"] = info["first_order_date"].strftime("%d %b %Y")

        first_time_count = len(users)
        total_owing = first_time_count * PAYOUT_PER_FIRST_TIME_USER
        monthly.append(
            {
                "month": month,
                "month_label": datetime.strptime(month, "%Y-%m").strftime("%B %Y"),
                "total_orders": total_orders_by_month[month],
                "first_time_count": first_time_count,
                "total_owing_display": f"£{total_owing:.2f}",
                "users": users,
            }
        )

    return {
        "monthly": monthly,
        "unmatched_orders": sorted(set(unmatched_orders)),
    }
