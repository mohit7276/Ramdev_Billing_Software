"""
settings_window.py

Company Settings Window

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from modules.company.company_manager import CompanyManager


class SettingsWindow(ttk.Frame):

    def __init__(self, parent, title="Settings", show_header=False):

        super().__init__(parent)

        self.manager = CompanyManager()
        self.show_header = show_header

        self.pack(fill="both", expand=True)

        self.create_widgets()

        self.load_company()

    # ----------------------------------------------------

    def create_widgets(self):

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.LabelFrame(
            self,
            text="Company Information",
            padding=15
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        labels = [

            "Company Name",

            "Business Type",

            "Address",

            "Phone",

            "Email",

            "GSTIN",

            "Website",

            "Bank Name",

            "Account Number",

            "IFSC Code",

            "UPI ID"

        ]

        self.entries = {}

        for row, label in enumerate(labels):

            ttk.Label(
                frame,
                text=label
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=6
            )

            entry = ttk.Entry(
                frame,
                width=45
            )

            entry.grid(
                row=row,
                column=1,
                padx=10,
                pady=6
            )

            self.entries[label] = entry

        ttk.Label(
            frame,
            text="Terms & Conditions"
        ).grid(
            row=len(labels),
            column=0,
            sticky="nw",
            pady=6
        )

        self.terms = tk.Text(
            frame,
            width=45,
            height=5
        )

        self.terms.grid(
            row=len(labels),
            column=1,
            padx=10,
            pady=6
        )

        ttk.Button(

            self,

            text="Save Company Information",

            command=self.save_company

        ).pack(
            pady=10
        )

    # ----------------------------------------------------

    def load_company(self):

        company = self.manager.get_company()

        if not company:
            return

        for key, entry in self.entries.items():

            entry.delete(0, tk.END)

            entry.insert(
                0,
                company.get(key, "")
            )

        self.terms.delete(
            "1.0",
            tk.END
        )

        self.terms.insert(

            "1.0",

            company.get(
                "Terms & Conditions",
                ""
            )

        )

    # ----------------------------------------------------

    def save_company(self):

        company = {}

        for key, entry in self.entries.items():

            company[key] = entry.get().strip()

        company["Logo"] = ""

        company["Terms & Conditions"] = self.terms.get(
            "1.0",
            tk.END
        ).strip()

        self.manager.update_company(company)

        messagebox.showinfo(

            "Success",

            "Company information updated successfully."

        )
