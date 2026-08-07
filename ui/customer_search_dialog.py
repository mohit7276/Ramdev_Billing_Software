"""
customer_search_dialog.py

Customer Search Dialog

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk

from modules.customers.customer_manager import CustomerManager


class CustomerSearchDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.manager = CustomerManager()

        self.selected_customer = None

        self.title("Select Customer")

        self.geometry("800x500")

        self.resizable(False, False)

        self.grab_set()

        self.create_widgets()

        self.load_customers()

    # -------------------------------------------------

    def create_widgets(self):

        top = ttk.Frame(self)

        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            top,
            text="Search Customer"
        ).pack(side="left")

        self.search_var = tk.StringVar()

        entry = ttk.Entry(
            top,
            textvariable=self.search_var,
            width=35
        )

        entry.pack(
            side="left",
            padx=10
        )

        entry.bind(
            "<KeyRelease>",
            self.search_customer
        )

        columns = (

            "Customer ID",

            "Customer Name",

            "Phone Number",

            "GSTIN",

            "Email"

        )

        self.tree = ttk.Treeview(

            self,

            columns=columns,

            show="headings"

        )

        widths = {

            "Customer ID":120,

            "Customer Name":220,

            "Phone Number":140,

            "GSTIN":170,

            "Email":180

        }

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10
        )

        self.tree.bind(
            "<Double-1>",
            self.select_customer
        )

        button_frame = ttk.Frame(self)

        button_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Button(

            button_frame,

            text="Select",

            command=self.select_customer

        ).pack(
            side="right",
            padx=10
        )

    # -------------------------------------------------

    def load_customers(self):

        self.tree.delete(*self.tree.get_children())

        customers = self.manager.get_all_customers()

        for customer in customers:

            self.tree.insert(

                "",

                "end",

                values=(

                    customer["Customer ID"],

                    customer["Customer Name"],

                    customer["Phone Number"],

                    customer["GSTIN"],

                    customer["Email"]

                )

            )

    # -------------------------------------------------

    def search_customer(self, event=None):

        keyword = self.search_var.get().strip()

        if keyword == "":

            customers = self.manager.get_all_customers()

        else:

            customers = self.manager.search_customers(
                keyword
            )

        self.tree.delete(*self.tree.get_children())

        for customer in customers:

            self.tree.insert(

                "",

                "end",

                values=(

                    customer["Customer ID"],

                    customer["Customer Name"],

                    customer["Phone Number"],

                    customer["GSTIN"],

                    customer["Email"]

                )

            )

    # -------------------------------------------------

    def select_customer(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        customer_id = self.tree.item(
            selected[0]
        )["values"][0]

        self.selected_customer = self.manager.get_customer(
            customer_id
        )

        self.destroy()
