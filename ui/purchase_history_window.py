"""
purchase_history_window.py

Purchase History Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modules.purchase.purchase_manager import PurchaseManager


class PurchaseHistoryWindow(ttk.Frame):

    def __init__(self, parent, on_close=None):

        super().__init__(parent)

        self.on_close = on_close or self.destroy

        self.manager = PurchaseManager()

        self.create_widgets()

        self.pack(fill="both", expand=True)

        self.load_purchases()

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
            text="Purchase History",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=(0, 15)
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
            width=40
        )

        search_entry.pack(
            side="left",
            padx=10
        )

        search_entry.bind(
            "<KeyRelease>",
            self.search
        )

        ttk.Button(
            search_frame,
            text="Refresh",
            command=self.load_purchases
        ).pack(
            side="left",
            padx=5
        )

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        table_frame = ttk.Frame(main)

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "Purchase ID",
            "Purchase Date",
            "Supplier Name",
            "Supplier Phone",
            "Product ID",
            "Product Name",
            "Quantity",
            "Purchase Rate",
            "Amount",
            "Remarks"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "Purchase ID": 110,
            "Purchase Date": 100,
            "Supplier Name": 150,
            "Supplier Phone": 120,
            "Product ID": 100,
            "Product Name": 160,
            "Quantity": 80,
            "Purchase Rate": 100,
            "Amount": 100,
            "Remarks": 180
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

        # -------------------------------------------------
        # Scrollbars
        # -------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
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
        # Summary
        # -------------------------------------------------

        summary_frame = ttk.Frame(main)

        summary_frame.pack(
            fill="x",
            pady=10
        )

        self.count_label = ttk.Label(
            summary_frame,
            text="Purchases: 0",
            font=("Segoe UI", 11, "bold")
        )

        self.count_label.pack(
            side="left",
            padx=10
        )

        self.total_label = ttk.Label(
            summary_frame,
            text="Total Purchase: ₹0.00",
            font=("Segoe UI", 11, "bold")
        )

        self.total_label.pack(
            side="right",
            padx=10
        )

        # -------------------------------------------------
        # Close
        # -------------------------------------------------

        ttk.Button(
            main,
            text="Close",
            command=self.close_window
        ).pack(
            pady=5
        )

    def close_window(self):

        self.on_close()

    # =====================================================
    # LOAD PURCHASES
    # =====================================================

    def load_purchases(self):

        self.search_var.set("")

        purchases = (
            self.manager
            .get_all_purchases()
        )

        self.display_purchases(
            purchases
        )

    # =====================================================
    # DISPLAY
    # =====================================================

    def display_purchases(
        self,
        purchases
    ):

        self.tree.delete(
            *self.tree.get_children()
        )

        total = 0

        for purchase in purchases:

            try:

                amount = float(
                    purchase.get(
                        "Amount",
                        0
                    )
                )

            except (
                ValueError,
                TypeError
            ):

                amount = 0

            total += amount

            self.tree.insert(
                "",
                "end",
                values=(
                    purchase.get(
                        "Purchase ID",
                        ""
                    ),
                    purchase.get(
                        "Purchase Date",
                        ""
                    ),
                    purchase.get(
                        "Supplier Name",
                        ""
                    ),
                    purchase.get(
                        "Supplier Phone",
                        ""
                    ),
                    purchase.get(
                        "Product ID",
                        ""
                    ),
                    purchase.get(
                        "Product Name",
                        ""
                    ),
                    purchase.get(
                        "Quantity",
                        ""
                    ),
                    f"{float(purchase.get('Purchase Rate', 0)):.2f}",
                    f"{amount:.2f}",
                    purchase.get(
                        "Remarks",
                        ""
                    )
                )
            )

        self.count_label.config(
            text=f"Purchases: {len(purchases)}"
        )

        self.total_label.config(
            text=f"Total Purchase: ₹{total:.2f}"
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search(self, event=None):

        keyword = (
            self.search_var
            .get()
            .strip()
        )

        if not keyword:

            self.load_purchases()

            return

        purchases = (
            self.manager
            .search_purchase(
                keyword
            )
        )

        self.display_purchases(
            purchases
        )