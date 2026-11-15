import gc
import weakref

from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from OrderLine import OrderLine

passed = 0
failed = 0


def check(description: str, condition: bool) -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"Passed: {description}")
    else:
        failed += 1
        print(f"Failed: {description}")


def heading(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


heading("Section 2: Association - Supplier and Product")
supplier = Supplier("S001", "TechWorld Supplies", "sales@techworld.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
ebook = DigitalProduct("D001", "Python E-book", 19.90, 100, supplier, 12.5)

print("Supplier information displayed through each Product:")
for product in [laptop, ebook]:
    print(f"- {product.get_name()}:")
    product.get_supplier().display_information()

check("Product stores a reference to the Supplier object (not just a name or ID)",
      laptop.get_supplier() is supplier)
check("Both products refer to the same Supplier object",
      laptop.get_supplier() is ebook.get_supplier())
check("Supplier and Products are separate objects",
      supplier is not laptop and supplier is not ebook)

print("\nPredict first: delete the 'supplier' variable, then display again")
del supplier
print(f"Laptop supplier after del: {laptop.get_supplier().get_name()}")
print(f"E-book supplier after del: {ebook.get_supplier().get_name()}")
check("Products can still display their supplier after 'del supplier'",
      laptop.get_supplier().get_name() == "TechWorld Supplies")
print("  (del only removes the variable name. The Supplier object stays alive because"
      " each Product still holds a reference to it.)")


heading("Section 3: Aggregation - Inventory and Product")
supplier_b = Supplier("S002", "Global Gadgets", "hello@globalgadgets.com")
mouse = PhysicalProduct("P002", "Mouse", 25.00, 40, supplier_b, 0.1)   # created BEFORE any inventory
inventory_a = Inventory()
inventory_b = Inventory()

check("Product added to Inventory A", inventory_a.add_product(mouse))
check("Inventory A finds the product", inventory_a.find_product("P002") is mouse)

print("\nPredict first: remove the product from Inventory A - does it still work?")
removed = inventory_a.remove_product("P002")
check("remove_product returns the same Product object", removed is mouse)
check("Inventory A no longer contains it", inventory_a.find_product("P002") is None)
check("Inventory A is now empty", inventory_a.get_all_products() == [])
check("Removed product can still be used (update_stock works)", mouse.update_stock(-5))
print("Removed product still displays:")
mouse.display_information()

check("Same product object added to Inventory B", inventory_b.add_product(mouse))
check("Inventory B holds the very same object", inventory_b.find_product("P002") is mouse)
check("Stock change made while outside any inventory is kept", mouse.get_stock() == 35)


heading("Section 4: Composition - Order and OrderLine")
order1 = Order("ORD001")
order1.add_order_line(laptop, 2)
order1.add_order_line(ebook, 3)
order1.add_order_line(mouse, 1)
order1.display_order()
expected_total = 1200.00 * 2 + 19.90 * 3 + 25.00 * 1
check(f"Order total is calculated from its OrderLines (${expected_total:.2f})",
      abs(order1.calculate_total() - expected_total) < 1e-9)
check("Order created its own OrderLine objects",
      all(isinstance(line, OrderLine) for line in order1.get_order_lines()))
check("OrderLine refers to the Product but does not copy it",
      order1.get_order_lines()[0].get_product() is laptop)

print("\nPredict first: add the same Product to a second Order")
order2 = Order("ORD002")
order2.add_order_line(laptop, 1)
line_in_order1 = order1.get_order_lines()[0]
line_in_order2 = order2.get_order_lines()[0]
print(f"id of Laptop via order1 line: {id(line_in_order1.get_product())}")
print(f"id of Laptop via order2 line: {id(line_in_order2.get_product())}")
print(f"id of order1 line: {id(line_in_order1)}")
print(f"id of order2 line: {id(line_in_order2)}")
check("2 OrderLine objects: each Order created its own line",
      line_in_order1 is not line_in_order2)
check("1 Product object: both lines refer to the same Laptop",
      line_in_order1.get_product() is line_in_order2.get_product() is laptop)

print("\nRemove an order line through the Order")
check("remove_order_line('D001') succeeds", order1.remove_order_line("D001"))
check("Order now has 2 lines", len(order1.get_order_lines()) == 2)
check("Total updated after removal",
      abs(order1.calculate_total() - (1200.00 * 2 + 25.00)) < 1e-9)
check("Removing an order line does not touch the Product", ebook.get_stock() == 100)

print("\nRemove the whole Order: its OrderLines go with it")
line_ref = weakref.ref(order1.get_order_lines()[0])
del line_in_order1
del order1
gc.collect()
check("OrderLine no longer exists after its Order is removed", line_ref() is None)
check("The Product it referred to still exists", laptop.get_name() == "Laptop")
check("get_order_lines() returns a copy, so the Order's own list cannot be changed",
      order2.get_order_lines() is not order2.get_order_lines())


heading("Section 6: Liskov Substitution Principle")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("show_product_details() with a PhysicalProduct:")
show_product_details(laptop)
print("\nshow_product_details() with a DigitalProduct:")
show_product_details(ebook)

lsp_inventory = Inventory()
check("Both types can be added to the same Inventory",
      lsp_inventory.add_product(laptop) and lsp_inventory.add_product(ebook))
check("find_product works for both types",
      lsp_inventory.find_product("P001") is laptop and lsp_inventory.find_product("D001") is ebook)

print("\nExpectation set by Product.update_stock(): returns True and changes stock for a"
      " valid change; returns False and leaves stock unchanged if it would go below zero.")
for product in lsp_inventory.get_all_products():
    before = product.get_stock()
    ok_add = lsp_inventory.update_stock(product.get_product_id(), 5)
    ok_too_much = lsp_inventory.update_stock(product.get_product_id(), -10_000)
    check(f"{type(product).__name__}: +5 returns True and stock becomes {before + 5}",
          ok_add is True and product.get_stock() == before + 5)
    check(f"{type(product).__name__}: -10000 returns False and stock stays {before + 5}",
          ok_too_much is False and product.get_stock() == before + 5)

print("\nDiagnose: the teammate's DigitalProduct that raises NotImplementedError")


class BadDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> None:  # type: ignore[override]
        raise NotImplementedError("Digital products have no stock")


bad = BadDigitalProduct("D999", "Bad Download", 5.00, 10, laptop.get_supplier(), 1.0)
bad_inventory = Inventory()
bad_inventory.add_product(bad)
try:
    bad_inventory.update_stock("D999", 1)
    crashed = False
except NotImplementedError as error:
    crashed = True
    print(f"  Inventory.update_stock crashed: NotImplementedError: {error}")
check("Substituting the bad subclass breaks Inventory (LSP violation)", crashed)


heading("Section 7: Polymorphism through Product references")
poly_inventory = Inventory()
poly_inventory.add_product(PhysicalProduct("P100", "Guitar", 350.00, 4, supplier_b, 3.2))
poly_inventory.add_product(DigitalProduct("D100", "Music Software", 99.00, 50, supplier_b, 850.0))

print("Predict first: get_fulfilment_info() for each product")
results: list[str] = []
for product in poly_inventory.get_all_products():   # one loop, no isinstance()
    product.display_information()
    info = product.get_fulfilment_info()
    results.append(info)
    print(info)
    print()
check("Guitar (physical) says it requires shipping",
      results[0] == "Requires physical shipping. Weight: 3.2 kg")
check("Music Software (digital) says it is a digital download",
      results[1] == "Digital download. Size: 850.0 MB")


heading("Section 9: Abstract class check")
try:
    Product("X", "Generic", 1.0, 1, supplier_b)  # type: ignore[abstract]
    blocked = False
except TypeError as error:
    blocked = True
    print(f"  Product(...) refused: {error}")
check("Abstract Product cannot be instantiated", blocked)

print("\n" + "=" * 70)
print(f"RESULT: {passed} passed, {failed} failed")
print("=" * 70)
