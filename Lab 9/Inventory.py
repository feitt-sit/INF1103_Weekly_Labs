from Product import Product
class Inventory():
    def __init__(self) -> None:
        self.__products: list[Product] = []
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True
    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            return None
        self.__products.remove(product)
        return product
    def search_by_name(self, product_name: str) -> list[Product]:
        results = []
        for p in self.__products:
            if p.get_name().lower() == str(product_name).lower():
                results.append(p)
        return results
    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == str(product_id).lower():
                return product
        return None
    def update_stock(self, product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)
    def display_all(self) -> None:
        if not self.__products:
            print("No products in inventory.")
            return
        print("Products in Inventory:")
        for p in self.__products:
            p.display_information()
    def get_all_products(self) -> list[Product]:
        return list(self.__products)
    