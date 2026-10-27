"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def place_table_order(table_id, guest, items_count, order_log=None):
    """Place a new dining order for an active table."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": 15.0 * items_count,
        "is_settled": False,
    }
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Void and remove an active order for a given table."""
    if table_id in orders:
        del orders[table_id]


def check_table_status(table_id):
    """Check whether a table order exists and is pending settlement."""
    if orders.get(table_id) is None:
        return False
    return not orders[table_id]["is_settled"]


def calculate_discounted_bill(table_id, promo_expr):
    """Safely calculate discounted bill total from promotional expression."""
    base_bill = orders[table_id]["bill"]
    if "base_bill" in promo_expr:
        raw_val = promo_expr.replace("base_bill", "").replace("*", "").strip()
        multiplier = float(raw_val)
        return base_bill * multiplier
    return base_bill


def generate_ticket_hash(table_id):
    """Generate SHA-256 digital hash verification token for kitchen ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Generate cryptographically secure 4-digit POS authorization PIN."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Export current dining orders to kitchen printer file."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(orders))
    print("Ticket sent to kitchen printer: " + filename)


def get_pending_summary(orders_dict):
    """Count the total number of unsettled pending table orders."""
    return sum(
        1 for details in orders_dict.values() if not details["is_settled"]
    )


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = "POS_TERMINAL_SECRET_TOKEN_2026"
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    discounted = calculate_discounted_bill("T1", "base_bill * 0.90")
    print("Discounted Bill:", discounted)
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS Secret active:", pos_terminal_key)


if __name__ == "__main__":
    main()
