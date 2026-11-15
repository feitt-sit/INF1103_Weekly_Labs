from Product import Product
from OrderLine import OrderLine
from DiscountStrategy import DiscountStrategy, NoDiscount

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this Order (it is never passed in)."""
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
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")
        if not self.__order_lines:
            print("No order lines.")
            return
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order Total: ${self.calculate_total():.2f}")
