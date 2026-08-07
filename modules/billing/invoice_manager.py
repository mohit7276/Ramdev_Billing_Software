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

    def create_invoice(
        self,
        customer,
        items,
        payment_mode="Cash",
        payment_status="Paid",
        discount=0
    ):
        """
        Create invoice.

        customer -> dict

        items -> list of dictionaries
        """

        if not items:
            return False, "Invoice contains no items."

        invoice_number = Helpers.next_invoice_number()

        subtotal = 0
        gst_total = 0

        # --------------------------
        # Calculate Totals
        # --------------------------

        for item in items:

            qty = float(item["Quantity"])
            rate = float(item["Rate"])
            gst = float(item["GST %"])

            amount = qty * rate

            gst_amount = amount * gst / 100

            subtotal += amount
            gst_total += gst_amount

        grand_total = subtotal + gst_total - float(discount)

        invoice = {

            "Invoice Number": invoice_number,

            "Invoice Date": Helpers.current_date(),

            "Invoice Time": Helpers.current_time(),

            "Customer ID": customer["Customer ID"],

            "Customer Name": customer["Customer Name"],

            "Phone Number": customer["Phone Number"],

            "Subtotal": round(subtotal, 2),

            "Discount": round(discount, 2),

            "GST": round(gst_total, 2),

            "Grand Total": round(grand_total, 2),

            "Payment Mode": payment_mode,

            "Payment Status": payment_status,

            "PDF Path": "",

            "Excel Path": ""
        }

        # Save Invoice

        self.db.insert_record(
            INVOICES_SHEET,
            invoice
        )

        # --------------------------
        # Save Items
        # --------------------------

        for item in items:

            qty = float(item["Quantity"])
            rate = float(item["Rate"])
            gst = float(item["GST %"])

            amount = qty * rate
            amount += amount * gst / 100

            row = {

                "Invoice Number": invoice_number,

                "Product ID": item["Product ID"],

                "Thread Type": item["Thread Type"],

                "Product Name": item["Product Name"],

                "Color": item["Color"],

                "Shade Number": item["Shade Number"],

                "Size": item["Size"],

                "Unit": item["Unit"],

                "Quantity": qty,

                "Rate": rate,

                "GST %": gst,

                "Amount": round(amount, 2)

            }

            self.db.insert_record(
                INVOICE_ITEMS_SHEET,
                row
            )

            # Update Stock

            self.product_manager.update_stock(
                item["Product ID"],
                int(qty)
            )

        return True, {
    "invoice_number": invoice_number,
    "invoice": invoice
}

    def get_invoice(self, invoice_number):
        """
        Get invoice by number.
        """

        return self.db.find_record(
            INVOICES_SHEET,
            "Invoice Number",
            invoice_number
        )

    def get_invoice_items(self, invoice_number):
        """
        Return invoice items.
        """

        items = self.db.get_all_records(
            INVOICE_ITEMS_SHEET
        )

        return [
            item
            for item in items
            if item["Invoice Number"] == invoice_number
        ]

    def get_all_invoices(self):
        """
        Return all invoices.
        """

        return self.db.get_all_records(
            INVOICES_SHEET
        )

    def search_invoice(self, keyword):
        """
        Search invoice.
        """

        keyword = str(keyword).lower()

        invoices = self.get_all_invoices()

        results = []

        for invoice in invoices:

            if (
                keyword in str(invoice["Invoice Number"]).lower()
                or keyword in str(invoice["Customer Name"]).lower()
                or keyword in str(invoice["Phone Number"]).lower()
            ):
                results.append(invoice)

        return results

    def total_sales(self):
        """
        Return total sales amount.
        """

        total = 0

        for invoice in self.get_all_invoices():

            total += float(invoice["Grand Total"])

        return round(total, 2)

    def total_invoices(self):
        """
        Return invoice count.
        """

        return len(self.get_all_invoices())

    def today_sales(self):
        """
        Return today's sales.
        """

        today = Helpers.current_date()

        total = 0

        for invoice in self.get_all_invoices():

            if invoice["Invoice Date"] == today:

                total += float(invoice["Grand Total"])

        return round(total, 2)
