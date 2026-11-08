from Product import Product
from CanBeShipped import CanBeShipped
from Supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight
    
    def get_fulfilment_info(self) -> str:
        return f"Requires physical shipping. Weight: {self.__weight} kg"
    
    def can_be_shipped(self) -> bool:
        return True

    def calculate_shipping_cost(self) -> float:
        base_cost = 5.0  # Base shipping cost
        weight_factor = 2.0  # Cost per kg
        return base_cost + (weight_factor * self.__weight)
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def display_information(self) -> None:
        print("Type: Physical")
        super().display_information()
        print(f"Weight: {self.__weight} kg")