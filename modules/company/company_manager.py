"""
company_manager.py

Manage company information.

Ramdev Billing Software
"""

from database.excel_manager import ExcelManager
from database.schema import (
    COMPANY_SHEET,
    COMPANY_HEADERS,
    DEFAULT_COMPANY
)


class CompanyManager:

    def __init__(self):

        self.db = ExcelManager()

        self.initialize_company()

    # -----------------------------------------------------

    def initialize_company(self):
        """
        Create default company if no data exists.
        """

        companies = self.db.get_all_records(COMPANY_SHEET)

        if companies:
            return

        company = {}

        for key, value in zip(
            COMPANY_HEADERS,
            DEFAULT_COMPANY
        ):
            company[key] = value

        self.db.insert_record(
            COMPANY_SHEET,
            company
        )

    # -----------------------------------------------------

    def get_company(self):
        """
        Return company information.
        """

        companies = self.db.get_all_records(
            COMPANY_SHEET
        )

        if companies:
            return companies[0]

        return None

    # -----------------------------------------------------

    def update_company(self, company_data):
        """
        Update company information.
        """

        companies = self.db.get_all_records(
            COMPANY_SHEET
        )

        if companies:

            self.db.update_record(

                COMPANY_SHEET,

                "Company Name",

                companies[0]["Company Name"],

                company_data

            )

            return True

        self.db.insert_record(
            COMPANY_SHEET,
            company_data
        )

        return True
