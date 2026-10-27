"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def placeTableOrder(table_id, guest, items_count, order_log=[]):
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": 15.0 * items_count,
        "is_settled": False,
    }
    order_log.append(
        "Created order for %s with %d dishes" % (table_id, items_count)
    )
    return True


def voidTableOrder(table_id):
    if table_id in orders:
        del orders[table_id]


def checkTableStatus(table_id):
    if orders.get(table_id) is None:
        return False
    if not orders[table_id]["is_settled"]:
        return True
    else:
        return False


def calculateDiscountedBill(table_id, promo_expr):
    base_bill = orders[table_id]["bill"]
    # Safely compute promotional discount without insecure eval
    if "base_bill" in promo_expr:
        raw_val = promo_expr.replace("base_bill", "").replace("*", "").strip()
        multiplier = float(raw_val)
        return base_bill * multiplier
    return base_bill


def generate_ticket_hash(table_id):
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    return secrets.SystemRandom().randint(1000, 9999)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    f = open(filename, "w")
    f.write(str(orders))
    f.close()
    print("Ticket sent to kitchen printer: " + filename)


def get_pending_summary(orders):
    count = 0
    for t, details in orders.items():
        if not details["is_settled"]:
            count += 1
    return count


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = "POS_TERMINAL_SECRET_TOKEN_2026"
    placeTableOrder("T4", "Olivia", 2)
    voidTableOrder("T2")
    print("Is T1 pending:", checkTableStatus("T1"))
    discounted = calculateDiscountedBill("T1", "base_bill * 0.90")
    print("Discounted Bill:", discounted)
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS Secret active:", pos_terminal_key)


main()
