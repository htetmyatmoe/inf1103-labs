inventory_count = 0 
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or type 'quit' to exit): ")

    if user_input.lower() == 'quit':
        break
    elif not user_input.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue
    elif int(user_input) < 0:
        print("Invalid input. Quantity cannot be negative.")
        failed_entries += 1
        continue

    inventory_count += int(user_input)

    if inventory_count > 500:
        print("Warning: Inventory count exceeds 500. Please check the stock levels.")
        failed_entries += 1
        break

print(f"Current inventory count: {inventory_count}")
print(f"Failed entries: {failed_entries}")
