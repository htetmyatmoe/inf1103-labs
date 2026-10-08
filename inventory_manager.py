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
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = {"id": p_id, "name": name, "price": price, "stock": stock}
    inventory.append(product)
    print("Product added successfully!")


def main():
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]

    print("INVENTORY MANAGEMENT SYSTEM")
    display_all(inventory)

    # Test adding a product
    add_product(inventory)
    display_all(inventory)


if __name__ == "__main__":
    main()