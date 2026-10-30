from abc import ABC, abstractmethod
class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
    # Returning product details
    def get_product_id(self):
        return self.__product_id
    def get_name(self):
        return self.__name
    def get_price(self):   
        return self.__price
    def get_stock(self):
        return self.__stock
    # Functions for class behaviour
    def update_stock(self, quantity):
        quantity = int(quantity)
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True
    def display_information(self):
        print(f"Product ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock} units")
    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }
    @abstractmethod
    def get_fulfilment_info(self):
        pass