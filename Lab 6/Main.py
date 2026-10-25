import os
import json

from Product import Product
from Inventory import Inventory

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

# File handling
def load_inventory():
    inventory = Inventory()
    if not os.path.exists(file_name):
        return inventory
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
            print("Error loading inventory data. Starting with an empty inventory.")
            return inventory
    if isinstance(data, dict):
        records = []
        for product_data, info in data.items():
            info = dict(info)
            info.setdefault("product_id", product_data)
            records.append(info)
    else:
        records = data
    for item in records:
        try:
            product = Product(
                item.get("product_id", item.get("id")),
                item["name"],
                item["price"],
                item.get("stock", item.get("quantity", 0)),
                )
            inventory.add_product(product)
        except (KeyError, TypeError, ValueError):
            print(f"Skipping invalid record: {item}.")
    return inventory

def save_inventory(inventory):
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open(file_name, "w") as f:
        json.dump(data, f, indent = 4)
    print("Inventory saved successfully.")
# For inputs
def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_int(prompt, allow_negative = False):
    while True:
        try:
            value = int(input(prompt))
            if value < 0 and not allow_negative:
                print("Please enter a non-negative integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# For menu
def add_product_menu(inventory):
    product_id = input("Enter product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id):
        print(f"Product with ID {product_id} already exists.")
        return
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    price = get_float("Enter product price: ")
    stock = get_int("Enter product stock quantity: ")
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print(f"Product {name} added successfully.")

def update_stock_menu(inventory):
    product_id = input("Enter product ID to update stock: ").strip()
    product = inventory.search_product(product_id)
    if not product:
        print(f"No product found with ID {product_id}.")
        return
    new_stock = get_int(f"Enter quantity to add for {product.get_name()} (negative number to remove stock): ", allow_negative = True)
    if inventory.update_stock(product_id, new_stock):
        print(f"Stock for {product.get_name()} updated to {product.get_stock()}.")
    else:
        print(f"Failed to update stock for {product.get_name()}.")

def search_product_menu(inventory):
    product_to_search = input("Enter product ID or name to search: ").strip()
    product = inventory.search_product(product_to_search)
    results = [product] if product else inventory.search_by_name(product_to_search)
    if not results:
        print(f"No products found matching '{product_to_search}'.")
        return
    print("Search Results:")
    for product in results:
        product.display_information()

def display_inventory_menu():
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update product stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")

def main():
    inventory = load_inventory()
    while True:
        display_inventory_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()