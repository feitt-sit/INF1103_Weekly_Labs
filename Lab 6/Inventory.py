class Inventory():
    def __init__(self):
        self.__products = []
    def search_product(self, product_id):
        for p in self.__products:
            if p.get_product_id().lower() == str(product_id).lower():
                return p
        return None
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return None
        self.__products.append(product)
        return True
    def search_by_name(self, product_name):
        results = []
        for p in self.__products:
            if p.get_name().lower() == str(product_name).lower():
                results.append(p)
        return results
    def update_stock(self, product_id, new_stock):
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(new_stock)
    def display_all(self):
        if not self.__products:
            print("No products in inventory.")
            return
        print("Products in Inventory:")
        for p in self.__products:
            p.display_information()
    def get_all_products(self):
        return list(self.__products)
    