"""
invoice_history_window.py

Invoice History Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modules.invoice.invoice_manager import InvoiceManager
from utils.invoice_export import InvoiceExporter


class InvoiceHistoryWindow(ttk.Frame):

    def __init__(self, parent, on_close=None):

        super().__init__(parent)

        self.on_close = on_close or self.destroy

        self.manager = InvoiceManager()
        self.search_var = tk.StringVar()

        self.create_widgets()
        self.pack(fill="both", expand=True)
        self.load_invoices()

    def header_subtitle(self):

        return "Search, review, and export invoice records from one polished view."

    def header_actions(self):

        return [
            ("Refresh", self.load_invoices, "Ghost.TButton"),
            ("View Invoice", self.view_invoice, "Outline.TButton"),
            ("Export PDF", self.export_pdf, "Outline.TButton"),
            ("Export Excel", self.export_excel, "Outline.TButton"),
            ("Close", self.close_window, "Accent.TButton"),
        ]

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        main = ttk.Frame(
            self,
            style="Content.TFrame",
            padding=18
        )

        main.pack(fill="both", expand=True)

        search_card = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=16
        )

        search_card.pack(fill="x", pady=(0, 16))

        ttk.Label(
            search_card,
            text="Search",
            style="CardSection.TLabel"
        ).pack(anchor="w")

        search_row = ttk.Frame(search_card, style="Card.TFrame")
        search_row.pack(fill="x", pady=(8, 0))

        search_entry = ttk.Entry(
            search_row,
            textvariable=self.search_var,
            width=40
        )

        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", self.search_invoices)

        ttk.Label(
            search_row,
            text="Filter by invoice, customer, phone, or status.",
            style="CardMuted.TLabel"
        ).pack(side="right", padx=(12, 0))

        summary_row = ttk.Frame(main, style="Content.TFrame")
        summary_row.pack(fill="x", pady=(0, 16))
        summary_row.columnconfigure(0, weight=1, uniform="summary")
        summary_row.columnconfigure(1, weight=1, uniform="summary")

        count_card = ttk.Frame(summary_row, style="Card.TFrame", padding=18)
        count_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(
            count_card,
            text="Invoices",
            style="CardSection.TLabel"
        ).pack(anchor="w")

        self.invoice_count_label = ttk.Label(
            count_card,
            text="0",
            style="Card.TLabel",
            font=("Segoe UI", 20, "bold")
        )

        self.invoice_count_label.pack(anchor="w", pady=(8, 0))

        sales_card = ttk.Frame(summary_row, style="Card.TFrame", padding=18)
        sales_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(
            sales_card,
            text="Total Sales",
            style="CardSection.TLabel"
        ).pack(anchor="w")

        self.sales_label = ttk.Label(
            sales_card,
            text="₹0.00",
            style="Card.TLabel",
            font=("Segoe UI", 20, "bold")
        )

        self.sales_label.pack(anchor="w", pady=(8, 0))

        table_card = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=12
        )

        table_card.pack(fill="both", expand=True)

        columns = (
            "Invoice Number",
            "Invoice Date",
            "Invoice Time",
            "Customer Name",
            "Phone Number",
            "Subtotal",
            "Discount",
            "GST",
            "Grand Total",
            "Payment Mode",
            "Payment Status"
        )

        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )

        widths = {
            "Invoice Number": 120,
            "Invoice Date": 100,
            "Invoice Time": 90,
            "Customer Name": 180,
            "Phone Number": 120,
            "Subtotal": 100,
            "Discount": 90,
            "GST": 90,
            "Grand Total": 110,
            "Payment Mode": 110,
            "Payment Status": 120
        }

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=widths[column], anchor="center")

        vertical_scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_card,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        table_card.rowconfigure(0, weight=1)
        table_card.columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", lambda event: self.view_invoice())

    # =====================================================
    # LOAD
    # =====================================================

    def load_invoices(self):

        self.search_var.set("")

        invoices = self.manager.get_all_invoices()
        self.display_invoices(invoices)

    # =====================================================
    # DISPLAY
    # =====================================================

    def display_invoices(self, invoices):

        self.tree.delete(*self.tree.get_children())

        total_sales = 0

        for invoice in invoices:

            try:
                subtotal = float(invoice.get("Subtotal", 0))
                discount = float(invoice.get("Discount", 0))
                gst = float(invoice.get("GST", 0))
                grand_total = float(invoice.get("Grand Total", 0))
            except (ValueError, TypeError):
                subtotal = 0
                discount = 0
                gst = 0
                grand_total = 0

            total_sales += grand_total

            self.tree.insert(
                "",
                "end",
                values=(
                    invoice.get("Invoice Number", ""),
                    invoice.get("Invoice Date", ""),
                    invoice.get("Invoice Time", ""),
                    invoice.get("Customer Name", ""),
                    invoice.get("Phone Number", ""),
                    f"{subtotal:.2f}",
                    f"{discount:.2f}",
                    f"{gst:.2f}",
                    f"{grand_total:.2f}",
                    invoice.get("Payment Mode", ""),
                    invoice.get("Payment Status", "")
                )
            )

        self.invoice_count_label.config(text=str(len(invoices)))
        self.sales_label.config(text=f"₹{total_sales:.2f}")

    # =====================================================
    # SEARCH
    # =====================================================

    def search_invoices(self, event=None):

        keyword = self.search_var.get().strip()

        if not keyword:
            self.load_invoices()
            return

        invoices = self.manager.search_invoice(keyword)
        self.display_invoices(invoices)

    # =====================================================
    # VIEW INVOICE
    # =====================================================

    def view_invoice(self):

        invoice, items = self.get_selected_invoice()

        if not invoice:
            return

        details = (
            f"Invoice: {invoice.get('Invoice Number', '')}\n"
            f"Date: {invoice.get('Invoice Date', '')}\n"
            f"Customer: {invoice.get('Customer Name', '')}\n"
            f"Phone: {invoice.get('Phone Number', '')}\n"
            f"Subtotal: ₹{invoice.get('Subtotal', 0)}\n"
            f"Discount: ₹{invoice.get('Discount', 0)}\n"
            f"GST: ₹{invoice.get('GST', 0)}\n"
            f"Grand Total: ₹{invoice.get('Grand Total', 0)}\n"
            f"Payment: {invoice.get('Payment Mode', '')}\n"
            f"Status: {invoice.get('Payment Status', '')}\n"
            f"\nItems: {len(items)}"
        )

        messagebox.showinfo("Invoice Details", details)

    def get_selected_invoice(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Selection", "Select an invoice first.")
            return None, None

        values = self.tree.item(selected[0], "values")
        invoice_number = values[0]

        invoice = self.manager.get_invoice(invoice_number)

        if not invoice:
            messagebox.showerror("Error", "Invoice not found.")
            return None, None

        items = self.manager.get_invoice_items(invoice_number)
        return invoice, items

    # =====================================================
    # EXPORT PDF
    # =====================================================

    def export_pdf(self):

        invoice, items = self.get_selected_invoice()

        if not invoice:
            return

        try:
            path = InvoiceExporter.export_pdf(invoice, items)
            messagebox.showinfo(
                "Success",
                f"PDF invoice created successfully.\n\nLocation:\n{path}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Unable to create PDF.\n\n{e}")

    # =====================================================
    # EXPORT EXCEL
    # =====================================================

    def export_excel(self):

        invoice, items = self.get_selected_invoice()

        if not invoice:
            return

        try:
            path = InvoiceExporter.export_excel(invoice, items)
            messagebox.showinfo(
                "Success",
                f"Excel invoice created successfully.\n\nLocation:\n{path}"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Unable to create Excel invoice.\n\n{e}")

    def close_window(self):

        self.on_close()
