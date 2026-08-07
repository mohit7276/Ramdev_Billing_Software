"""
stock_window.py

Inventory Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk

from modules.inventory.inventory_manager import InventoryManager


class StockWindow(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.manager = InventoryManager()

        self.title("Inventory")

        self.geometry("1200x650")

        self.create_widgets()

        self.load_stock()

    # -------------------------------------------------

    def create_widgets(self):

        columns = (

            "Product ID",

            "Product Name",

            "Thread Type",

            "Color",

            "Size",

            "Rate",

            "Stock"

        )

        self.tree = ttk.Treeview(

            self,

            columns=columns,

            show="headings"

        )

        for col in columns:

            self.tree.heading(col, text=col)

            self.tree.column(

                col,

                width=160,

                anchor="center"

            )

        self.tree.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        bottom = ttk.Frame(self)

        bottom.pack(fill="x", padx=10, pady=10)

        self.stock_label = ttk.Label(bottom)

        self.stock_label.pack(side="left")

        self.value_label = ttk.Label(bottom)

        self.value_label.pack(side="right")

    # -------------------------------------------------

    def load_stock(self):

        self.tree.delete(*self.tree.get_children())

        for product in self.manager.get_stock():

            self.tree.insert(

                "",

                "end",

                values=(

                    product["Product ID"],

                    product["Product Name"],

                    product["Thread Type"],

                    product["Color"],

                    product["Size"],

                    product["Rate"],

                    product["Stock"]

                )

            )

        self.stock_label.config(

            text=f"Products : {self.manager.total_stock_items()}"

        )

        self.value_label.config(

            text=f"Stock Value : ₹ {self.manager.stock_value():,.2f}"

        )
