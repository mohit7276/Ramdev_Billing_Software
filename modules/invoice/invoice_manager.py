"""
invoice_manager.py

Handles invoice creation, invoice items,
payment details and stock updates.

Ramdev Billing Software
"""

from database.excel_manager import ExcelManager

from database.schema import (
    INVOICES_SHEET,
    INVOICE_ITEMS_SHEET
)

from modules.products.product_manager import ProductManager
from utils.helpers import Helpers


class InvoiceManager:

    def __init__(self):

        self.db = ExcelManager()

        self.product_manager = ProductManager()

    # =====================================================
    # CREATE INVOICE
    # =====================================================

    def create_invoice(
        self,
        customer,
        items,
        payment_mode="Cash",
        payment_status="Paid",
        discount=0
    ):

        if not customer:

            return False, "Customer is required."

        if not items:

            return False, "Invoice contains no items."

        try:

            discount = float(discount)

        except (
            ValueError,
            TypeError
        ):

            return False, "Invalid discount."

        if discount < 0:

            return False, "Discount cannot be negative."

        invoice_number = (
            Helpers.next_invoice_number()
        )

        subtotal = 0
        gst_total = 0

        # -------------------------------------------------
        # Calculate Invoice Total
        # -------------------------------------------------

        for item in items:

            try:

                quantity = float(
                    item["Quantity"]
                )

                rate = float(
                    item["Rate"]
                )

                gst_percent = float(
                    item["GST %"]
                )

            except (
                KeyError,
                ValueError,
                TypeError
            ):

                return False, "Invalid invoice item."

            if quantity <= 0:

                return False, "Quantity must be greater than zero."

            if rate < 0:

                return False, "Rate cannot be negative."

            amount = quantity * rate

            gst_amount = (
                amount * gst_percent / 100
            )

            subtotal += amount

            gst_total += gst_amount

        grand_total = (
            subtotal
            + gst_total
            - discount
        )

        if grand_total < 0:

            return False, "Discount cannot exceed invoice amount."

        # -------------------------------------------------
        # Invoice Record
        # -------------------------------------------------

        invoice = {

            "Invoice Number":
                invoice_number,

            "Invoice Date":
                Helpers.current_date(),

            "Invoice Time":
                Helpers.current_time(),

            "Customer ID":
                customer["Customer ID"],

            "Customer Name":
                customer["Customer Name"],

            "Phone Number":
                customer.get(
                    "Phone Number",
                    ""
                ),

            "Subtotal":
                round(
                    subtotal,
                    2
                ),

            "Discount":
                round(
                    discount,
                    2
                ),

            "GST":
                round(
                    gst_total,
                    2
                ),

            "Grand Total":
                round(
                    grand_total,
                    2
                ),

            "Payment Mode":
                payment_mode,

            "Payment Status":
                payment_status,

            "PDF Path":
                "",

            "Excel Path":
                ""
        }

        # -------------------------------------------------
        # Save Invoice
        # -------------------------------------------------

        self.db.insert_record(
            INVOICES_SHEET,
            invoice
        )

        # -------------------------------------------------
        # Save Invoice Items
        # -------------------------------------------------

        for item in items:

            quantity = float(
                item["Quantity"]
            )

            rate = float(
                item["Rate"]
            )

            gst_percent = float(
                item["GST %"]
            )

            base_amount = (
                quantity * rate
            )

            gst_amount = (
                base_amount
                * gst_percent
                / 100
            )

            total_amount = (
                base_amount
                + gst_amount
            )

            row = {

                "Invoice Number":
                    invoice_number,

                "Product ID":
                    item["Product ID"],

                "Thread Type":
                    item["Thread Type"],

                "Product Name":
                    item["Product Name"],

                "Color":
                    item["Color"],

                "Shade Number":
                    item["Shade Number"],

                "Size":
                    item["Size"],

                "Unit":
                    item["Unit"],

                "Quantity":
                    quantity,

                "Rate":
                    rate,

                "GST %":
                    gst_percent,

                "Amount":
                    round(
                        total_amount,
                        2
                    )
            }

            self.db.insert_record(
                INVOICE_ITEMS_SHEET,
                row
            )

            # ---------------------------------------------
            # Reduce Stock
            # ---------------------------------------------

            success = self.product_manager.update_stock(
                item["Product ID"],
                quantity
            )

            if not success:

                return (
                    False,
                    f"Unable to reduce stock for product "
                    f"{item['Product ID']}."
                )

        return True, invoice_number

    # =====================================================
    # GET INVOICE
    # =====================================================

    def get_invoice(
        self,
        invoice_number
    ):

        return self.db.find_record(
            INVOICES_SHEET,
            "Invoice Number",
            invoice_number
        )

    # =====================================================
    # GET INVOICE ITEMS
    # =====================================================

    def get_invoice_items(
        self,
        invoice_number
    ):

        items = (
            self.db.get_all_records(
                INVOICE_ITEMS_SHEET
            )
        )

        return [
            item
            for item in items
            if str(
                item.get(
                    "Invoice Number",
                    ""
                )
            ) == str(
                invoice_number
            )
        ]

    # =====================================================
    # ALL INVOICES
    # =====================================================

    def get_all_invoices(self):

        return self.db.get_all_records(
            INVOICES_SHEET
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_invoice(
        self,
        keyword
    ):

        keyword = str(
            keyword
        ).lower()

        invoices = (
            self.get_all_invoices()
        )

        results = []

        for invoice in invoices:

            if (

                keyword in str(
                    invoice.get(
                        "Invoice Number",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    invoice.get(
                        "Customer Name",
                        ""
                    )
                ).lower()

                or

                keyword in str(
                    invoice.get(
                        "Phone Number",
                        ""
                    )
                ).lower()

            ):

                results.append(
                    invoice
                )

        return results

    # =====================================================
    # TOTAL SALES
    # =====================================================

    def total_sales(self):

        total = 0

        for invoice in (
            self.get_all_invoices()
        ):

            try:

                total += float(
                    invoice.get(
                        "Grand Total",
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
    # TOTAL INVOICES
    # =====================================================

    def total_invoices(self):

        return len(
            self.get_all_invoices()
        )

    # =====================================================
    # TODAY SALES
    # =====================================================

    def today_sales(self):

        today = (
            Helpers.current_date()
        )

        total = 0

        for invoice in (
            self.get_all_invoices()
        ):

            if str(
                invoice.get(
                    "Invoice Date",
                    ""
                )
            ) == str(today):

                try:

                    total += float(
                        invoice.get(
                            "Grand Total",
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
