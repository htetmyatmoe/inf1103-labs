import json
import os

class Product:
    def __init__(self, id, name, price, stock):
        self._product_id = id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    def update_stock(self, quantity: int):
        """Updates stock safely with internal control."""
        new_stock = self._stock + quantity
        if new_stock < 0:
            print("Error: Stock cannot be negative!")
            return False
        self._stock = new_stock
        return True

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self):
        return {
            "id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }


class PhysicalProduct(Product):
    def __init__(self, id, name, price, stock, weight):
        super().__init__(id, name, price, stock)
        self._weight = float(weight)  # in kilograms

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self._weight} kg")


class DigitalProduct(Product):
    def __init__(self, id, name, price, stock, download_size):
        super().__init__(id, name, price, stock)
        self._download_size = float(download_size)  # in megabytes

    def display_information(self):
        super().display_information()
        print(f"    Download size: {self._download_size} MB")


class Inventory:
    def __init__(self):
        self._products = []

    def add_product(self, product: Product):
        self._products.append(product)

    def search_product(self, id):
        for product in self._products:
            if product._product_id == id:
                return product
        return None

    def display_all(self):
        if not self._products:
            print("Inventory is empty.")
            return
        for product in self._products:
            product.display_information()

    def save_to_file(self, filename="inventory.json"):
        data = [p.to_dict() for p in self._products]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Inventory saved successfully.")

    def load_from_file(self, filename="inventory.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            try:
                data = json.load(f)
                self._products = []
                for item in data:
                    product = Product(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"]
                    )
                    self._products.append(product)
                print("Inventory loaded successfully.")
            except json.JSONDecodeError:
                print("Error reading inventory file.")

def main():
    inventory = Inventory()
    inventory.load_from_file()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("(Type 'exit' at any prompt to cancel)")
            
            pid = input("Enter Product ID: ").strip()
            if pid.lower() == "exit":
                print("Cancelled adding product.")
                continue

            name = input("Enter Product Name: ").strip()
            if name.lower() == "exit":
                print("Cancelled adding product.")
                continue

            try:
                price_input = input("Enter Price: ").strip()
                if price_input.lower() == "exit":
                    print("Cancelled adding product.")
                    continue
                price = float(price_input)

                stock_input = input("Enter Stock Quantity: ").strip()
                if stock_input.lower() == "exit":
                    print("Cancelled adding product.")
                    continue
                stock = int(stock_input)

                new_product = Product(pid, name, price, stock)
                inventory.add_product(new_product)
                print("Product added successfully!")
            except ValueError:
                print("Invalid input for price or stock. Product creation cancelled.")

        elif choice == "3":
            print("(Type 'exit' at any prompt to cancel)")
            
            pid = input("Enter Product ID to update stock: ").strip()
            if pid.lower() == "exit":
                print("Cancelled stock update.")
                continue

            product = inventory.search_product(pid)
            if product:
                try:
                    qty_input = input("Enter quantity to add/subtract (e.g., 10 or -5): ").strip()
                    if qty_input.lower() == "exit":
                        print("Cancelled stock update.")
                        continue
                    
                    qty = int(qty_input)
                    if product.update_stock(qty):
                        print("Stock updated successfully.")
                except ValueError:
                    print("Invalid quantity format. Update cancelled.")
            else:
                print("Product not found.")
                
        elif choice == "4":
            pid = input("Enter Product ID to search: ").strip()
            product = inventory.search_product(pid)
            if product:
                product.display_information()
            else:
                print("Product not found.")

        elif choice == "5":
            inventory.save_to_file()

        elif choice == "6":
            inventory.save_to_file()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select between 1 and 6.")

if __name__ == "__main__":
    main()