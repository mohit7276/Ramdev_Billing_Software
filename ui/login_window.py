"""
login_window.py

Login Window for
Ramdev Billing Software.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import (
    apply_theme,
    BACKGROUND,
    PRIMARY,
    SIDEBAR,
    SURFACE,
    TEXT_LIGHT,
)
from modules.auth.login_manager import LoginManager


class LoginWindow:

    def __init__(self, root):
        self.root = root
        apply_theme(self.root)
        self.root.title("Ramdev Billing Software - Login")
        self.root.geometry("920x560")
        self.root.minsize(860, 520)
        self.root.resizable(True, True)

        self.login_manager = LoginManager()

        self.build_ui()

    def build_ui(self):

        self.root.configure(bg=BACKGROUND)

        outer = ttk.Frame(
            self.root,
            style="Content.TFrame",
            padding=18
        )

        outer.pack(fill="both", expand=True)

        outer.columnconfigure(0, weight=1, uniform="login")
        outer.columnconfigure(1, weight=1, uniform="login")

        # -------------------------------------------------
        # Brand panel
        # -------------------------------------------------

        brand = ttk.Frame(
            outer,
            style="Sidebar.TFrame",
            padding=28
        )

        brand.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        ttk.Label(
            brand,
            text="Ramdev Billing Software",
            style="Sidebar.TLabel",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        ttk.Label(
            brand,
            text="A polished workspace for billing, stock control, and customer management.",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 11),
            wraplength=280,
            justify="left"
        ).pack(anchor="w", pady=(10, 28))

        for text in [
            "Fast invoice creation and printing",
            "Inventory, customers, and reports in one place",
            "Cleaner tables, cards, and navigation",
        ]:

            item = ttk.Frame(brand, style="Sidebar.TFrame")
            item.pack(fill="x", pady=8)

            marker = tk.Frame(
                item,
                width=10,
                height=10,
                bg=PRIMARY,
                bd=0,
                highlightthickness=0
            )
            marker.pack(side="left", padx=(0, 12), pady=5)

            ttk.Label(
                item,
                text=text,
                style="Sidebar.TLabel",
                font=("Segoe UI", 10, "bold")
            ).pack(side="left", anchor="w")

        footer = ttk.Label(
            brand,
            text="Built for a calm, professional workflow.",
            style="SidebarMuted.TLabel",
            font=("Segoe UI", 9)
        )

        footer.pack(anchor="w", pady=(28, 0))

        # -------------------------------------------------
        # Form panel
        # -------------------------------------------------

        form_panel = ttk.Frame(
            outer,
            style="Card.TFrame",
            padding=32
        )

        form_panel.grid(row=0, column=1, sticky="nsew")

        ttk.Label(
            form_panel,
            text="Welcome back",
            style="CardHeader.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            form_panel,
            text="Sign in to continue to the billing dashboard.",
            style="CardSubtitle.TLabel"
        ).pack(anchor="w", pady=(4, 18))

        card = ttk.Frame(
            form_panel,
            style="Card.TFrame"
        )

        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Username", style="CardSection.TLabel").pack(anchor="w")

        self.username_entry = ttk.Entry(
            card
        )
        self.username_entry.pack(fill="x", pady=(6, 14))

        ttk.Label(card, text="Password", style="CardSection.TLabel").pack(anchor="w")

        self.password_entry = ttk.Entry(
            card,
            show="*"
        )
        self.password_entry.pack(fill="x", pady=(6, 10))

        self.show_password_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            style="Card.TCheckbutton"
        ).pack(anchor="w", pady=(0, 18))

        self.login_btn = ttk.Button(
            card,
            text="Login",
            style="Accent.TButton",
            command=self.login
        )

        self.login_btn.pack(fill="x")

        ttk.Label(
            card,
            text="Use your assigned credentials to access invoices, inventory, and reports.",
            style="CardMuted.TLabel",
            wraplength=300,
            justify="left"
        ).pack(anchor="w", pady=(16, 0))

        self.username_entry.focus_set()

        self.root.bind("<Return>", lambda event: self.login())

    def toggle_password_visibility(self, event=None):

        self.password_entry.configure(
            show="" if self.show_password_var.get() else "*"
        )

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "":
            messagebox.showwarning(
                "Validation",
                "Please enter username."
            )
            return

        if password == "":
            messagebox.showwarning(
                "Validation",
                "Please enter password."
            )
            return

        success, result = self.login_manager.login(
            username,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                f"Welcome {result['Username']}!"
            )

            self.root.destroy()

            from ui.dashboard_window import DashboardWindow

            dashboard_root = tk.Tk()
            apply_theme(dashboard_root)

            DashboardWindow(
                dashboard_root,
                result
            )

            dashboard_root.mainloop()

        else:

            messagebox.showerror(
                "Login Failed",
                result
            )


if __name__ == "__main__":

    root = tk.Tk()

    LoginWindow(root)

    root.mainloop()
