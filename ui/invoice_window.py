"""
invoice_window.py

Invoice/Billing Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.base_window import BaseWindow

from modules.invoice.invoice_manager import InvoiceManager
from utils.invoice_export import InvoiceExporter


class InvoiceWindow(BaseWindow):

    def __init__(self, parent, title="New Invoice", show_header=True):

        super().__init__(
            parent,
            title,
            show_header=show_header
        )

        self.invoice_items = []

        self.customer = None
        self.selected_product = None

    # ==========================================================
    # Toolbar
    # ==========================================================

    def create_toolbar(self):

        super().create_toolbar()

        ttk.Button(
            self.toolbar,
            text="New Invoice",
            command=self.new_invoice
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            self.toolbar,
            text="Save Invoice",
            command=self.save_invoice
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            self.toolbar,
            text="Print",
            command=self.print_invoice
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            self.toolbar,
            text="Clear",
            command=self.clear_invoice
        ).pack(
            side="left",
            padx=5
        )

    # ==========================================================
    # Content
    # ==========================================================

    def create_content(self):

        self.content = ttk.Frame(self)

        self.content.pack(
            fill="both",
            expand=True,
            padx=10
        )

        self.create_customer_section()

        self.create_product_section()

        self.create_invoice_table()

        self.create_total_section()

    # ==========================================================
    # Customer
    # ==========================================================

    def create_customer_section(self):

        frame = ttk.LabelFrame(
            self.content,
            text="Customer Information",
            padding=10
        )

        frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            frame,
            text="Customer"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.customer_name = ttk.Entry(
            frame,
            width=35
        )

        self.customer_name.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            frame,
            text="Search",
            command=self.search_customer
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Label(
            frame,
            text="Phone"
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        self.phone = ttk.Entry(
            frame,
            width=20
        )

        self.phone.grid(
            row=0,
            column=4,
            padx=5
        )

    # ==========================================================
    # Product
    # ==========================================================

    def create_product_section(self):

        frame = ttk.LabelFrame(
            self.content,
            text="Add Product",
            padding=10
        )

        frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            frame,
            text="Product"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.product_name = ttk.Entry(
            frame,
            width=35
        )

        self.product_name.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            frame,
            text="Search",
            command=self.search_product
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Label(
            frame,
            text="Qty"
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        self.qty = ttk.Entry(
            frame,
            width=10
        )

        self.qty.insert(
            0,
            "1"
        )

        self.qty.grid(
            row=0,
            column=4,
            padx=5
        )

        ttk.Button(
            frame,
            text="Add Item",
            command=self.add_item
        ).grid(
            row=0,
            column=5,
            padx=10
        )

    # ==========================================================
    # Invoice Table
    # ==========================================================

    def create_invoice_table(self):

        frame = ttk.Frame(
            self.content
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "Product",
            "Color",
            "Size",
            "Qty",
            "Rate",
            "GST",
            "Amount"
        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=12
        )

        widths = [
            250,
            120,
            80,
            70,
            100,
            80,
            120
        ]

        for col, width in zip(
            columns,
            widths
        ):

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
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

        self.tree.bind(
            "<Delete>",
            lambda event: self.remove_selected_item()
        )

    # ==========================================================
    # Totals
    # ==========================================================

    def create_total_section(self):

        frame = ttk.LabelFrame(
            self.content,
            text="Invoice Summary",
            padding=10
        )

        frame.pack(
            fill="x",
            pady=10
        )

        self.subtotal = tk.StringVar(
            value="0.00"
        )

        self.gst = tk.StringVar(
            value="0.00"
        )

        self.discount = tk.StringVar(
            value="0.00"
        )

        self.total = tk.StringVar(
            value="0.00"
        )

        ttk.Label(
            frame,
            text="Subtotal"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.subtotal
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        ttk.Label(
            frame,
            text="GST"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.gst
        ).grid(
            row=1,
            column=1,
            sticky="e"
        )

        ttk.Label(
            frame,
            text="Discount"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        discount_entry = ttk.Entry(
            frame,
            textvariable=self.discount,
            width=12
        )

        discount_entry.grid(
            row=2,
            column=1,
            sticky="e"
        )

        discount_entry.bind(
            "<KeyRelease>",
            lambda event: self.calculate_totals()
        )

        ttk.Separator(
            frame,
            orient="horizontal"
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=8
        )

        ttk.Label(
            frame,
            text="Grand Total",
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).grid(
            row=4,
            column=0,
            sticky="w"
        )

        ttk.Label(
            frame,
            textvariable=self.total,
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).grid(
            row=4,
            column=1,
            sticky="e"
        )

    # ==========================================================
    # Calculate Totals
    # ==========================================================

    def calculate_totals(self):

        subtotal = 0

        gst_total = 0

        for item in self.invoice_items:

            amount = (
                float(item["Quantity"])
                * float(item["Rate"])
            )

            subtotal += amount

            gst_total += (
                amount
                * float(item["GST %"])
                / 100
            )

        try:

            discount = float(
                self.discount.get()
            )

        except (
            ValueError,
            TypeError
        ):

            discount = 0

        if discount < 0:

            discount = 0

        grand_total = (
            subtotal
            + gst_total
            - discount
        )

        if grand_total < 0:

            grand_total = 0

        self.subtotal.set(
            f"{subtotal:.2f}"
        )

        self.gst.set(
            f"{gst_total:.2f}"
        )

        self.total.set(
            f"{grand_total:.2f}"
        )

    # ==========================================================
    # New Invoice
    # ==========================================================

    def new_invoice(self):

        if messagebox.askyesno(
            "New Invoice",
            "Clear current invoice?"
        ):

            self.clear_invoice()

    # ==========================================================
    # Remove Selected Item
    # ==========================================================

    def remove_selected_item(self):

        selected = self.tree.selection()

        if not selected:

            return

        index = self.tree.index(
            selected[0]
        )

        if 0 <= index < len(
            self.invoice_items
        ):

            del self.invoice_items[
                index
            ]

        self.refresh_table()

    # ==========================================================
    # Save Invoice
    # ==========================================================

    def save_invoice(self):

        # --------------------------------------------------
        # Customer validation
        # --------------------------------------------------

        if not self.customer:

            messagebox.showwarning(
                "Customer",
                "Please select a customer."
            )

            return

        # --------------------------------------------------
        # Item validation
        # --------------------------------------------------

        if len(self.invoice_items) == 0:

            messagebox.showwarning(
                "Invoice",
                "Please add at least one product."
            )

            return

        # --------------------------------------------------
        # Discount
        # --------------------------------------------------

        try:

            discount = float(
                self.discount.get()
            )

        except (
            ValueError,
            TypeError
        ):

            messagebox.showerror(
                "Discount",
                "Invalid discount."
            )

            return

        if discount < 0:

            messagebox.showerror(
                "Discount",
                "Discount cannot be negative."
            )

            return

        # --------------------------------------------------
        # Payment
        # --------------------------------------------------

        payment_mode = "Cash"

        payment_status = "Paid"

        # --------------------------------------------------
        # Invoice Manager
        # --------------------------------------------------

        manager = InvoiceManager()

        try:

            success, result = (
                manager.create_invoice(
                    customer=self.customer,
                    items=self.invoice_items,
                    payment_mode=payment_mode,
                    payment_status=payment_status,
                    discount=discount
                )
            )

        except Exception as e:

            messagebox.showerror(
                "Invoice Error",
                f"Unable to save invoice.\n\n{e}"
            )

            return

        # --------------------------------------------------
        # Successful Invoice
        # --------------------------------------------------

        if success:

            invoice_number = result

            # ----------------------------------------------
            # Get saved invoice
            # ----------------------------------------------

            invoice = manager.get_invoice(
                invoice_number
            )

            items = manager.get_invoice_items(
                invoice_number
            )

            pdf_path = ""

            excel_path = ""

            # ----------------------------------------------
            # Generate PDF
            # ----------------------------------------------

            try:

                pdf_path = (
                    InvoiceExporter.export_pdf(
                        invoice,
                        items
                    )
                )

            except Exception as e:

                messagebox.showwarning(
                    "PDF Export",
                    f"Invoice saved, but PDF "
                    f"could not be generated.\n\n{e}"
                )

            # ----------------------------------------------
            # Generate Excel
            # ----------------------------------------------

            try:

                excel_path = (
                    InvoiceExporter.export_excel(
                        invoice,
                        items
                    )
                )

            except Exception as e:

                messagebox.showwarning(
                    "Excel Export",
                    f"Invoice saved, but Excel "
                    f"file could not be generated.\n\n{e}"
                )

            # ----------------------------------------------
            # Update invoice file paths
            # ----------------------------------------------

            update_data = {}

            if pdf_path:

                update_data[
                    "PDF Path"
                ] = pdf_path

            if excel_path:

                update_data[
                    "Excel Path"
                ] = excel_path

            if update_data:

                try:

                    manager.db.update_record(
                        "Invoices",
                        "Invoice Number",
                        invoice_number,
                        update_data
                    )

                except Exception:
                    pass

            # ----------------------------------------------
            # Success Message
            # ----------------------------------------------

            message = (
                f"Invoice {invoice_number} "
                f"created successfully."
            )

            if pdf_path:

                message += (
                    f"\n\nPDF:\n{pdf_path}"
                )

            if excel_path:

                message += (
                    f"\n\nExcel:\n{excel_path}"
                )

            messagebox.showinfo(
                "Invoice Saved",
                message
            )

            self.clear_invoice()

        else:

            messagebox.showerror(
                "Error",
                str(result)
            )

    # ==========================================================
    # Print Invoice
    # ==========================================================

    def print_invoice(self):

        if not self.customer:

            messagebox.showwarning(
                "Customer",
                "Please select a customer."
            )

            return

        if not self.invoice_items:

            messagebox.showwarning(
                "Invoice",
                "Please add at least one product."
            )

            return

        try:

            discount = float(
                self.discount.get()
            )

        except (
            ValueError,
            TypeError
        ):

            discount = 0

        # --------------------------------------------------
        # Generate temporary invoice data
        # --------------------------------------------------

        manager = InvoiceManager()

        subtotal = 0

        gst_total = 0

        for item in self.invoice_items:

            amount = (
                float(item["Quantity"])
                * float(item["Rate"])
            )

            subtotal += amount

            gst_total += (
                amount
                * float(item["GST %"])
                / 100
            )

        grand_total = (
            subtotal
            + gst_total
            - discount
        )

        invoice = {

            "Invoice Number":
                "PREVIEW",

            "Invoice Date":
                "",

            "Invoice Time":
                "",

            "Customer ID":
                self.customer.get(
                    "Customer ID",
                    ""
                ),

            "Customer Name":
                self.customer.get(
                    "Customer Name",
                    ""
                ),

            "Phone Number":
                self.customer.get(
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
                "Cash",

            "Payment Status":
                "Paid"
        }

        try:

            path = (
                InvoiceExporter.export_pdf(
                    invoice,
                    self.invoice_items
                )
            )

            messagebox.showinfo(
                "Print",
                f"PDF invoice generated.\n\n"
                f"{path}\n\n"
                f"Open the PDF and print it."
            )

        except Exception as e:

            messagebox.showerror(
                "Print Error",
                f"Unable to generate invoice PDF.\n\n{e}"
            )

    # ==========================================================
    # Clear Invoice
    # ==========================================================

    def clear_invoice(self):

        self.invoice_items.clear()

        self.tree.delete(
            *self.tree.get_children()
        )

        self.customer = None

        self.selected_product = None

        self.customer_name.delete(
            0,
            "end"
        )

        self.phone.delete(
            0,
            "end"
        )

        self.product_name.delete(
            0,
            "end"
        )

        self.qty.delete(
            0,
            "end"
        )

        self.qty.insert(
            0,
            "1"
        )

        self.subtotal.set(
            "0.00"
        )

        self.gst.set(
            "0.00"
        )

        self.discount.set(
            "0.00"
        )

        self.total.set(
            "0.00"
        )

    # ==========================================================
    # Search Customer
    # ==========================================================

    def search_customer(self):

        from ui.customer_search_dialog import (
            CustomerSearchDialog
        )

        dialog = CustomerSearchDialog(
            self
        )

        self.wait_window(
            dialog
        )

        if dialog.selected_customer:

            customer = (
                dialog.selected_customer
            )

            self.customer = customer

            self.customer_name.delete(
                0,
                "end"
            )

            self.customer_name.insert(
                0,
                customer.get(
                    "Customer Name",
                    ""
                )
            )

            self.phone.delete(
                0,
                "end"
            )

            self.phone.insert(
                0,
                customer.get(
                    "Phone Number",
                    ""
                )
            )

    # ==========================================================
    # Search Product
    # ==========================================================

    def search_product(self):

        from ui.product_search_dialog import (
            ProductSearchDialog
        )

        dialog = ProductSearchDialog(
            self
        )

        self.wait_window(
            dialog
        )

        if dialog.selected_product:

            product = (
                dialog.selected_product
            )

            self.selected_product = product

            self.product_name.delete(
                0,
                "end"
            )

            self.product_name.insert(
                0,
                product.get(
                    "Product Name",
                    ""
                )
            )

            self.qty.focus()

    # ==========================================================
    # Add Item
    # ==========================================================

    def add_item(self):

        if not self.selected_product:

            messagebox.showwarning(
                "Product",
                "Please select a product."
            )

            return

        try:

            qty = float(
                self.qty.get()
            )

        except (
            ValueError,
            TypeError
        ):

            messagebox.showerror(
                "Quantity",
                "Invalid quantity."
            )

            return

        if qty <= 0:

            messagebox.showerror(
                "Quantity",
                "Quantity must be greater than zero."
            )

            return

        product = (
            self.selected_product
        )

        # --------------------------------------------------
        # Stock validation
        # --------------------------------------------------

        try:

            stock = float(
                product.get(
                    "Stock",
                    0
                )
            )

        except (
            ValueError,
            TypeError
        ):

            messagebox.showerror(
                "Stock",
                "Invalid product stock."
            )

            return

        # --------------------------------------------------
        # Check quantity already added
        # --------------------------------------------------

        existing_quantity = 0

        for item in self.invoice_items:

            if (
                item["Product ID"]
                == product["Product ID"]
            ):

                existing_quantity = float(
                    item["Quantity"]
                )

                break

        total_requested = (
            existing_quantity + qty
        )

        if total_requested > stock:

            messagebox.showerror(
                "Stock",
                f"Only {stock} item(s) available.\n\n"
                f"Already added: {existing_quantity}\n"
                f"Trying to add: {qty}"
            )

            return

        # --------------------------------------------------
        # Duplicate Product
        # --------------------------------------------------

        for item in self.invoice_items:

            if (
                item["Product ID"]
                == product["Product ID"]
            ):

                item["Quantity"] += qty

                self.refresh_table()

                return

        # --------------------------------------------------
        # Add New Item
        # --------------------------------------------------

        try:

            rate = float(
                product.get(
                    "Rate",
                    0
                )
            )

            gst_percent = float(
                product.get(
                    "GST %",
                    0
                )
            )

        except (
            ValueError,
            TypeError
        ):

            messagebox.showerror(
                "Product",
                "Invalid product rate or GST."
            )

            return

        item = {

            "Product ID":
                product.get(
                    "Product ID",
                    ""
                ),

            "Thread Type":
                product.get(
                    "Thread Type",
                    ""
                ),

            "Product Name":
                product.get(
                    "Product Name",
                    ""
                ),

            "Color":
                product.get(
                    "Color",
                    ""
                ),

            "Shade Number":
                product.get(
                    "Shade Number",
                    ""
                ),

            "Size":
                product.get(
                    "Size",
                    ""
                ),

            "Unit":
                product.get(
                    "Unit",
                    ""
                ),

            "Quantity":
                qty,

            "Rate":
                rate,

            "GST %":
                gst_percent
        }

        self.invoice_items.append(
            item
        )

        # IMPORTANT:
        # Refresh table immediately after
        # adding the item.

        self.refresh_table()

    # ==========================================================
    # Refresh Table
    # ==========================================================

    def refresh_table(self):

        self.tree.delete(
            *self.tree.get_children()
        )

        for item in self.invoice_items:

            amount = (
                float(item["Quantity"])
                * float(item["Rate"])
            )

            gst = (
                amount
                * float(item["GST %"])
                / 100
            )

            total = (
                amount
                + gst
            )

            self.tree.insert(
                "",
                "end",
                values=(

                    item.get(
                        "Product Name",
                        ""
                    ),

                    item.get(
                        "Color",
                        ""
                    ),

                    item.get(
                        "Size",
                        ""
                    ),

                    item.get(
                        "Quantity",
                        0
                    ),

                    f"{float(item.get('Rate', 0)):.2f}",

                    f"{float(item.get('GST %', 0))}%",

                    f"{total:.2f}"
                )
            )

        self.calculate_totals()