# Setting counters to 0 at the start
inventory = 0
deliveries = 0
failed_attempts = 0
total_tax = 0
def get_valid_input():
    '''Function to get a valid input from the user. Returns the valid input, "quit" if the user wants to quit, or None if invalid.'''
    user_input = input("Enter stock quantity:")
    # Checks if user wants to quit program
    if user_input.lower() == "quit":
        print("Exiting program.")
        return "quit"

    # Validates that the input is valid and within the acceptable range of 0 to 500
    try:
        quantity = int(user_input)
    # Catches the ValueError if the input is not a valid integer
    except ValueError:
        print("Error: Invalid input. Please enter a valid stock quantity.")
        return None
    # Checks if the quantity is less than 0
    if quantity < 0:
        print("Error: Stock number cannot be negative")
        print("Please enter a valid stock quantity.")
        return None
    # Checks if quantity is more than 500 from the user input itself
    if quantity > 500:
        print("Alert: Stock number exceeds 500")
        print("Exiting loop.")
        return "quit"
    return quantity

def process_delivery(current_total, new_value):
    '''Function to process the delivery and update the inventory. Returns the updated inventory.'''
    return current_total + new_value

def calculate_tax(amount):
    '''Function to calculate tax based on the amount. Returns the calculated tax.'''
    tax_rate = 0.1
    return amount * tax_rate

def generate_report(total_units, failed_attempts):
    '''Function to generate a report of the total deliveries, total units in inventory, failed attempts, and total tax collected at the end.'''
    print(f"Total deliveries processed: {deliveries}")
    print(f"Total units in inventory: {total_units}")
    print(f"Number of failed attempts: {failed_attempts}")
    print(f"Total tax collected: {total_tax}")

# Creates loop to continuously prompt the user for input until they choose to quit or exceed the maximum stock limit
while True:
    # Calls the get_valid_input function to get a validated input from the user
    validated_input = get_valid_input()
    # Checks if the validated input is "quit" to exit the program and generate a report
    if validated_input == "quit":
        generate_report(inventory, failed_attempts)
        break
    # Checks if the validated input is None, indicating an invalid input, and increases the failed attempts counter
    if validated_input is None:
        failed_attempts += 1
        continue
    # Checks if the new inventory after adding the validated input would exceed 500, and if so, alerts the user and exits the program
    if inventory + validated_input > 500:
        print("Alert: Stock number exceeds 500")
        print("Exiting program.")
        generate_report(inventory, failed_attempts)
        break
    # If the validated input is valid and does not exceed the maximum stock limit, it processes the delivery, calculates the tax, 
    # updates the total tax collected, increases the "deliveries" counter, and prints the current inventory.
    inventory = process_delivery(inventory, validated_input)
    tax = calculate_tax(validated_input)
    total_tax += tax
    deliveries += 1
    print(f"Current inventory: {inventory}")