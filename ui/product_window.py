"""
product_window.py

Product Management Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.base_window import BaseWindow
from modules.products.product_manager import ProductManager


class ProductWindow(BaseWindow):

    def __init__(self, parent, title="Product Management", show_header=True):

        self.manager = ProductManager()

        super().__init__(parent, title, show_header=show_header)

        self.load_products()

    # ==========================================================
    # Toolbar
    # ==========================================================

    def create_toolbar(self):

        super().create_toolbar()

        ttk.Button(
            self.toolbar,
            text="Add Product",
            command=self.add_product
        ).pack(side="left", padx=5)

        ttk.Button(
            self.toolbar,
            text="Edit Product",
            command=self.edit_product
        ).pack(side="left", padx=5)

        ttk.Button(
            self.toolbar,
            text="Delete Product",
            command=self.delete_product
        ).pack(side="left", padx=5)

        ttk.Label(
            self.toolbar,
            text="Search:"
        ).pack(side="right")

        self.search_var = tk.StringVar()

        search = ttk.Entry(
            self.toolbar,
            textvariable=self.search_var,
            width=35
        )

        search.pack(side="right", padx=5)

        search.bind("<KeyRelease>", self.search_products)

    # ==========================================================
    # Content
    # ==========================================================

    def create_content(self):

        self.content = ttk.Frame(self)

        self.content.pack(fill="both", expand=True, padx=15)

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

            self.content,

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
            self.content,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    # ==========================================================
    # Load Products
    # ==========================================================

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

        self.set_status(
            f"{len(products)} product(s)"
        )

    # ==========================================================
    # Search
    # ==========================================================

    def search_products(self, event=None):

        keyword = self.search_var.get().strip()

        self.tree.delete(*self.tree.get_children())

        if keyword:

            products = self.manager.search_products(keyword)

        else:

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

        self.set_status(
            f"{len(products)} product(s)"
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def selected_product(self):

        selected = self.tree.selection()

        if not selected:
            return None

        values = self.tree.item(
            selected[0]
        )["values"]

        return values[0]

    # ==========================================================
    # Buttons
    # ==========================================================

    def add_product(self):

        from ui.product_dialog import ProductDialog

        dialog = ProductDialog(self)

        self.wait_window(dialog)

        if dialog.saved:
            self.load_products()

    def edit_product(self):

        product_id = self.selected_product()

        if not product_id:

            messagebox.showwarning(
                "Warning",
                "Select a product."
            )

            return

        product = self.manager.get_product(product_id)

        from ui.product_dialog import ProductDialog

        dialog = ProductDialog(
            self,
            product
        )

        self.wait_window(dialog)

        if dialog.saved:
            self.load_products()

    def delete_product(self):

        product_id = self.selected_product()

        if not product_id:

            messagebox.showwarning(
                "Warning",
                "Select a product."
            )

            return

        if not messagebox.askyesno(
            "Delete",
            "Delete selected product?"
        ):
            return

        if self.manager.delete_product(product_id):

            self.load_products()

            messagebox.showinfo(
                "Success",
                "Product deleted successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete product."
            )
