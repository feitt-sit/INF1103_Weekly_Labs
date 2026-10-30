from Product import Product
from CanBeShipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight
    
    def get_fulfilment_info(self):
        return f"Requires physical shipping. Weight: {self.__weight} kg"
    
    def can_be_shipped(self):
        return True

    def calculate_shipping_cost(self):
        base_cost = 5.0  # Base shipping cost
        weight_factor = 2.0  # Cost per kg
        return base_cost + (weight_factor * self.__weight)
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def display_information(self):
        print("Type: Physical")
        super().display_information()
        print(f"Weight: {self.__weight} kg")