"""
helpers.py

Common helper functions.

Ramdev Billing Software
"""

from datetime import datetime

from database.excel_manager import ExcelManager
from database.schema import (
    INVOICES_SHEET,
    SETTINGS_SHEET
)


class Helpers:
    """
    Common helper functions for
    Ramdev Billing Software.
    """

    # =====================================================
    # CURRENT DATE
    # =====================================================

    @staticmethod
    def current_date():

        return datetime.now().strftime(
            "%Y-%m-%d"
        )

    # =====================================================
    # CURRENT TIME
    # =====================================================

    @staticmethod
    def current_time():

        return datetime.now().strftime(
            "%H:%M:%S"
        )

    # =====================================================
    # TIMESTAMP
    # =====================================================

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

    # =====================================================
    # NEXT INVOICE NUMBER
    # =====================================================

    @staticmethod
    def next_invoice_number():

        db = ExcelManager()

        # Get prefix from Settings
        prefix = "INV"

        settings = db.get_all_records(
            SETTINGS_SHEET
        )

        for setting in settings:

            if setting.get("Key") == "Invoice Prefix":

                prefix = str(
                    setting.get(
                        "Value",
                        "INV"
                    )
                )

                break

        # Generate next number
        return db.generate_next_id(
            INVOICES_SHEET,
            prefix,
            "Invoice Number"
        )