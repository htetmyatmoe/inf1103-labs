import os

FILE_NAME = "inventory.txt"


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
    product_name = input("Enter Product Name (or 'quit' to exit): ").strip()
    if product_name.lower() == "quit":
        return "quit", None

    qty_input = input("Enter Quantity: ").strip()
    if not qty_input.isdigit() or int(qty_input) <= 0:
        print("Invalid quantity. Please enter a positive integer.")
        return None, None

    return product_name, int(qty_input)


def process_delivery(orders_list, product_name, quantity):
    if orders_list:
        next_id = orders_list[-1][0] + 1
    else:
        next_id = 1001

    new_order = (next_id, product_name, quantity)
    orders_list.append(new_order)
    return new_order


def calculate_tax(amount):
    return amount * 0.10


def save_inventory(filepath, orders_list):
    try:
        with open(filepath, "w") as file:
            for order_id, product_name, qty in orders_list:
                file.write(f"{order_id}, {product_name}, {qty}\n")
        print(f"Order successfully saved to {filepath}\n")
    except IOError as e:
        print(f"Error saving file: {e}")


def generate_report(orders_list, failed_attempts):
    total_transactions = len(orders_list)
    total_units = sum(qty for _, _, qty in orders_list)
    total_tax = sum(calculate_tax(qty) for _, _, qty in orders_list)

    print("=== Audit Report ===")
    print(f"Total Transactions Recorded: {total_transactions}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Tax (10% on units): {total_tax:.2f}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    orders = load_inventory(FILE_NAME)
    failed_attempts = 0

    print("Current Orders:")
    if orders:
        for order_id, product, qty in orders:
            print(f"{order_id}, {product}, {qty}")
    else:
        print("No prior orders found.")

    print("---------------------------------")

    while True:
        product_name, quantity = get_valid_input()

        if product_name == "quit":
            break

        if product_name is None or quantity is None:
            failed_attempts += 1
            continue

        new_order = process_delivery(orders, product_name, quantity)
        tax = calculate_tax(quantity)

        print("\nNew Order Added:")
        print(f"{new_order[0]}, {new_order[1]}, {new_order[2]} (Tax: {tax:.2f})\n")

    save_inventory(FILE_NAME, orders)
    generate_report(orders, failed_attempts)


if __name__ == "__main__":
    main()