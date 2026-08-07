"""
product_dialog.py

Add/Edit Product Dialog

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_manager import ProductManager


class ProductDialog(tk.Toplevel):

    def __init__(self, parent, product=None):

        super().__init__(parent)

        self.manager = ProductManager()
        self.product = product
        self.saved = False

        self.title(
            "Edit Product"
            if product else
            "Add Product"
        )

        self.geometry("600x650")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

        if product:
            self.load_product()

    # ---------------------------------------------------------

    def create_widgets(self):

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        # Thread Type

        ttk.Label(frame, text="Thread Type").grid(row=0, column=0, sticky="w", pady=8)

        self.thread_type = ttk.Entry(frame, width=35)
        self.thread_type.grid(row=0, column=1)

        # Product Name

        ttk.Label(frame, text="Product Name").grid(row=1, column=0, sticky="w", pady=8)

        self.product_name = ttk.Entry(frame, width=35)
        self.product_name.grid(row=1, column=1)

        # Color

        ttk.Label(frame, text="Color").grid(row=2, column=0, sticky="w", pady=8)

        self.color = ttk.Entry(frame, width=35)
        self.color.grid(row=2, column=1)

        # Shade Number

        ttk.Label(frame, text="Shade Number").grid(row=3, column=0, sticky="w", pady=8)

        self.shade = ttk.Entry(frame, width=35)
        self.shade.grid(row=3, column=1)

        # Size

        ttk.Label(frame, text="Size").grid(row=4, column=0, sticky="w", pady=8)

        self.size = ttk.Entry(frame, width=35)
        self.size.grid(row=4, column=1)

        # Unit

        ttk.Label(frame, text="Unit").grid(row=5, column=0, sticky="w", pady=8)

        self.unit = ttk.Entry(frame, width=35)
        self.unit.grid(row=5, column=1)

        # Rate

        ttk.Label(frame, text="Rate").grid(row=6, column=0, sticky="w", pady=8)

        self.rate = ttk.Entry(frame, width=35)
        self.rate.grid(row=6, column=1)

        # GST

        ttk.Label(frame, text="GST %").grid(row=7, column=0, sticky="w", pady=8)

        self.gst = ttk.Combobox(
            frame,
            width=32,
            state="readonly",
            values=[
                "0",
                "5",
                "12",
                "18",
                "28"
            ]
        )

        self.gst.current(3)

        self.gst.grid(row=7, column=1)

        # Stock

        ttk.Label(frame, text="Opening Stock").grid(row=8, column=0, sticky="w", pady=8)

        self.stock = ttk.Entry(frame, width=35)

        self.stock.grid(row=8, column=1)

        # Buttons

        button_frame = ttk.Frame(frame)

        button_frame.grid(
            row=9,
            column=0,
            columnspan=2,
            pady=25
        )

        ttk.Button(
            button_frame,
            text="Save",
            command=self.save
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", padx=5)

    # ---------------------------------------------------------

    def load_product(self):

        self.thread_type.insert(
            0,
            self.product["Thread Type"]
        )

        self.product_name.insert(
            0,
            self.product["Product Name"]
        )

        self.color.insert(
            0,
            self.product["Color"]
        )

        self.shade.insert(
            0,
            self.product["Shade Number"]
        )

        self.size.insert(
            0,
            self.product["Size"]
        )

        self.unit.insert(
            0,
            self.product["Unit"]
        )

        self.rate.insert(
            0,
            self.product["Rate"]
        )

        self.gst.set(
            str(self.product["GST %"])
        )

        self.stock.insert(
            0,
            self.product["Stock"]
        )

    # ---------------------------------------------------------

    def save(self):

        if self.product:

            success, result = self.manager.update_product(

                self.product["Product ID"],

                {

                    "Thread Type": self.thread_type.get().strip(),

                    "Product Name": self.product_name.get().strip(),

                    "Color": self.color.get().strip(),

                    "Shade Number": self.shade.get().strip(),

                    "Size": self.size.get().strip(),

                    "Unit": self.unit.get().strip(),

                    "Rate": self.rate.get().strip(),

                    "GST %": self.gst.get(),

                    "Stock": self.stock.get().strip()

                }

            )

        else:

            success, result = self.manager.add_product(

                thread_type=self.thread_type.get().strip(),

                product_name=self.product_name.get().strip(),

                color=self.color.get().strip(),

                shade_number=self.shade.get().strip(),

                size=self.size.get().strip(),

                unit=self.unit.get().strip(),

                rate=self.rate.get().strip(),

                gst=self.gst.get(),

                stock=self.stock.get().strip()

            )

        if success:

            self.saved = True

            messagebox.showinfo(
                "Success",
                "Product saved successfully."
            )

            self.destroy()

        else:

            messagebox.showerror(
                "Validation Error",
                "\n".join(result)
            )
