"""
purchase_window.py

Purchase Entry Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modules.suppliers.supplier_manager import SupplierManager
from modules.purchase.purchase_manager import PurchaseManager
from modules.products.product_manager import ProductManager


class PurchaseWindow(ttk.Frame):

    def __init__(self, parent, on_close=None):

        super().__init__(parent)

        self.on_close = on_close or self.destroy

        self.purchase_manager = PurchaseManager()

        self.product_manager = ProductManager()

        self.supplier_manager = SupplierManager()

        self.suppliers = []

        self.products = []

        self.create_widgets()

        self.pack(fill="both", expand=True)

        self.load_products()

        self.load_suppliers()

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        main = ttk.Frame(self)
        main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.supplier_name = tk.StringVar()
        self.supplier_phone = tk.StringVar()

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Purchase Entry",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=(0, 20)
        )

        # -------------------------------------------------
        # Supplier
        # -------------------------------------------------

        supplier_frame = ttk.LabelFrame(
            main,
            text="Supplier Details",
            padding=15
        )

        supplier_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            supplier_frame,
            text="Supplier Name:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.supplier_combo = ttk.Combobox(
            supplier_frame,
            textvariable=self.supplier_name,
            state="readonly",
            width=32
        )

        self.supplier_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.supplier_combo.bind(
            "<<ComboboxSelected>>",
            self.supplier_selected
        )

        ttk.Label(
            supplier_frame,
            text="Phone:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        ttk.Entry(
            supplier_frame,
            textvariable=self.supplier_phone,
            width=25
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            supplier_frame,
            text="Phone:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.supplier_phone = tk.StringVar()

        ttk.Entry(
            supplier_frame,
            textvariable=self.supplier_phone,
            width=25
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Product
        # -------------------------------------------------

        product_frame = ttk.LabelFrame(
            main,
            text="Product Details",
            padding=15
        )

        product_frame.pack(
            fill="x",
            pady=10
        )

        ttk.Label(
            product_frame,
            text="Product:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.product_var = tk.StringVar()

        self.product_combo = ttk.Combobox(
            product_frame,
            textvariable=self.product_var,
            state="readonly",
            width=40
        )

        self.product_combo.grid(
            row=0,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.product_combo.bind(
            "<<ComboboxSelected>>",
            self.product_selected
        )

        # -------------------------------------------------
        # Product Information
        # -------------------------------------------------

        ttk.Label(
            product_frame,
            text="Product ID:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.product_id = tk.StringVar()

        ttk.Entry(
            product_frame,
            textvariable=self.product_id,
            state="readonly",
            width=20
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            product_frame,
            text="Current Stock:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.current_stock = tk.StringVar()

        ttk.Entry(
            product_frame,
            textvariable=self.current_stock,
            state="readonly",
            width=15
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Quantity
        # -------------------------------------------------

        ttk.Label(
            product_frame,
            text="Quantity:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.quantity = tk.StringVar()

        ttk.Entry(
            product_frame,
            textvariable=self.quantity,
            width=20
        ).grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Purchase Rate
        # -------------------------------------------------

        ttk.Label(
            product_frame,
            text="Purchase Rate:"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.purchase_rate = tk.StringVar()

        ttk.Entry(
            product_frame,
            textvariable=self.purchase_rate,
            width=15
        ).grid(
            row=2,
            column=3,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Amount
        # -------------------------------------------------

        ttk.Label(
            product_frame,
            text="Amount:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.amount = tk.StringVar(
            value="0.00"
        )

        ttk.Entry(
            product_frame,
            textvariable=self.amount,
            state="readonly",
            width=20
        ).grid(
            row=3,
            column=1,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Remarks
        # -------------------------------------------------

        ttk.Label(
            product_frame,
            text="Remarks:"
        ).grid(
            row=4,
            column=0,
            sticky="nw",
            padx=5,
            pady=5
        )

        self.remarks = tk.StringVar()

        ttk.Entry(
            product_frame,
            textvariable=self.remarks,
            width=50
        ).grid(
            row=4,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="w"
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        button_frame = ttk.Frame(
            main
        )

        button_frame.pack(
            pady=20
        )

        ttk.Button(
            button_frame,
            text="Save Purchase",
            command=self.save_purchase
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.close_window
        ).pack(
            side="left",
            padx=10
        )

        # -------------------------------------------------
        # Amount Calculation
        # -------------------------------------------------

        self.quantity.trace_add(
            "write",
            self.calculate_amount
        )

        self.purchase_rate.trace_add(
            "write",
            self.calculate_amount
        )

    def close_window(self):

        self.on_close()

    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    def load_products(self):

        try:

            self.products = (
                self.product_manager
                .get_all_products()
            )

            product_names = []

            for product in self.products:

                product_names.append(
                    product.get(
                        "Product Name",
                        ""
                    )
                )

            self.product_combo["values"] = (
                product_names
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to load products.\n\n{e}"
            )


def load_suppliers(self):

    self.suppliers = self.supplier_manager.get_all_suppliers()

    supplier_names = []

    for supplier in self.suppliers:
        supplier_names.append(supplier.get("Supplier Name", ""))

    self.supplier_combo["values"] = supplier_names


def supplier_selected(self, event=None):

    selected_name = self.supplier_name.get()

    for supplier in self.suppliers:

        if supplier.get("Supplier Name", "") == selected_name:
            self.supplier_phone.set(supplier.get("Phone Number", ""))
            break


def product_selected(self, event=None):

    selected_name = self.product_var.get()

    for product in self.products:

        if product.get("Product Name", "") == selected_name:

            self.product_id.set(product.get("Product ID", ""))
            self.current_stock.set(product.get("Stock", 0))
            self.purchase_rate.set(product.get("Rate", 0))
            break


def calculate_amount(self, *args):

    try:
        quantity = float(self.quantity.get())
        rate = float(self.purchase_rate.get())
        self.amount.set(f"{quantity * rate:.2f}")
    except (ValueError, TypeError):
        self.amount.set("0.00")


def save_purchase(self):

    supplier = self.supplier_name.get().strip()
    phone = self.supplier_phone.get().strip()
    product_name = self.product_var.get()
    quantity = self.quantity.get().strip()
    rate = self.purchase_rate.get().strip()
    remarks = self.remarks.get().strip()

    if not supplier:
        messagebox.showwarning("Validation", "Enter supplier name.")
        return

    if not product_name:
        messagebox.showwarning("Validation", "Select a product.")
        return

    if not quantity:
        messagebox.showwarning("Validation", "Enter quantity.")
        return

    if not rate:
        messagebox.showwarning("Validation", "Enter purchase rate.")
        return

    try:
        quantity_value = float(quantity)
        rate_value = float(rate)
    except ValueError:
        messagebox.showerror("Validation", "Quantity and rate must be numbers.")
        return

    if quantity_value <= 0:
        messagebox.showwarning("Validation", "Quantity must be greater than zero.")
        return

    if rate_value < 0:
        messagebox.showwarning("Validation", "Purchase rate cannot be negative.")
        return

    selected_product = None

    for product in self.products:

        if product.get("Product Name", "") == product_name:
            selected_product = product
            break

    if not selected_product:
        messagebox.showerror("Error", "Selected product was not found.")
        return

    success, result = self.purchase_manager.create_purchase(
        supplier_name=supplier,
        supplier_phone=phone,
        product=selected_product,
        quantity=quantity_value,
        purchase_rate=rate_value,
        remarks=remarks
    )

    if success:
        messagebox.showinfo(
            "Purchase Saved",
            f"Purchase saved successfully.\n\nPurchase ID: {result}"
        )
        self.clear_form()
        self.load_products()
    else:
        messagebox.showerror("Purchase Failed", str(result))


def clear_form(self):

    self.supplier_name.set("")
    self.supplier_phone.set("")
    self.product_var.set("")
    self.product_id.set("")
    self.current_stock.set("")
    self.quantity.set("")
    self.purchase_rate.set("")
    self.amount.set("0.00")
    self.remarks.set("")


PurchaseWindow.load_suppliers = load_suppliers
PurchaseWindow.supplier_selected = supplier_selected
PurchaseWindow.product_selected = product_selected
PurchaseWindow.calculate_amount = calculate_amount
PurchaseWindow.save_purchase = save_purchase
PurchaseWindow.clear_form = clear_form