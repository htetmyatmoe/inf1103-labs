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


def save_inventory(inventory):
    """Save the current inventory to inventory.json."""
    print("Saving inventory...")
    with open(FILE_NAME, "w") as f:
        json.dump(inventory, f, indent=4)
    print(f"Inventory saved successfully to {FILE_NAME}.")


def display_all(inventory):
    """Display all products in inventory."""
    print("\nCurrent Inventory")
    if not inventory:
        print("No products available.")
        return
    for item in inventory:
        print(
            f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}"
        )


def add_product(inventory):
    """Prompt user and append a new product if the ID is unique."""
    print("\nAdd New Product")
    p_id = input("Product ID: ").strip()

    # Check if product ID already exists
    for item in inventory:
        if item["id"].lower() == p_id.lower():
            print(f"Error: Product ID '{p_id}' already exists! Cannot add duplicate product.")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid price or stock quantity.")
        return

    product = {"id": p_id, "name": name, "price": price, "stock": stock}
    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    """Update stock quantity for a given product ID."""
    print("\nUpdate Stock")
    p_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == p_id.lower():
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            try:
                new_stock = int(input("New Stock Quantity: "))
                item["stock"] = new_stock
                print("\nStock updated successfully!")
            except ValueError:
                print("Invalid stock value.")
            return

    print("Product not found.")


def search_product(inventory):
    """Search for a product by ID."""
    print("\nSearch Product")
    p_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == p_id.lower():
            print("\nProduct Found")
            print("---------------------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("---------------------------------------------")
            return

    print("\nProduct not found.")


def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()

    while True:
        print("\nMENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        choice = input("Enter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("\nSaving inventory before exit...")
            with open(FILE_NAME, "w") as f:
                json.dump(inventory, f, indent=4)
            print("Inventory saved successfully.\n")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()