"""
inventory_manager.py

Inventory Management

Ramdev Billing Software
"""

from modules.products.product_manager import ProductManager


class InventoryManager:

    def __init__(self):

        self.product_manager = ProductManager()

    # -------------------------------------------------

    def get_stock(self):

        return self.product_manager.get_all_products()

    # -------------------------------------------------

    def low_stock(self, limit=10):

        products = self.get_stock()

        return [

            product

            for product in products

            if float(product["Stock"]) <= limit

        ]

    # -------------------------------------------------

    def out_of_stock(self):

        products = self.get_stock()

        return [

            product

            for product in products

            if float(product["Stock"]) == 0

        ]

    # -------------------------------------------------

    def stock_value(self):

        total = 0

        for product in self.get_stock():

            total += (

                float(product["Rate"])

                * float(product["Stock"])

            )

        return round(total, 2)

    # -------------------------------------------------

    def total_stock_items(self):

        return len(self.get_stock())

    # -------------------------------------------------

    def total_quantity(self):

        qty = 0

        for product in self.get_stock():

            qty += float(product["Stock"])

        return qty
