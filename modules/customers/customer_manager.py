"""
customer_manager.py

Customer management module for
Ramdev Billing Software.
"""

from database.excel_manager import ExcelManager
from database.validator import Validator
from database.schema import CUSTOMERS_SHEET
from utils.helpers import Helpers


class CustomerManager:

    def __init__(self):
        self.db = ExcelManager()

    def get_all_customers(self):
        """
        Return all customers.
        """
        return self.db.get_all_records(CUSTOMERS_SHEET)

    def get_customer(self, customer_id):
        """
        Return customer by ID.
        """
        return self.db.find_record(
            CUSTOMERS_SHEET,
            "Customer ID",
            customer_id
        )

    def customer_exists(self, customer_id):
        """
        Check customer exists.
        """
        return self.db.record_exists(
            CUSTOMERS_SHEET,
            "Customer ID",
            customer_id
        )

    def phone_exists(self, phone):
        """
        Check duplicate phone number.
        """
        customers = self.get_all_customers()

        for customer in customers:
            if customer["Phone Number"] == phone:
                return True

        return False

    def add_customer(
        self,
        customer_name,
        phone_number,
        address="",
        gstin="",
        email=""
    ):
        """
        Add new customer.
        """

        customer = {
            "Customer ID": self.db.generate_next_id(
                CUSTOMERS_SHEET,
                "CUS",
                "Customer ID"
            ),
            "Customer Name": customer_name,
            "Phone Number": phone_number,
            "Address": address,
            "GSTIN": gstin,
            "Email": email,
            "Created Date": Helpers.current_date()
        }

        errors = Validator.validate_customer(customer)

        if errors:
            return False, errors

        if self.phone_exists(phone_number):
            return False, ["Phone Number already exists."]

        self.db.insert_record(
            CUSTOMERS_SHEET,
            customer
        )

        return True, customer

    def update_customer(
        self,
        customer_id,
        data
    ):
        """
        Update customer.
        """

        customer = self.get_customer(customer_id)

        if not customer:
            return False, ["Customer not found."]

        customer.update(data)

        errors = Validator.validate_customer(customer)

        if errors:
            return False, errors

        self.db.update_record(
            CUSTOMERS_SHEET,
            "Customer ID",
            customer_id,
            data
        )

        return True, customer

    def delete_customer(self, customer_id):
        """
        Delete customer.
        """

        if not self.customer_exists(customer_id):
            return False

        return self.db.delete_record(
            CUSTOMERS_SHEET,
            "Customer ID",
            customer_id
        )

    def search_customers(self, keyword):
        """
        Search customers by ID, Name,
        Phone or GSTIN.
        """

        keyword = keyword.lower().strip()

        results = []

        customers = self.get_all_customers()

        for customer in customers:

            if (
                keyword in str(customer["Customer ID"]).lower()
                or keyword in str(customer["Customer Name"]).lower()
                or keyword in str(customer["Phone Number"]).lower()
                or keyword in str(customer["GSTIN"]).lower()
            ):
                results.append(customer)

        return results

    def total_customers(self):
        """
        Return total customer count.
        """
        return len(self.get_all_customers())
