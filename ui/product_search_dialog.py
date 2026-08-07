"""
product_search_dialog.py

Product Search Dialog

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk

from modules.products.product_manager import ProductManager


class ProductSearchDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.manager = ProductManager()

        self.selected_product = None

        self.title("Select Product")

        self.geometry("1100x550")

        self.resizable(False, False)

        self.grab_set()

        self.create_widgets()

        self.load_products()

    # ---------------------------------------------------------

    def create_widgets(self):

        top = ttk.Frame(self)

        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            top,
            text="Search Product"
        ).pack(side="left")

        self.search_var = tk.StringVar()

        entry = ttk.Entry(
            top,
            textvariable=self.search_var,
            width=40
        )

        entry.pack(
            side="left",
            padx=10
        )

        entry.bind(
            "<KeyRelease>",
            self.search_product
        )

        columns = (

            "Product ID",

            "Thread Type",

            "Product Name",

            "Color",

            "Shade Number",

            "Size",

            "Unit",

            "Rate",

            "GST %",

            "Stock"

        )

        self.tree = ttk.Treeview(

            self,

            columns=columns,

            show="headings"

        )

        widths = {

            "Product ID":100,

            "Thread Type":140,

            "Product Name":220,

            "Color":100,

            "Shade Number":120,

            "Size":80,

            "Unit":80,

            "Rate":100,

            "GST %":80,

            "Stock":80

        }

        for col in columns:

            self.tree.heading(col, text=col)

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
            self.select_product
        )

        button_frame = ttk.Frame(self)

        button_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Button(

            button_frame,

            text="Select",

            command=self.select_product

        ).pack(
            side="right",
            padx=10
        )

    # ---------------------------------------------------------

    def load_products(self):

        self.tree.delete(*self.tree.get_children())

        products = self.manager.get_all_products()

        for product in products:

            self.tree.insert(

                "",

                "end",

                values=(

                    product["Product ID"],

                    product["Thread Type"],

                    product["Product Name"],

                    product["Color"],

                    product["Shade Number"],

                    product["Size"],

                    product["Unit"],

                    product["Rate"],

                    product["GST %"],

                    product["Stock"]

                )

            )

    # ---------------------------------------------------------

    def search_product(self, event=None):

        keyword = self.search_var.get().strip()

        if keyword == "":

            products = self.manager.get_all_products()

        else:

            products = self.manager.search_products(
                keyword
            )

        self.tree.delete(*self.tree.get_children())

        for product in products:

            self.tree.insert(

                "",

                "end",

                values=(

                    product["Product ID"],

                    product["Thread Type"],

                    product["Product Name"],

                    product["Color"],

                    product["Shade Number"],

                    product["Size"],

                    product["Unit"],

                    product["Rate"],

                    product["GST %"],

                    product["Stock"]

                )

            )

    # ---------------------------------------------------------

    def select_product(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        product_id = self.tree.item(
            selected[0]
        )["values"][0]

        self.selected_product = self.manager.get_product(
            product_id
        )

        self.destroy()
