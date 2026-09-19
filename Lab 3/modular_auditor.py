inventory = 0
failed_attempts = 0
total_tax = 0
def get_valid_input():
    user_input = input("Enter stock quantity:")
    if user_input.lower() == "quit":
        print("Exiting program.")
        return "quit"

    try:
        quantity = int(user_input)
    except ValueError:
        print("Error: Invalid input. Please enter a valid stock quantity.")
        return None
    if quantity < 0:
        print("Error: Stock number cannot be negative")
        print("Please enter a valid stock quantity.")
        return None
    if quantity > 500:
        print("Alert: Stock number exceeds 500")
        print("Exiting loop.")
        return "quit"
    return quantity

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    tax_rate = 0.1
    return amount * tax_rate

def generate_report(total_units, failed_attempts):
    print(f"Total deliveries processed: {total_units}")
    print(f"Number of failed attempts: {failed_attempts}")
    print(f"Total tax collected: {total_tax}")

while True:
    validated_input = get_valid_input()
    if validated_input == "quit":
        generate_report(inventory, failed_attempts)
        break
    if validated_input is None:
        failed_attempts += 1
        continue
    if inventory + validated_input > 500:
        generate_report(inventory, failed_attempts)
        break
    inventory = process_delivery(inventory, validated_input)
    tax = calculate_tax(validated_input)
    total_tax += tax
    print(f"Current inventory: {inventory}")