import os

FILE_NAME = "inventory.txt"


def load_inventory(filepath):
    """
    Reads previously saved orders from the file into a Python list.
    If the file does not exist, starts with an empty list.
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
                        order_id = int(parts[0])
                        product_name = parts[1]
                        qty = int(parts[2])
                        orders.append((order_id, product_name, qty))
    except IOError as e:
        print(f"Error loading file: {e}")

    return orders


def main():
    orders = load_inventory(FILE_NAME)
    print("Current Orders:\n")
    if orders:
        for order_id, product, qty in orders:
            print(f"{order_id}, {product}, {qty}")
    else:
        print("No prior orders found.")


if __name__ == "__main__":
    main()