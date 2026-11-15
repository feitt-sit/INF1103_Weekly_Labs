"""Automated tests for INF1103 Lab 9.

Run from the Lab 9 folder (the one containing Main.py):
    python -m unittest discover -s tests -v
"""
import ast
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from Supplier import Supplier
from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from OrderLine import OrderLine
from ProductFactory import ProductFactory
from DiscountStrategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                              BulkDiscount, StudentDiscount)
from Main import get_positive_float, load_products

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S1", "Test Supplier", "test@example.com")
    desk = ProductFactory.create("physical", "P1", "Desk", 125.0, 10, supplier, weight=5.0)
    order = Order("O1", discount)
    order.add_order_line(desk, 2)          # 2 x 125.00 = 250.00
    return order


class TestStrategyPattern(unittest.TestCase):
    def test_order_without_discount_uses_no_discount(self):
        self.assertEqual(make_order_totalling_250().calculate_total(), 250.0)

    def test_bulk_discount_applies_at_threshold(self):
        self.assertEqual(make_order_totalling_250(BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_bulk_discount_not_applied_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150.0), 150.0)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(250.0), 237.5)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self):
        class FixedDiscount(DiscountStrategy):      # a brand-new strategy, defined only here
            def apply(self, total: float) -> float:
                return total - 50
        self.assertEqual(make_order_totalling_250(FixedDiscount()).calculate_total(), 200.0)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        self.assertAlmostEqual(make_order_totalling_250(shared).calculate_total(), 225.0)
        self.assertAlmostEqual(make_order_totalling_250(shared).calculate_total(), 225.0)

    def test_order_contains_no_discount_if_elif_logic(self):
        with open(os.path.join(PROJECT_DIR, "Order.py")) as f:
            source = f.read()
        for text in ("discount_type", "PercentageDiscount", "BulkDiscount", "elif"):
            self.assertNotIn(text, source)

    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


class TestFactoryPattern(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")

    def test_factory_creates_physical_product(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_factory_creates_digital_product(self):
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier, download_size=300.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_product_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_main_creates_products_only_through_factory(self):
        with open(os.path.join(PROJECT_DIR, "Main.py")) as f:
            source = f.read()
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)
        self.assertIn("ProductFactory.create(", source)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 0, 10, self.supplier)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "Editor", -5.0, 10, self.supplier)

    def test_negative_stock_rejected_for_both_types(self):
        for product_type in ("physical", "digital"):
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X1", "Item", 10.0, -1, self.supplier)

    def test_zero_stock_allowed(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_order_line_quantity_must_be_positive(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, self.supplier)
        for quantity in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(product, quantity)

    def test_order_rejects_zero_quantity_through_order_line(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10.0, 5, self.supplier)
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(product, 0)


class TestUserInput(unittest.TestCase):
    def test_invalid_input_is_handled_and_user_asked_again(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = get_positive_float("Enter price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")

    def run_load(self, path: str) -> tuple[Inventory, str]:
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, inventory, self.supplier)
        return inventory, output.getvalue()

    def test_missing_file_handled_gracefully(self):
        inventory, output = self.run_load(os.path.join(PROJECT_DIR, "does_not_exist.csv"))
        self.assertIn("Products file not found", output)
        self.assertTrue(output.strip().endswith("Load attempt finished."))
        self.assertEqual(inventory.get_all_products(), [])

    def test_lab_csv_skips_bad_rows_and_loads_valid_rows(self):
        inventory, output = self.run_load(os.path.join(PROJECT_DIR, "products.csv"))
        loaded_ids = [p.get_product_id() for p in inventory.get_all_products()]
        self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)
        lines = output.strip().splitlines()
        self.assertEqual(lines[-2], "3 products loaded.")
        self.assertEqual(lines[-1], "Load attempt finished.")

    def test_invalid_values_in_file_are_skipped(self):
        rows = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,Good,10.00,5\n"
                "physical,P2,Zero Price,0,5\n"
                "digital,D1,Negative Stock,5.00,-1\n"
                "physical,P3,Missing Column,5.00\n")
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(rows)
            path = f.name
        try:
            inventory, output = self.run_load(path)
        finally:
            os.remove(path)
        self.assertEqual([p.get_product_id() for p in inventory.get_all_products()], ["P1"])
        self.assertIn("1 products loaded.", output)


class TestSpecificExceptions(unittest.TestCase):
    def test_every_except_names_a_specific_exception(self):
        for file_name in sorted(os.listdir(PROJECT_DIR)):
            if not file_name.endswith(".py"):
                continue
            with open(os.path.join(PROJECT_DIR, file_name)) as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    self.assertIsNotNone(node.type, f"bare 'except:' in {file_name}")
                    self.assertNotIn(ast.unparse(node.type), ("Exception", "BaseException"),
                                     f"too general 'except' in {file_name}")


if __name__ == "__main__":
    unittest.main()
