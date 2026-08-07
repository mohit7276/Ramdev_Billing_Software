"""
customer_window.py

Customer Management Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.base_window import BaseWindow
from modules.customers.customer_manager import CustomerManager


class CustomerWindow(BaseWindow):

    def __init__(self, parent, title="Customer Management", show_header=True):

        self.manager = CustomerManager()

        super().__init__(parent, title, show_header=show_header)

        self.load_customers()

    # ==========================================================
    # Toolbar
    # ==========================================================

    def create_toolbar(self):

        super().create_toolbar()

        ttk.Button(
            self.toolbar,
            text="Add Customer",
            command=self.add_customer
        ).pack(side="left", padx=5)

        ttk.Button(
            self.toolbar,
            text="Edit Customer",
            command=self.edit_customer
        ).pack(side="left", padx=5)

        ttk.Button(
            self.toolbar,
            text="Delete Customer",
            command=self.delete_customer
        ).pack(side="left", padx=5)

        ttk.Label(
            self.toolbar,
            text="Search:"
        ).pack(side="right")

        self.search_var = tk.StringVar()

        search = ttk.Entry(
            self.toolbar,
            textvariable=self.search_var,
            width=30
        )

        search.pack(side="right", padx=5)

        search.bind("<KeyRelease>", self.search_customer)

    # ==========================================================
    # Content
    # ==========================================================

    def create_content(self):

        self.content = ttk.Frame(self)

        self.content.pack(fill="both", expand=True, padx=15)

        columns = (
            "Customer ID",
            "Customer Name",
            "Phone Number",
            "GSTIN",
            "Email",
            "Created Date"
        )

        self.tree = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.tree.heading(column, text=column)

            self.tree.column(
                column,
                width=150,
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
    # Load Data
    # ==========================================================

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

                    customer["Email"],

                    customer["Created Date"]

                )
            )

        self.set_status(
            f"{len(customers)} customer(s)"
        )

    # ==========================================================
    # Search
    # ==========================================================

    def search_customer(self, event=None):

        keyword = self.search_var.get().strip()

        self.tree.delete(*self.tree.get_children())

        if keyword == "":

            customers = self.manager.get_all_customers()

        else:

            customers = self.manager.search_customers(
                keyword
            )

        for customer in customers:

            self.tree.insert(
                "",
                "end",
                values=(

                    customer["Customer ID"],

                    customer["Customer Name"],

                    customer["Phone Number"],

                    customer["GSTIN"],

                    customer["Email"],

                    customer["Created Date"]

                )
            )

        self.set_status(
            f"{len(customers)} customer(s)"
        )

    # ==========================================================
    # Selected Customer
    # ==========================================================

    def selected_customer(self):

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

    def add_customer(self):

        from ui.customer_dialog import CustomerDialog

        dialog = CustomerDialog(self)

        self.wait_window(dialog)

        if dialog.saved:
            self.load_customers()

    def edit_customer(self):

        customer_id = self.selected_customer()

        if not customer_id:

            messagebox.showwarning(
                "Warning",
                "Select a customer."
            )

            return

        customer = self.manager.get_customer(customer_id)

        from ui.customer_dialog import CustomerDialog

        dialog = CustomerDialog(
            self,
            customer
        )

        self.wait_window(dialog)

        if dialog.saved:
            self.load_customers()

    def delete_customer(self):

        customer_id = self.selected_customer()

        if not customer_id:

            messagebox.showwarning(
                "Warning",
                "Select a customer."
            )

            return

        answer = messagebox.askyesno(
            "Delete",
            "Delete selected customer?"
        )

        if not answer:
            return

        success = self.manager.delete_customer(
            customer_id
        )

        if success:

            self.load_customers()

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully."
            )

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete customer."
            )
