"""
validator.py

Validation functions for Ramdev Billing Software.
"""

import re


class Validator:

    @staticmethod
    def is_required(value):
        """
        Check if value is not empty.
        """
        if value is None:
            return False

        if str(value).strip() == "":
            return False

        return True

    @staticmethod
    def is_phone(phone):
        """
        Validate Indian mobile number.
        """
        phone = str(phone).strip()

        pattern = r"^[6-9]\d{9}$"

        return bool(re.match(pattern, phone))

    @staticmethod
    def is_email(email):
        """
        Validate email address.
        """
        email = str(email).strip()

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        return bool(re.match(pattern, email))

    @staticmethod
    def is_gstin(gstin):
        """
        Validate GSTIN.
        """
        gstin = str(gstin).strip().upper()

        pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{1}Z[A-Z0-9]{1}$"

        return bool(re.match(pattern, gstin))

    @staticmethod
    def is_number(value):
        """
        Check numeric value.
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_positive(value):
        """
        Check positive number.
        """
        try:
            return float(value) >= 0
        except ValueError:
            return False

    @staticmethod
    def is_integer(value):
        """
        Check integer.
        """
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_customer(customer):
        """
        Validate customer data.
        """

        errors = []

        if not Validator.is_required(customer.get("Customer Name")):
            errors.append("Customer Name is required.")

        if not Validator.is_phone(customer.get("Phone Number")):
            errors.append("Invalid Phone Number.")

        email = customer.get("Email", "")

        if email and not Validator.is_email(email):
            errors.append("Invalid Email.")

        return errors

    @staticmethod
    def validate_product(product):
        """
        Validate product data.
        """

        errors = []

        if not Validator.is_required(product.get("Product Name")):
            errors.append("Product Name is required.")

        if not Validator.is_required(product.get("Thread Type")):
            errors.append("Thread Type is required.")

        if not Validator.is_number(product.get("Rate")):
            errors.append("Invalid Rate.")

        if not Validator.is_positive(product.get("Rate")):
            errors.append("Rate cannot be negative.")

        if not Validator.is_integer(product.get("Stock")):
            errors.append("Stock must be an integer.")

        if not Validator.is_positive(product.get("Stock")):
            errors.append("Stock cannot be negative.")

        return errors

    @staticmethod
    def validate_invoice(invoice):
        """
        Validate invoice data.
        """

        errors = []

        if not Validator.is_required(invoice.get("Customer Name")):
            errors.append("Customer Name is required.")

        if not Validator.is_number(invoice.get("Grand Total")):
            errors.append("Invalid Grand Total.")

        if not Validator.is_positive(invoice.get("Grand Total")):
            errors.append("Grand Total cannot be negative.")

        return errors