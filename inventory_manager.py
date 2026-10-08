import json
import os

FILE_NAME = "inventory.json"


def load_inventory():
    """Check whether inventory.json exists. Load if found, otherwise start empty."""
    if os.path.exists(FILE_NAME):
        print(f"{FILE_NAME} found.")
        try:
            with open(FILE_NAME, "r") as f:
                data = json.load(f)
                print("Inventory loaded successfully.")
                return data
        except (json.JSONDecodeError, IOError):
            print("Error reading file. Starting with an empty inventory.")
            return []
    else:
        print(f"{FILE_NAME} not found. Starting with an empty inventory.")
        return []


def display_all(inventory):
    print("\nCurrent Inventory")
    if not inventory:
        print("No products available.")
        return
    for item in inventory:
        print(
            f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}"
        )


def add_product(inventory):
    print("\nAdd New Product")
    p_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input.")
        return

    product = {"id": p_id, "name": name, "price": price, "stock": stock}
    inventory.append(product)
    print("Product added successfully!")


def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()
    display_all(inventory)


if __name__ == "__main__":
    main()