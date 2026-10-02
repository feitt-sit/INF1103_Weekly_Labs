import json

# Setting counters to 0 at the start
inventory_file = "inventory_file.json"
def load_inventory():
    try:
        with open(inventory_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_inventory(inventory):
    with open(inventory_file, "w") as f:
        json.dump(inventory, f)

def add_product(inventory, name, quantity, price):
    product = {"name": name, "quantity": quantity, "price": price}
    inventory.append(product)
    return inventory

def update_stock(inventory, name, quantity):
    for product in inventory:
        if product["name"].lower() == name.lower():
            product["name"] = name
            product["quantity"] = quantity
            return True
    return False

def search_product(inventory, name):
    for product in inventory:
        if product["name"].lower() == name.lower():
            return product
    return None

def display_all(inventory):
    if not inventory:
        print("Inventory is empty.")
        return
    for product in inventory:
        print(f"Name: {product['name']}, Quantity: {product['quantity']}, Price: {product['price']}")

def display_menu():
    print("\nInventory Management System")
    print("1. Display all products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save inventory")
    print("6. Exit")

def main():
    inventory = load_inventory()
    # Creates loop to continuously prompt the user for input until they choose to quit or exceed the maximum stock limit
    while True:
        display_menu()
        user_input = input("Enter your choice:")
        if user_input == "1":
            display_all(inventory)
        elif user_input == "2":
            name = input("Enter product name:")
            try:
                quantity = int(input("Enter product quantity:"))
                price = float(input("Enter product price:"))
            except ValueError:
                print("Invalid input. Please enter numeric values for quantity and price.")
                continue
            inventory = add_product(inventory, name, quantity, price)
            print(f"Product {name} updated.")
        elif user_input == "3":
            name = input("Enter product name to update:")
            try:
                quantity = int(input("Enter new quantity:"))
            except ValueError:
                print("Invalid input. Please enter a numeric value for quantity.")
                continue
            if update_stock(inventory, name, quantity):
                print(f"Product {name} updated.")
            else:
                print(f"Product {name} not found.")
        elif user_input == "4":
            name = input("Enter product name to search:")
            product = search_product(inventory, name)
            if product:
                print(f"Found product: Name: {product['name']}, Quantity: {product['quantity']}, Price: {product['price']}")
            else:
                print(f"Product {name} not found.")
        elif user_input == "5":
            save_inventory(inventory)
            print("Inventory saved.")
        # Checks if the validated input is "6" to exit the program
        elif user_input == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()