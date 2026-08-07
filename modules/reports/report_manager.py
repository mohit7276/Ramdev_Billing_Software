"""
report_manager.py

Report Manager for
Ramdev Billing Software.

Generates sales, customer, product and stock reports.
"""

from datetime import datetime

from database.excel_manager import ExcelManager
from database.schema import (
    INVOICES_SHEET,
    INVOICE_ITEMS_SHEET,
    CUSTOMERS_SHEET,
    PRODUCTS_SHEET
)


class ReportManager:

    def __init__(self):
        self.db = ExcelManager()

    # ==========================================================
    # Invoice Reports
    # ==========================================================

    def all_invoices(self):
        """
        Return all invoices.
        """
        return self.db.get_all_records(INVOICES_SHEET)

    def invoices_by_date(self, date):
        """
        Return invoices for a specific date.
        Date Format : DD-MM-YYYY
        """

        invoices = self.all_invoices()

        return [
            invoice
            for invoice in invoices
            if invoice["Invoice Date"] == date
        ]

    def invoices_between_dates(self, start_date, end_date):
        """
        Return invoices between dates.
        """

        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")

        result = []

        for invoice in self.all_invoices():

            invoice_date = datetime.strptime(
                invoice["Invoice Date"],
                "%d-%m-%Y"
            )

            if start <= invoice_date <= end:
                result.append(invoice)

        return result

    # ==========================================================
    # Sales Reports
    # ==========================================================

    def total_sales(self):
        """
        Total sales amount.
        """

        total = 0

        for invoice in self.all_invoices():

            total += float(invoice["Grand Total"])

        return round(total, 2)

    def total_gst(self):
        """
        Total GST collected.
        """

        total = 0

        for invoice in self.all_invoices():

            total += float(invoice["GST"])

        return round(total, 2)

    def total_discount(self):
        """
        Total discount given.
        """

        total = 0

        for invoice in self.all_invoices():

            total += float(invoice["Discount"])

        return round(total, 2)

    # ==========================================================
    # Customer Reports
    # ==========================================================

    def total_customers(self):
        """
        Total customers.
        """

        return len(
            self.db.get_all_records(
                CUSTOMERS_SHEET
            )
        )

    def customer_report(self):
        """
        Customer list.
        """

        return self.db.get_all_records(
            CUSTOMERS_SHEET
        )

    # ==========================================================
    # Product Reports
    # ==========================================================

    def total_products(self):
        """
        Total products.
        """

        return len(
            self.db.get_all_records(
                PRODUCTS_SHEET
            )
        )

    def product_report(self):
        """
        Product list.
        """

        return self.db.get_all_records(
            PRODUCTS_SHEET
        )

    def low_stock_products(self, minimum_stock=10):
        """
        Products with low stock.
        """

        products = self.product_report()

        result = []

        for product in products:

            if int(product["Stock"]) <= minimum_stock:
                result.append(product)

        return result

    # ==========================================================
    # Invoice Item Reports
    # ==========================================================

    def invoice_items(self):
        """
        Return all invoice items.
        """

        return self.db.get_all_records(
            INVOICE_ITEMS_SHEET
        )

    def top_selling_products(self):
        """
        Return products sorted by quantity sold.
        """

        items = self.invoice_items()

        sales = {}

        for item in items:

            name = item["Product Name"]

            qty = float(item["Quantity"])

            sales[name] = sales.get(name, 0) + qty

        return sorted(
            sales.items(),
            key=lambda x: x[1],
            reverse=True
        )

    # ==========================================================
    # Dashboard Statistics
    # ==========================================================

    def dashboard_summary(self):
        """
        Dashboard summary.
        """

        return {

            "total_sales": self.total_sales(),

            "total_invoices": len(self.all_invoices()),

            "total_customers": self.total_customers(),

            "total_products": self.total_products(),

            "low_stock_products": len(
                self.low_stock_products()
            ),

            "total_gst": self.total_gst(),

            "total_discount": self.total_discount()

        }
