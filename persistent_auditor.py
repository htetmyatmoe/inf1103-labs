import os

FILE_NAME = "orders.txt"


def load_inventory(filepath):
    """
    Phase A: Reads previously saved orders from file into a list.
    """
    orders = []
    if not os.path.exists(filepath):
        return orders

    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) == 3:
                        orders.append((int(parts[0]), parts[1], int(parts[2])))
    except IOError as e:
        print(f"Error loading file: {e}")

    return orders


def get_valid_input():
    """
    Phase B: Prompts for product name (or 'quit') and a valid positive quantity.
    """
    product_name = input("Enter Product Name (or type 'quit' to exit): ").strip()
    if product_name.lower() == "quit":
        return "quit", None

    while True:
        qty_input = input("Enter Quantity: ").strip()
        if qty_input.isdigit() and int(qty_input) > 0:
            return product_name, int(qty_input)
        print("Invalid quantity. Please enter a positive integer.")


def process_delivery(orders_list, product_name, quantity):
    """
    Phase B: Increments ID, appends to the history list, and returns the new order.
    """
    if orders_list:
        next_id = orders_list[-1][0] + 1
    else:
        next_id = 1001

    new_order = (next_id, product_name, quantity)
    orders_list.append(new_order)
    return new_order


def main():
    # 1. Load initial history
    orders = load_inventory(FILE_NAME)

    print("Current Orders:\n")
    if orders:
        for order_id, product, qty in orders:
            print(f"{order_id}, {product}, {qty}")
    else:
        print("No prior orders found.")
    print()

    # 2. Continuous entry loop
    while True:
        product_name, quantity = get_valid_input()

        if product_name == "quit":
            break

        new_order = process_delivery(orders, product_name, quantity)
        print("\nNew Order Added:")
        print(f"{new_order[0]},{new_order[1]},{new_order[2]}\n")

    print(f"\nSession finished. Total orders in history: {len(orders)}")


if __name__ == "__main__":
    main()