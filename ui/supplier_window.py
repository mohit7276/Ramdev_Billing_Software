"""
supplier_window.py

Supplier Management Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modules.suppliers.supplier_manager import SupplierManager


class SupplierWindow(ttk.Frame):

    def __init__(self, parent, on_close=None):

        super().__init__(parent)

        self.on_close = on_close or self.destroy

        self.manager = SupplierManager()

        self.create_widgets()
        self.pack(fill="both", expand=True)
        self.load_suppliers()

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        main = ttk.Frame(
            self,
            padding=15
        )

        main.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        ttk.Label(
            main,
            text="Supplier Management",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=(0, 15)
        )

        # -------------------------------------------------
        # Form
        # -------------------------------------------------

        form = ttk.LabelFrame(
            main,
            text="Supplier Details",
            padding=15
        )

        form.pack(
            fill="x",
            pady=(0, 10)
        )

        ttk.Label(
            form,
            text="Supplier Name:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.name_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.name_var,
            width=35
        ).grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="Phone Number:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.phone_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.phone_var,
            width=25
        ).grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="GSTIN:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.gstin_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.gstin_var,
            width=35
        ).grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="Email:"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.email_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.email_var,
            width=25
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="Address:"
        ).grid(
            row=2,
            column=0,
            sticky="nw",
            padx=5,
            pady=5
        )

        self.address_var = tk.StringVar()

        ttk.Entry(
            form,
            textvariable=self.address_var,
            width=70
        ).grid(
            row=2,
            column=1,
            columnspan=3,
            sticky="w",
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        button_frame = ttk.Frame(form)

        button_frame.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Add Supplier",
            command=self.add_supplier
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.close_window
        ).pack(
            side="left",
            padx=5
        )

        # -------------------------------------------------
        # Search
        # -------------------------------------------------

        search_frame = ttk.Frame(main)

        search_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )

        search_entry.pack(
            side="left",
            padx=10
        )

        search_entry.bind(
            "<KeyRelease>",
            self.search_suppliers
        )

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        table_frame = ttk.Frame(main)

        table_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        columns = (
            "Supplier ID",
            "Supplier Name",
            "Phone Number",
            "Address",
            "GSTIN",
            "Email",
            "Created Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "Supplier ID": 100,
            "Supplier Name": 170,
            "Phone Number": 120,
            "Address": 220,
            "GSTIN": 150,
            "Email": 180,
            "Created Date": 100
        }

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # Delete
        # -------------------------------------------------

        ttk.Button(
            main,
            text="Delete Selected Supplier",
            command=self.delete_supplier
        ).pack(
            pady=5
        )

    def close_window(self):

        self.on_close()
        return

    
        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        table_frame = ttk.Frame(main)

        table_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        columns = (
            "Supplier ID",
            "Supplier Name",
            "Phone Number",
            "Address",
            "GSTIN",
            "Email",
            "Created Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "Supplier ID": 100,
            "Supplier Name": 170,
            "Phone Number": 120,
            "Address": 220,
            "GSTIN": 150,
            "Email": 180,
            "Created Date": 100
        }

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # Delete
        # -------------------------------------------------

        ttk.Button(
            main,
            text="Delete Selected Supplier",
            command=self.delete_supplier
        ).pack(
            pady=5
        )

        ttk.Button(
            search_frame,
            text="Refresh",
            command=self.load_suppliers
        ).pack(
            side="left"
        )

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        table_frame = ttk.Frame(main)

        table_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        columns = (
            "Supplier ID",
            "Supplier Name",
            "Phone Number",
            "Address",
            "GSTIN",
            "Email",
            "Created Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "Supplier ID": 100,
            "Supplier Name": 170,
            "Phone Number": 120,
            "Address": 220,
            "GSTIN": 150,
            "Email": 180,
            "Created Date": 100
        }

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # -------------------------------------------------
        # Delete
        # -------------------------------------------------

        ttk.Button(
            main,
            text="Delete Selected Supplier",
            command=self.delete_supplier
        ).pack(
            pady=5
        )

    # =====================================================
    # ADD
    # =====================================================

    def add_supplier(self):

        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        gstin = self.gstin_var.get().strip()
        email = self.email_var.get().strip()

        if not name:

            messagebox.showwarning(
                "Validation",
                "Enter supplier name."
            )

            return

        success, result = self.manager.add_supplier(
            supplier_name=name,
            phone=phone,
            address=address,
            gstin=gstin,
            email=email
        )

        if success:

            messagebox.showinfo(
                "Success",
                f"Supplier added successfully.\n\n"
                f"Supplier ID: {result}"
            )

            self.clear_form()
            self.load_suppliers()

        else:

            messagebox.showerror(
                "Error",
                str(result)
            )

    # =====================================================
    # LOAD
    # =====================================================

    def load_suppliers(self):

        self.search_var.set("")

        self.display_suppliers(
            self.manager.get_all_suppliers()
        )

    # =====================================================
    # DISPLAY
    # =====================================================

    def display_suppliers(self, suppliers):

        self.tree.delete(
            *self.tree.get_children()
        )

        for supplier in suppliers:

            self.tree.insert(
                "",
                "end",
                values=(
                    supplier.get(
                        "Supplier ID",
                        ""
                    ),
                    supplier.get(
                        "Supplier Name",
                        ""
                    ),
                    supplier.get(
                        "Phone Number",
                        ""
                    ),
                    supplier.get(
                        "Address",
                        ""
                    ),
                    supplier.get(
                        "GSTIN",
                        ""
                    ),
                    supplier.get(
                        "Email",
                        ""
                    ),
                    supplier.get(
                        "Created Date",
                        ""
                    )
                )
            )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_suppliers(self, event=None):

        keyword = (
            self.search_var
            .get()
            .strip()
        )

        if not keyword:

            self.load_suppliers()

            return

        results = (
            self.manager.search_suppliers(
                keyword
            )
        )

        self.display_suppliers(
            results
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_supplier(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection",
                "Select a supplier first."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        supplier_id = values[0]
        supplier_name = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete supplier '{supplier_name}'?"
        )

        if not confirm:

            return

        success = (
            self.manager.delete_supplier(
                supplier_id
            )
        )

        if success:

            messagebox.showinfo(
                "Deleted",
                "Supplier deleted successfully."
            )

            self.load_suppliers()

        else:

            messagebox.showerror(
                "Error",
                "Unable to delete supplier."
            )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_form(self):

        self.name_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.gstin_var.set("")
        self.email_var.set("")
