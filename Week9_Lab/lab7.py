import json
import os
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, id, name, price, stock):
        self._product_id = id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    def update_stock(self, quantity: int):
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

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    BASE_SHIPPING = 5.00   # flat fee in dollars
    RATE_PER_KG = 2.00     # extra dollars per kilogram

    def __init__(self, id, name, price, stock, weight):
        super().__init__(id, name, price, stock)
        self._weight = float(weight)  # in kilograms

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self._weight} kg")

    def get_fulfilment_info(self):
        return f"{self.name} requires physical shipping ({self._weight} kg)."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING + self._weight * self.RATE_PER_KG

    def to_dict(self):
        data = super().to_dict()      # id, name, price, stock from Product
        data["type"] = "physical"     # tells load_from_file which class to rebuild
        data["weight"] = self._weight
        return data


class DigitalProduct(Product):
    def __init__(self, id, name, price, stock, download_size):
        super().__init__(id, name, price, stock)
        self._download_size = float(download_size)  # in megabytes

    def display_information(self):
        super().display_information()
        print(f"    Download size: {self._download_size} MB")

    def get_fulfilment_info(self):
        return f"{self.name} is delivered digitally via download link ({self._download_size} MB)."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data


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
                    product_type = item.get("type", "physical")
                    if product_type == "digital":
                        product = DigitalProduct(
                            item["id"], item["name"], item["price"], item["stock"],
                            item.get("download_size", 0.0)
                        )
                    else:
                        product = PhysicalProduct(
                            item["id"], item["name"], item["price"], item["stock"],
                            item.get("weight", 0.0)
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

            product_type = input("Product type - (P)hysical or (D)igital: ").strip().lower()
            if product_type == "exit":
                print("Cancelled adding product.")
                continue
            if product_type not in ("p", "d", "physical", "digital"):
                print("Invalid product type. Product creation cancelled.")
                continue
            is_physical = product_type in ("p", "physical")

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

                if is_physical:
                    extra_input = input("Enter Weight (kg): ").strip()
                else:
                    extra_input = input("Enter Download Size (MB): ").strip()
                if extra_input.lower() == "exit":
                    print("Cancelled adding product.")
                    continue
                extra = float(extra_input)

                if is_physical:
                    new_product = PhysicalProduct(pid, name, price, stock, extra)
                else:
                    new_product = DigitalProduct(pid, name, price, stock, extra)
                inventory.add_product(new_product)
                print("Product added successfully!")
                print(new_product.get_fulfilment_info())
            except ValueError:
                print("Invalid number entered. Product creation cancelled.")

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