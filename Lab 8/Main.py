import os
import json

from Product import Product
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Supplier import Supplier
from Order import Order

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

# File handling
def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    if not os.path.exists(file_name):
       return inventory, suppliers
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
            print("Error loading inventory data. Starting with an empty inventory.")
            return inventory, suppliers
    if isinstance(data, dict):
           supplier_records = data.get("suppliers", [])
           records = data.get("products", [])
    else:                                    # old Lab 7 file: just a list of products
           supplier_records = []
           records = data

    for item in supplier_records:
        supplier = Supplier(item["supplier_id"], item["name"], item["contact_email"])
        suppliers[supplier.get_supplier_id()] = supplier
        # Old products have no supplier, so give them a placeholder one
    unknown = suppliers.setdefault("S000", Supplier("S000", "Unknown supplier", "-"))

    for item in records:
        try:
            supplier = suppliers.get(item.get("supplier_id"), unknown)
            if item.get("type") == "digital" or item.get("download_size") is not None:
                product = DigitalProduct(
                    item.get("product_id", item.get("id")),
                    item["name"],
                    item["price"],
                    item.get("stock", item.get("quantity", 0)),
                    supplier,
                    item.get("download_size", 0.0)
                )
            else:
                product = PhysicalProduct(
                    item.get("product_id", item.get("id")),
                    item["name"],
                    item["price"],
                    item.get("stock", item.get("quantity", 0)),
                    supplier,
                    item.get("weight", 0.0)
                )
            inventory.add_product(product)
        except (KeyError, TypeError, ValueError):
            print(f"Skipping invalid record: {item}.")
    return inventory, suppliers

def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    data = {
        "suppliers": [supplier.to_dict() for supplier in suppliers.values()],
        "products": [product.to_dict() for product in inventory.get_all_products()]
    }
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    print("Inventory saved successfully.")
# For inputs
def get_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_int(prompt: str, allow_negative: bool = False) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value < 0 and not allow_negative:
                print("Please enter a non-negative integer.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    supplier_id = input("Enter supplier ID: ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        print(f"Using existing supplier: {suppliers[supplier_id].get_name()}")
        return suppliers[supplier_id]
    name = input("New supplier - enter supplier name: ").strip()
    if not name:
        print("Supplier name cannot be empty.")
        return None
    contact_email = input("Enter supplier contact email: ").strip()
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers[supplier_id] = supplier            # remember it for next time
    return supplier
# For menu
def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    product_id = input("Enter product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.find_product(product_id):
        print(f"Product with ID {product_id} already exists.")
        return
    name = input("Enter product name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    product_type = input("Enter product type (physical/digital): ").strip().lower()
    if product_type not in ("physical", "digital"):
        print("Invalid product type. Please enter 'physical' or 'digital'.")
        return
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return
    if product_type == "physical":
        weight = get_float("Enter product weight (kg): ")
        price = get_float("Enter product price: ")
        stock = get_int("Enter product stock quantity: ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_float("Enter download size (MB): ")
        price = get_float("Enter product price: ")
        stock = get_int("Enter product stock quantity: ")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    inventory.add_product(product)
    print(f"Product {name} added successfully.")

def update_stock_menu(inventory: Inventory) -> None:
    product_id = input("Enter product ID to update stock: ").strip()
    product = inventory.find_product(product_id)
    if not product:
        print(f"No product found with ID {product_id}.")
        return
    new_stock = get_int(f"Enter quantity to add for {product.get_name()} (negative number to remove stock): ", allow_negative = True)
    if inventory.update_stock(product_id, new_stock):
        print(f"Stock for {product.get_name()} updated to {product.get_stock()}.")
    else:
        print(f"Failed to update stock for {product.get_name()}.")

def search_product_menu(inventory: Inventory) -> None:
    product_to_search = input("Enter product ID or name to search: ").strip()
    product = inventory.find_product(product_to_search)
    results = [product] if product else inventory.search_by_name(product_to_search)
    if not results:
        print(f"No products found matching '{product_to_search}'.")
        return
    print("Search Results:")
    for product in results:
        product.display_information()
        print(product.get_fulfilment_info())

def display_inventory_menu() -> None:
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update product stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")

def main() -> None:
    inventory, suppliers = load_inventory()
    while True:
        display_inventory_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory, suppliers)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(inventory, suppliers)
        elif choice == "6":
            save_inventory(inventory, suppliers)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()