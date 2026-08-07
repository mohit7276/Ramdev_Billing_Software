"""
purchase_manager.py

Handles purchase creation,
purchase history and stock updates.

Ramdev Billing Software
"""

from database.excel_manager import ExcelManager
from database.schema import PURCHASES_SHEET

from modules.products.product_manager import ProductManager
from utils.helpers import Helpers


class PurchaseManager:

    def __init__(self):

        self.db = ExcelManager()

        self.product_manager = ProductManager()

    # =====================================================
    # CREATE PURCHASE
    # =====================================================

    def create_purchase(
        self,
        supplier_name,
        supplier_phone,
        product,
        quantity,
        purchase_rate,
        remarks=""
    ):
        """
        Create a purchase record and
        increase product stock.
        """

        try:

            quantity = float(quantity)

            purchase_rate = float(
                purchase_rate
            )

        except (ValueError, TypeError):

            return False, "Invalid quantity or purchase rate."

        if quantity <= 0:

            return False, "Quantity must be greater than zero."

        if purchase_rate < 0:

            return False, "Purchase rate cannot be negative."

        if not product:

            return False, "Product not selected."

        # -------------------------------------------------
        # Generate Purchase ID
        # -------------------------------------------------

        purchase_id = self.db.generate_next_id(
            PURCHASES_SHEET,
            "PUR",
            "Purchase ID"
        )

        # -------------------------------------------------
        # Calculate Amount
        # -------------------------------------------------

        amount = quantity * purchase_rate

        # -------------------------------------------------
        # Purchase Record
        # -------------------------------------------------

        purchase = {

            "Purchase ID": purchase_id,

            "Purchase Date":
                Helpers.current_date(),

            "Supplier Name":
                supplier_name,

            "Supplier Phone":
                supplier_phone,

            "Product ID":
                product["Product ID"],

            "Product Name":
                product["Product Name"],

            "Quantity":
                quantity,

            "Purchase Rate":
                purchase_rate,

            "Amount":
                round(amount, 2),

            "Remarks":
                remarks
        }

        # -------------------------------------------------
        # Save Purchase
        # -------------------------------------------------

        self.db.insert_record(
            PURCHASES_SHEET,
            purchase
        )

        # -------------------------------------------------
        # Update Stock
        # -------------------------------------------------

        success, result = (
            self.product_manager.add_stock(
                product["Product ID"],
                quantity
            )
        )

        if not success:

            return False, result

        return True, purchase_id

    # =====================================================
    # GET ALL PURCHASES
    # =====================================================

    def get_all_purchases(self):

        return self.db.get_all_records(
            PURCHASES_SHEET
        )

    # =====================================================
    # GET PURCHASE
    # =====================================================

    def get_purchase(
        self,
        purchase_id
    ):

        return self.db.find_record(
            PURCHASES_SHEET,
            "Purchase ID",
            purchase_id
        )

    # =====================================================
    # SEARCH PURCHASES
    # =====================================================

    def search_purchase(
        self,
        keyword
    ):

        keyword = str(
            keyword
        ).lower()

        purchases = (
            self.get_all_purchases()
        )

        results = []

        for purchase in purchases:

            if (

                keyword in str(
                    purchase.get(
                        "Purchase ID",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    purchase.get(
                        "Supplier Name",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    purchase.get(
                        "Supplier Phone",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    purchase.get(
                        "Product Name",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    purchase.get(
                        "Product ID",
                        ""
                    )
                ).lower()

            ):

                results.append(
                    purchase
                )

        return results

    # =====================================================
    # TOTAL PURCHASE
    # =====================================================

    def total_purchase_value(self):

        total = 0

        for purchase in (
            self.get_all_purchases()
        ):

            try:

                total += float(
                    purchase.get(
                        "Amount",
                        0
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                continue

        return round(
            total,
            2
        )

    # =====================================================
    # PURCHASE COUNT
    # =====================================================

    def total_purchases(self):

        return len(
            self.get_all_purchases()
        )