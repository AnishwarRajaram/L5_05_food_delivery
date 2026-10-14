"""Manage food delivery orders, statuses, revenue, and backups."""

import json
from datetime import datetime

VALID_STATUSES = ("placed", "cooking", "out_for_delivery", "delivered")


def create_order(customer, items, orders, menu, order_history):
    """Create an order from menu items and add its ID to the history."""
    if not customer or not customer.strip():
        raise ValueError("Customer name must not be empty")
    if not items:
        raise ValueError("An order must contain at least one item")

    order_id = max(orders, default=0) + 1
    total = 0
    for i in items:
        if i not in menu:
            raise ValueError(f"Unknown menu item: {i}")
        total += menu[i]
    orders[order_id] = {
        "customer": customer,
        "items": items,
        "total": total,
        "status": "placed",
    }
    order_history.append(order_id)
    return order_id


def update_order_status(orders, order_id, status):
    """Update an order when its ID and status are valid."""
    if order_id not in orders or status not in VALID_STATUSES:
        return False
    orders[order_id]["status"] = status
    return True


def read_menu_config(file="menu.json"):
    """Read a menu config, using the built-in menu if it is unavailable."""
    try:
        with open(file, encoding="utf-8") as menu_file:
            return json.load(menu_file)
    except (OSError, json.JSONDecodeError):
        return {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}


def daily_revenue(orders):
    """Return the total value of delivered orders."""
    revenue = 0
    for o in orders:
        if orders[o]["status"] == "delivered":
            revenue = revenue + orders[o]["total"]
    return revenue


def backup_orders(orders, file="orders.json"):
    """Save orders as JSON without executing data during restore."""
    with open(file, "w", encoding="utf-8") as backup_file:
        json.dump(orders, backup_file)


def restore_orders(file="orders.json"):
    """Load orders from JSON and restore integer order IDs."""
    with open(file, encoding="utf-8") as backup_file:
        saved_orders = json.load(backup_file)
    return {int(order_id): order for order_id, order in saved_orders.items()}


def print_queue(orders):
    """Print each order and its current status."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(
            order_id,
            order["customer"],
            order["status"],
            order["total"],
        )


def main():
    """Run a short example of the order queue workflow."""
    menu = read_menu_config()
    orders = {}
    order_history = []
    a = create_order("Asha", ["pizza", "coke"], orders, menu, order_history)
    b = create_order("Ravi", ["burger", "fries"], orders, menu, order_history)
    c = create_order("Mina", ["fries"], orders, menu, order_history)
    for order_id, status in (
        (a, "delivered"),
        (b, "cooking"),
        (42, "delivered"),
        (c, "delivered"),
    ):
        if not update_order_status(orders, order_id, status):
            print(f"Could not update order {order_id} to {status!r}")
    print("Revenue today:", daily_revenue(orders))
    backup_orders(orders)
    orders = restore_orders()
    print_queue(orders)


if __name__ == "__main__":
    main()
