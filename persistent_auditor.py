import os

FILE_NAME = "orders.txt"


def load_inventory(filepath):
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
                        order_id = int(parts[0])
                        product_name = parts[1]
                        qty = int(parts[2])
                        orders.append((order_id, product_name, qty))
    except IOError as e:
        print(f"Error loading file: {e}")

    return orders


def get_valid_input():
    """Prompts for product name and valid quantity."""
    product_name = input("Enter Product Name: ").strip()

    while True:
        qty_input = input("Enter Quantity: ").strip()
        if qty_input.isdigit() and int(qty_input) > 0:
            return product_name, int(qty_input)
        print("Invalid quantity. Please enter a positive integer.")


def process_delivery(orders_list, product_name, quantity):
    """
    Auto-increments Order ID, updates the tracking list,
    and returns the new entry tuple.
    """
    if orders_list:
        next_id = orders_list[-1][0] + 1
    else:
        next_id = 1001

    new_order = (next_id, product_name, quantity)
    orders_list.append(new_order)
    return new_order


def main():
    orders = load_inventory(FILE_NAME)

    print("Current Orders:\n")
    if orders:
        for order_id, product, qty in orders:
            print(f"{order_id}, {product}, {qty}")
    else:
        print("No prior orders found.")

    print()

    # Input handling and list tracking
    product_name, quantity = get_valid_input()
    new_order = process_delivery(orders, product_name, quantity)

    print("\nNew Order Added:")
    print(f"{new_order[0]},{new_order[1]},{new_order[2]}")


if __name__ == "__main__":
    main()