def get_valid_input():
    """Prompts the user for input and validates it."""
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

    if user_input.lower() == 'quit':
        return 'quit'

    if not user_input.isdigit():
        print("Invalid input. Please enter a valid number.")
        return None

    value = int(user_input)
    if value < 0:
        print("Invalid input. Quantity cannot be negative.")
        return None

    return value


def process_delivery(current_total, new_value):
    """Calculates and returns the new inventory total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates and returns a 10% tax for the delivery."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, total_deliveries):
    """Prints the final summary report."""
    print("\n--- Final Inventory Audit Report ---")
    print(f"Total Inventory Units     : {total_units}")
    print(f"Total Deliveries Processed: {total_deliveries}")
    print(f"Number of Failed Entries  : {failed_attempts}")
    print("------------------------------------")


def main():
    inventory_count = 0
    failed_entries = 0
    deliveries_processed = 0

    while True:
        entry = get_valid_input()

        if entry == 'quit':
            break

        if entry is None:
            failed_entries += 1
            continue

        # Check if adding the new entry exceeds capacity
        if inventory_count + entry > 500:
            print("Warning: Inventory count exceeds 500. Please check the stock levels.")
            failed_entries += 1
            break

        # Process valid delivery
        inventory_count = process_delivery(inventory_count, entry)
        tax = calculate_tax(entry)
        deliveries_processed += 1

        print(f"Added: {entry} units | Delivery Tax (10%): {tax:.2f} | Running Total: {inventory_count}")

    generate_report(inventory_count, failed_entries, deliveries_processed)


if __name__ == "__main__":
    main()