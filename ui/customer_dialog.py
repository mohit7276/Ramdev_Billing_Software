"""
customer_dialog.py

Add/Edit Customer Dialog

Ramdev Billing Software
"""

import tkinter as tk
from tkinter import ttk, messagebox

from modules.customers.customer_manager import CustomerManager


class CustomerDialog(tk.Toplevel):

    def __init__(self, parent, customer=None):

        super().__init__(parent)

        self.manager = CustomerManager()
        self.customer = customer
        self.saved = False

        self.title(
            "Edit Customer"
            if customer else
            "Add Customer"
        )

        self.geometry("500x500")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

        if customer:
            self.load_customer()

    # -------------------------------------------------

    def create_widgets(self):

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        # Customer Name

        ttk.Label(
            frame,
            text="Customer Name"
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.name = ttk.Entry(frame, width=40)

        self.name.grid(row=0, column=1, sticky="ew")

        # Phone

        ttk.Label(
            frame,
            text="Phone Number"
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.phone = ttk.Entry(frame, width=40)

        self.phone.grid(row=1, column=1, sticky="ew")

        # Address

        ttk.Label(
            frame,
            text="Address"
        ).grid(row=2, column=0, sticky="nw", pady=8)

        self.address = tk.Text(
            frame,
            width=40,
            height=4
        )

        self.address.grid(row=2, column=1, sticky="ew")

        # GSTIN

        ttk.Label(
            frame,
            text="GSTIN"
        ).grid(row=3, column=0, sticky="w", pady=8)

        self.gstin = ttk.Entry(frame, width=40)

        self.gstin.grid(row=3, column=1, sticky="ew")

        # Email

        ttk.Label(
            frame,
            text="Email"
        ).grid(row=4, column=0, sticky="w", pady=8)

        self.email = ttk.Entry(frame, width=40)

        self.email.grid(row=4, column=1, sticky="ew")

        # Buttons

        button_frame = ttk.Frame(frame)

        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20
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

    # -------------------------------------------------

    def load_customer(self):

        self.name.insert(
            0,
            self.customer["Customer Name"]
        )

        self.phone.insert(
            0,
            self.customer["Phone Number"]
        )

        self.address.insert(
            "1.0",
            self.customer["Address"]
        )

        self.gstin.insert(
            0,
            self.customer["GSTIN"]
        )

        self.email.insert(
            0,
            self.customer["Email"]
        )

    # -------------------------------------------------

    def save(self):

        name = self.name.get().strip()

        phone = self.phone.get().strip()

        address = self.address.get(
            "1.0",
            "end"
        ).strip()

        gstin = self.gstin.get().strip()

        email = self.email.get().strip()

        if self.customer:

            success, result = self.manager.update_customer(

                self.customer["Customer ID"],

                {

                    "Customer Name": name,

                    "Phone Number": phone,

                    "Address": address,

                    "GSTIN": gstin,

                    "Email": email

                }

            )

        else:

            success, result = self.manager.add_customer(

                customer_name=name,

                phone_number=phone,

                address=address,

                gstin=gstin,

                email=email

            )

        if success:

            self.saved = True

            messagebox.showinfo(
                "Success",
                "Customer saved successfully."
            )

            self.destroy()

        else:

            messagebox.showerror(
                "Validation Error",
                "\n".join(result)
            )
