#!/usr/bin/env python3
"""Shopping cart example with improved code quality and security."""

import hashlib
import os
import secrets

cart_items = {
    "ITEM1": {"name": "Wireless Mouse", "price": 25.0, "qty": 2},
    "ITEM2": {"name": "Mechanical Keyboard", "price": 80.0, "qty": 1},
    "ITEM3": {"name": "USB-C Hub", "price": 45.0, "qty": 3},
}


def add_item_to_cart(item_id, name, price, qty=1, audit_log=None):
    """Add a new item to the cart and record the operation."""

    if audit_log is None:
        audit_log = []

    if item_id in cart_items:
        return False

    cart_items[item_id] = {"name": name, "price": price, "qty": qty}

    audit_log.append(f"Added {item_id} with price {price:.2f}")
    return True


def remove_item_from_cart(item_id):
    """Remove an item from the cart if it exists."""
    try:
        del cart_items[item_id]
        return True
    except KeyError:
        return False


def check_cart_status(item_id):
    """Return whether an item exists in the cart with positive quantity."""
    item = cart_items.get(item_id)
    return item is not None and item["qty"] > 0


def calculate_discounted_total(item_id, discount_rate=0.10):
    """Calculate an item's price after applying a discount rate."""
    if item_id not in cart_items:
        raise KeyError(f"Item {item_id} was not found in the cart.")

    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_price = cart_items[item_id]["price"]
    return base_price * (1.0 - discount_rate)


def generate_item_hash(item_id):
    """Generate a SHA-256 hash for an item identifier."""
    return hashlib.sha256(item_id.encode("utf-8")).hexdigest()


def generate_checkout_pin():
    """Generate a cryptographically secure four-digit PIN."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_cart_receipt(filename="receipt.txt"):
    """Write cart contents to a receipt file."""
    with open(filename, "w", encoding="utf-8") as receipt_file:
        for item_id, details in cart_items.items():
            receipt_file.write(
                f"{item_id}: {details['name']}, "
                f"price={details['price']:.2f}, qty={details['qty']}\n"
            )

    print(f"Receipt saved to: {filename}")


def get_cart_summary(items):
    """Return the total quantity of items with positive quantities."""
    total_quantity = 0

    for details in items.values():
        if details["qty"] > 0:
            total_quantity += details["qty"]

    return total_quantity


def main():
    """Run the shopping cart demonstration."""
    payment_gateway_key = os.getenv("STRIPE_SECRET_KEY")

    add_item_to_cart("ITEM4", "Monitor Stand", 35.0, 1)
    remove_item_from_cart("ITEM2")

    print("Is ITEM1 in cart:", check_cart_status("ITEM1"))
    print("Discounted Price:", calculate_discounted_total("ITEM1"))
    print("Item Hash:", generate_item_hash("ITEM1"))
    print("Checkout PIN:", generate_checkout_pin())

    export_cart_receipt()
    print("Total items:", get_cart_summary(cart_items))
    print("Gateway secret configured:", bool(payment_gateway_key))


if __name__ == "__main__":
    main()
