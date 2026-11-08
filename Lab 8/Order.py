from Product import Product
from OrderLine import OrderLine


class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this Order (it is never passed in)."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().lower() == str(product_id).lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        """Return a copy of the list so the Order's own list cannot be changed outside."""
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")
        if not self.__order_lines:
            print("No order lines.")
            return
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order Total: ${self.calculate_total():.2f}")
