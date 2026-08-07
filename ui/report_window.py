"""
report_window.py

Reports Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk

from modules.billing.invoice_manager import InvoiceManager
from modules.customers.customer_manager import CustomerManager
from modules.products.product_manager import ProductManager


class ReportWindow(ttk.Frame):

    def __init__(self, parent, show_header=True):

        super().__init__(parent)

        self.show_header = show_header

        self.invoice_manager = InvoiceManager()
        self.customer_manager = CustomerManager()
        self.product_manager = ProductManager()

        self.pack(fill="both", expand=True)

        self.create_widgets()

        self.load_summary()

    # -------------------------------------------------

    def create_widgets(self):

        summary = ttk.LabelFrame(
            self,
            text="Business Summary",
            padding=15
        )

        summary.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.total_sales = tk.StringVar(value="0.00")
        self.total_invoice = tk.StringVar(value="0")
        self.total_customer = tk.StringVar(value="0")
        self.total_product = tk.StringVar(value="0")
        self.today_sales = tk.StringVar(value="0.00")

        data = [

            ("Total Sales", self.total_sales),

            ("Today's Sales", self.today_sales),

            ("Invoices", self.total_invoice),

            ("Customers", self.total_customer),

            ("Products", self.total_product)

        ]

        for i, (title, variable) in enumerate(data):

            card = ttk.Frame(summary)

            card.grid(
                row=0,
                column=i,
                padx=10
            )

            ttk.Label(

                card,

                text=title,

                font=("Segoe UI", 10, "bold")

            ).pack()

            ttk.Label(

                card,

                textvariable=variable,

                font=("Segoe UI", 15)

            ).pack()

        history = ttk.LabelFrame(

            self,

            text="Recent Invoices",

            padding=10

        )

        history.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        columns = (

            "Invoice",

            "Date",

            "Customer",

            "Amount"

        )

        self.tree = ttk.Treeview(

            history,

            columns=columns,

            show="headings"

        )

        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(
                col,
                width=180,
                anchor="center"
            )

        self.tree.pack(
            fill="both",
            expand=True
        )

    # -------------------------------------------------

    def load_summary(self):

        self.total_sales.set(

            f"₹ {self.invoice_manager.total_sales():,.2f}"

        )

        self.today_sales.set(

            f"₹ {self.invoice_manager.today_sales():,.2f}"

        )

        self.total_invoice.set(

            self.invoice_manager.total_invoices()

        )

        self.total_customer.set(

            len(

                self.customer_manager.get_all_customers()

            )

        )

        self.total_product.set(

            len(

                self.product_manager.get_all_products()

            )

        )

        self.tree.delete(

            *self.tree.get_children()

        )

        invoices = self.invoice_manager.get_all_invoices()

        invoices = invoices[::-1]

        for invoice in invoices[:20]:

            self.tree.insert(

                "",

                "end",

                values=(

                    invoice["Invoice Number"],

                    invoice["Invoice Date"],

                    invoice["Customer Name"],

                    invoice["Grand Total"]

                )

            )
