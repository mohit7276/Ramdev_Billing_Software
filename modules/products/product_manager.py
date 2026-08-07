"""
product_manager.py

Product management module for
Ramdev Billing Software.
"""

from database.excel_manager import ExcelManager
from database.validator import Validator
from database.schema import PRODUCTS_SHEET


class ProductManager:

    def __init__(self):
        self.db = ExcelManager()

    def get_all_products(self):
        """
        Return all products.
        """
        return self.db.get_all_records(PRODUCTS_SHEET)

    def get_product(self, product_id):
        """
        Return product by Product ID.
        """
        return self.db.find_record(
            PRODUCTS_SHEET,
            "Product ID",
            product_id
        )

    def product_exists(self, product_id):
        """
        Check product exists.
        """
        return self.db.record_exists(
            PRODUCTS_SHEET,
            "Product ID",
            product_id
        )

    def add_product(
        self,
        thread_type,
        product_name,
        color,
        shade_number,
        size,
        unit,
        rate,
        gst,
        stock
    ):
        """
        Add new product.
        """

        product = {
            "Product ID": self.db.generate_next_id(
                PRODUCTS_SHEET,
                "PROD",
                "Product ID"
            ),
            "Thread Type": thread_type,
            "Product Name": product_name,
            "Color": color,
            "Shade Number": shade_number,
            "Size": size,
            "Unit": unit,
            "Rate": rate,
            "GST %": gst,
            "Stock": stock
        }

        errors = Validator.validate_product(product)

        if errors:
            return False, errors

        self.db.insert_record(
            PRODUCTS_SHEET,
            product
        )

        return True, product

    def update_product(
        self,
        product_id,
        data
    ):
        """
        Update existing product.
        """

        product = self.get_product(product_id)

        if not product:
            return False, ["Product not found."]

        product.update(data)

        errors = Validator.validate_product(product)

        if errors:
            return False, errors

        self.db.update_record(
            PRODUCTS_SHEET,
            "Product ID",
            product_id,
            data
        )

        return True, product

    def delete_product(self, product_id):
        """
        Delete product.
        """

        if not self.product_exists(product_id):
            return False

        return self.db.delete_record(
            PRODUCTS_SHEET,
            "Product ID",
            product_id
        )

    def search_products(self, keyword):
        """
        Search products by Product ID,
        Product Name, Thread Type,
        Color or Shade Number.
        """

        keyword = keyword.lower().strip()

        results = []

        for product in self.get_all_products():

            if (
                keyword in str(product["Product ID"]).lower()
                or keyword in str(product["Product Name"]).lower()
                or keyword in str(product["Thread Type"]).lower()
                or keyword in str(product["Color"]).lower()
                or keyword in str(product["Shade Number"]).lower()
            ):
                results.append(product)

        return results

    def update_stock(self, product_id, quantity):
        """
        Reduce stock after billing.
        """

        product = self.get_product(product_id)

        if not product:
            return False

        current_stock = int(product["Stock"])

        if quantity > current_stock:
            return False

        new_stock = current_stock - quantity

        self.db.update_record(
            PRODUCTS_SHEET,
            "Product ID",
            product_id,
            {
                "Stock": new_stock
            }
        )

        return True

    def increase_stock(self, product_id, quantity):
        """
        Increase stock.
        """

        product = self.get_product(product_id)

        if not product:
            return False

        current_stock = int(product["Stock"])

        self.db.update_record(
            PRODUCTS_SHEET,
            "Product ID",
            product_id,
            {
                "Stock": current_stock + quantity
            }
        )

        return True

    def low_stock_products(self, minimum_stock=10):
        """
        Return products with stock less than or
        equal to minimum_stock.
        """

        products = []

        for product in self.get_all_products():

            if int(product["Stock"]) <= minimum_stock:
                products.append(product)

        return products

    def total_products(self):
        """
        Return total product count.
        """
        return len(self.get_all_products())

def add_stock(self, product_id, quantity):
    """
    Add purchased quantity to existing product stock.
    """

    product = self.db.find_record(
        PRODUCTS_SHEET,
        "Product ID",
        product_id
    )

    if not product:
        return False, "Product not found."

    current_stock = float(
        product.get("Stock", 0)
    )

    new_stock = current_stock + float(quantity)

    self.db.update_record(
        PRODUCTS_SHEET,
        "Product ID",
        product_id,
        {
            "Stock": new_stock
        }
    )

    return True, new_stock

# =====================================================
# REDUCE STOCK
# =====================================================

def reduce_stock(
    self,
    product_id,
    quantity
):
    """
    Reduce product stock when a sale/invoice is created.
    """

    try:
        quantity = float(quantity)

    except (ValueError, TypeError):
        return False, "Invalid quantity."

    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    product = self.find_product(
        product_id
    )

    if not product:
        return False, "Product not found."

    try:
        current_stock = float(
            product.get("Stock", 0)
        )

    except (ValueError, TypeError):
        return False, "Invalid current stock."

    if quantity > current_stock:
        return (
            False,
            f"Insufficient stock. "
            f"Available stock: {current_stock}"
        )

    new_stock = current_stock - quantity

    success = self.db.update_record(
        "Products",
        "Product ID",
        product_id,
        {
            "Stock": new_stock
        }
    )

    if not success:
        return False, "Unable to update product stock."

    return True, new_stock