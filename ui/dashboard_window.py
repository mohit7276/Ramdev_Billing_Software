"""
dashboard_window.py

Main Dashboard Window
Ramdev Billing Software
"""

import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from ui.purchase_window import PurchaseWindow
from ui.purchase_history_window import PurchaseHistoryWindow
from ui.invoice_history_window import InvoiceHistoryWindow
from ui.supplier_window import SupplierWindow
from ui.invoice_window import InvoiceWindow
from ui.customer_window import CustomerWindow
from ui.product_window import ProductWindow
from ui.report_window import ReportWindow
from ui.settings_window import SettingsWindow

from modules.reports.report_manager import ReportManager
from ui.theme import PRIMARY, SURFACE, TEXT, TEXT_LIGHT


class DashboardWindow:

    def __init__(self, root, user):

        self.root = root
        self.user = user
        self.report_manager = ReportManager()

        self.root.title("Ramdev Billing Software")
        self.root.geometry("1440x860")
        self.root.minsize(1280, 760)
        self.root.state("zoomed")

        self.build_ui()

    # ==========================================================
    # UI
    # ==========================================================

    def build_ui(self):

        self.shell = ttk.Frame(
            self.root,
            style="Content.TFrame",
            padding=18
        )

        self.shell.pack(fill="both", expand=True)

        self.shell.rowconfigure(0, weight=1)
        self.shell.columnconfigure(0, weight=0)
        self.shell.columnconfigure(1, weight=1)

        self.create_sidebar()

        self.create_dashboard()

    # ==========================================================
    # Sidebar
    # ==========================================================

    def create_sidebar(self):

        sidebar = ttk.Frame(
            self.shell,
            style="Sidebar.TFrame",
            width=290,
            padding=22
        )

        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        sidebar.grid_propagate(False)

        brand = ttk.Frame(sidebar, style="Sidebar.TFrame")
        brand.pack(fill="x", pady=(0, 24))

        ttk.Label(
            brand,
            text="Ramdev Billing",
            style="Sidebar.TLabel",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        ttk.Label(
            brand,
            text=f"Welcome, {self.user['Username']}",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(6, 0))

        ttk.Label(
            sidebar,
            text="Navigation",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 10))

        main_buttons = [

            ("Dashboard", self.show_dashboard),

            ("New Invoice", self.open_invoice),

            ("Purchase Entry", self.open_purchase),

            ("Invoice History", self.open_invoice_history),

            ("Purchase History", self.open_purchase_history),

            ("Customers", self.open_customers),

            ("Products", self.open_products),

            ("Suppliers", self.open_suppliers),

            ("Reports", self.open_reports),

            ("Settings", self.open_settings)

        ]

        self.sidebar_nav_items = []

        for text, command in main_buttons:

            item = self.create_sidebar_nav_item(sidebar, text, command)
            item.pack(fill="x", pady=3)
            self.sidebar_nav_items.append(item)

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", pady=18)

        ttk.Label(
            sidebar,
            text="Session",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.create_sidebar_nav_item(
            sidebar,
            "Logout",
            self.logout,
            active=False,
            hover=False
        ).pack(fill="x")

        footer = ttk.Frame(sidebar, style="Sidebar.TFrame")
        footer.pack(fill="x", side="bottom", pady=(24, 0))

        ttk.Label(
            footer,
            text="Clean workspace\nFast billing flow",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 9),
            justify="left"
        ).pack(anchor="w")

    def create_sidebar_nav_item(self, parent, text, command, active=False, hover=True):

        container = tk.Frame(
            parent,
            bg="#111C34" if active else "#0F172A",
            highlightthickness=0,
            bd=0
        )

        indicator = tk.Frame(
            container,
            bg="#2563EB" if active else container.cget("bg"),
            width=4,
            height=28,
            bd=0,
            highlightthickness=0
        )

        indicator.pack(side="left", fill="y")

        label = tk.Label(
            container,
            text=text,
            bg=container.cget("bg"),
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=14,
            pady=10,
            cursor="hand2"
        )

        label.pack(side="left", fill="x", expand=True)

        def activate(event=None):
            command()

        def on_enter(event):
            if hover:
                container.configure(bg="#111C34")
                indicator.configure(bg="#60A5FA" if not active else "#2563EB")
                label.configure(bg="#111C34")

        def on_leave(event):
            if hover:
                container.configure(bg="#111C34" if active else "#0F172A")
                indicator.configure(bg="#2563EB" if active else container.cget("bg"))
                label.configure(bg=container.cget("bg"))

        label.bind("<Button-1>", activate)
        container.bind("<Button-1>", activate)

        if hover:
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            container.bind("<Enter>", on_enter)
            container.bind("<Leave>", on_leave)

        return container

    # ==========================================================
    # Main Area
    # ==========================================================

    def create_dashboard(self):

        self.content = ttk.Frame(
            self.shell,
            style="Content.TFrame"
        )

        self.content.grid(row=0, column=1, sticky="nsew")

        self.content.columnconfigure(0, weight=1)

        self.show_dashboard()

    # ==========================================================
    # Dashboard
    # ==========================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        stats = self.report_manager.dashboard_summary()

        hero = ttk.Frame(
            self.content,
            style="Card.TFrame",
            padding=20
        )

        hero.pack(fill="x", pady=(0, 16))

        hero.columnconfigure(0, weight=1)
        hero.columnconfigure(1, weight=0)

        left = ttk.Frame(hero, style="Card.TFrame")
        left.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            left,
            text="Dashboard Overview",
            bg=SURFACE,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Track sales, stock pressure, customers, and billing activity from a cleaner workspace.",
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10),
            wraplength=720,
            justify="left"
        ).pack(anchor="w", pady=(6, 0))

        tk.Label(
            left,
            text=f"Session user: {self.user['Username']}",
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(12, 0))

        right = ttk.Frame(hero, style="Card.TFrame")
        right.grid(row=0, column=1, sticky="ne", padx=(16, 0))

        tk.Label(
            right,
            text=date.today().strftime("%d %b %Y"),
            bg=SURFACE,
            fg=PRIMARY,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="e")

        tk.Label(
            right,
            text="Today",
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10)
        ).pack(anchor="e", pady=(4, 0))

        cards = ttk.Frame(
            self.content,
            style="Content.TFrame"
        )

        cards.pack(fill="x", pady=(0, 16))

        for index in range(3):
            cards.columnconfigure(index, weight=1, uniform="card")

        items = [

            ("Total Sales", f"₹ {stats['total_sales']}"),

            ("Invoices", stats["total_invoices"]),

            ("Customers", stats["total_customers"]),

            ("Products", stats["total_products"]),

            ("Low Stock", stats["low_stock_products"]),

            ("GST Collected", f"₹ {stats['total_gst']}")

        ]

        row = 0
        col = 0

        accent_colors = ["#2563EB", "#0EA5E9", "#14B8A6", "#F59E0B", "#8B5CF6", "#22C55E"]

        for index, (title, value) in enumerate(items):

            card = ttk.Frame(
                cards,
                style="Card.TFrame",
                padding=18
            )

            card.grid(
                row=row,
                column=col,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            accent = tk.Frame(
                card,
                bg=accent_colors[index % len(accent_colors)],
                height=4,
                bd=0,
                highlightthickness=0
            )
            accent.pack(fill="x", side="top")

            tk.Label(
                card,
                text=title,
                bg=SURFACE,
                fg=PRIMARY,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w", pady=(14, 4))

            tk.Label(
                card,
                text=str(value),
                bg=SURFACE,
                fg=TEXT,
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w")

            hint = "Healthy" if title not in {"Low Stock"} else "Needs attention"

            tk.Label(
                card,
                text=hint,
                bg=SURFACE,
                fg=TEXT_LIGHT,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(4, 0))

            col += 1

            if col == 3:
                row += 1
                col = 0

        lower = ttk.Frame(self.content, style="Content.TFrame")
        lower.pack(fill="both", expand=True)

        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=1)

        actions = ttk.Frame(
            lower,
            style="Card.TFrame",
            padding=18
        )

        actions.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(
            actions,
            text="Quick Actions",
            bg=SURFACE,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            actions,
            text="Jump into the most common workflows without leaving the dashboard.",
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10),
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(6, 14))

        action_buttons = [
            ("New Invoice", self.open_invoice, "Accent.TButton"),
            ("Customer Management", self.open_customers, "Outline.TButton"),
            ("Product Management", self.open_products, "Outline.TButton"),
            ("Reports", self.open_reports, "Ghost.TButton"),
        ]

        for text, command, style_name in action_buttons:
            ttk.Button(
                actions,
                text=text,
                command=command,
                style=style_name
            ).pack(fill="x", pady=5)

        insight = ttk.Frame(
            lower,
            style="Card.TFrame",
            padding=18
        )

        insight.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        tk.Label(
            insight,
            text="Operational Snapshot",
            bg=SURFACE,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        note = "Inventory is under control."

        if stats["low_stock_products"]:
            note = f"{stats['low_stock_products']} product(s) need restocking soon."

        tk.Label(
            insight,
            text=note,
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10),
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(6, 12))

        tk.Label(
            insight,
            text="Use the sidebar to switch between invoices, purchase entry, history, and settings.",
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10),
            wraplength=400,
            justify="left"
        ).pack(anchor="w")

    # ==========================================================
    # Navigation
    # ==========================================================

    def open_invoice(self):

        self.show_module(
            InvoiceWindow,
            title="New Invoice",
            show_header=False
        )

    def open_purchase(self):

        self.show_module(
            PurchaseWindow,
            title="Purchase Entry",
            on_close=self.show_dashboard
        )

    def open_invoice_history(self):

        self.show_module(
            InvoiceHistoryWindow,
            title="Invoice History",
            on_close=self.show_dashboard
        )

    def open_purchase_history(self):

        self.show_module(
            PurchaseHistoryWindow,
            title="Purchase History",
            on_close=self.show_dashboard
        )

    def open_customers(self):

        self.show_module(
            CustomerWindow,
            title="Customer Management",
            show_header=False
        )

    def open_products(self):

        self.show_module(
            ProductWindow,
            title="Product Management",
            show_header=False
        )

    def open_suppliers(self):

        self.show_module(
            SupplierWindow,
            title="Supplier Management",
            on_close=self.show_dashboard
        )

    def open_reports(self):

        self.show_module(
            ReportWindow,
            title="Reports",
            show_header=False
        )

    def open_settings(self):

        self.show_module(
            SettingsWindow,
            title="Settings",
            show_header=False
        )

    def show_module(self, module_class, title="", **module_kwargs):

        self.clear_content()

        header = ttk.Frame(
            self.content,
            style="Card.TFrame",
            padding=18
        )

        header.pack(fill="x", pady=(0, 16))

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title_block = ttk.Frame(header, style="Card.TFrame")
        title_block.grid(row=0, column=0, sticky="w")

        header_subtitle = module_kwargs.pop(
            "header_subtitle",
            "Embedded module view"
        )

        tk.Label(
            title_block,
            text=title,
            bg=SURFACE,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text=header_subtitle,
            bg=SURFACE,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        header_actions = ttk.Frame(header, style="Card.TFrame")
        header_actions.grid(row=0, column=1, sticky="e")

        module_frame = ttk.Frame(
            self.content,
            style="Card.TFrame",
            padding=0
        )

        module_frame.pack(fill="both", expand=True)

        module_instance = module_class(module_frame, **module_kwargs)

        if hasattr(module_instance, "header_subtitle"):
            subtitle_value = module_instance.header_subtitle
            if callable(subtitle_value):
                header_subtitle = subtitle_value()
            elif subtitle_value:
                header_subtitle = subtitle_value

        actions = []

        if hasattr(module_instance, "header_actions"):
            actions = module_instance.header_actions() or []

        if actions:
            for text, command, style_name in actions:
                ttk.Button(
                    header_actions,
                    text=text,
                    command=command,
                    style=style_name
                ).pack(side="left", padx=(0, 8))

        ttk.Button(
            header_actions,
            text="Back to Dashboard",
            command=self.show_dashboard,
            style="Ghost.TButton"
        ).pack(side="left")

    # ==========================================================
    # Logout
    # ==========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:

            self.root.destroy()

            from ui.login_window import LoginWindow

            root = tk.Tk()

            LoginWindow(root)

            root.mainloop()
