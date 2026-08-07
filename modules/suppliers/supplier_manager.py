"""
supplier_manager.py

Handles supplier management.

Ramdev Billing Software
"""

from database.excel_manager import ExcelManager


class SupplierManager:

    def __init__(self):

        self.db = ExcelManager()

    # =====================================================
    # ADD SUPPLIER
    # =====================================================

    def add_supplier(
        self,
        supplier_name,
        phone,
        address="",
        gstin="",
        email=""
    ):
        """
        Add a new supplier.
        """

        supplier_name = str(
            supplier_name
        ).strip()

        phone = str(
            phone
        ).strip()

        if not supplier_name:

            return False, "Supplier name is required."

        # -------------------------------------------------
        # Check duplicate supplier
        # -------------------------------------------------

        suppliers = self.get_all_suppliers()

        for supplier in suppliers:

            if (
                str(
                    supplier.get(
                        "Supplier Name",
                        ""
                    )
                ).strip().lower()
                == supplier_name.lower()
            ):

                return False, "Supplier already exists."

        # -------------------------------------------------
        # Generate ID
        # -------------------------------------------------

        supplier_id = self.db.generate_next_id(
            "Suppliers",
            "SUP",
            "Supplier ID"
        )

        supplier = {

            "Supplier ID":
                supplier_id,

            "Supplier Name":
                supplier_name,

            "Phone Number":
                phone,

            "Address":
                address,

            "GSTIN":
                gstin,

            "Email":
                email,

            "Created Date":
                __import__(
                    "datetime"
                ).datetime.now().strftime(
                    "%Y-%m-%d"
                )
        }

        self.db.insert_record(
            "Suppliers",
            supplier
        )

        return True, supplier_id

    # =====================================================
    # GET ALL
    # =====================================================

    def get_all_suppliers(self):

        return self.db.get_all_records(
            "Suppliers"
        )

    # =====================================================
    # GET ONE
    # =====================================================

    def get_supplier(
        self,
        supplier_id
    ):

        return self.db.find_record(
            "Suppliers",
            "Supplier ID",
            supplier_id
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_suppliers(
        self,
        keyword
    ):

        keyword = str(
            keyword
        ).lower()

        suppliers = (
            self.get_all_suppliers()
        )

        results = []

        for supplier in suppliers:

            searchable = " ".join([
                str(
                    supplier.get(
                        "Supplier ID",
                        ""
                    )
                ),
                str(
                    supplier.get(
                        "Supplier Name",
                        ""
                    )
                ),
                str(
                    supplier.get(
                        "Phone Number",
                        ""
                    )
                ),
                str(
                    supplier.get(
                        "GSTIN",
                        ""
                    )
                ),
                str(
                    supplier.get(
                        "Email",
                        ""
                    )
                )
            ]).lower()

            if keyword in searchable:

                results.append(
                    supplier
                )

        return results

    # =====================================================
    # UPDATE
    # =====================================================

    def update_supplier(
        self,
        supplier_id,
        data
    ):

        return self.db.update_record(
            "Suppliers",
            "Supplier ID",
            supplier_id,
            data
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_supplier(
        self,
        supplier_id
    ):

        return self.db.delete_record(
            "Suppliers",
            "Supplier ID",
            supplier_id
        )
