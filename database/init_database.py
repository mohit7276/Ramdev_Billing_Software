"""
init_database.py

Initialize Ramdev Billing Software Excel Database.

Ramdev Billing Software
"""

from database.excel_manager import ExcelManager


def initialize_database():

    print("=" * 50)
    print("Ramdev Billing Software")
    print("Initializing Excel Database...")
    print("=" * 50)

    try:

        db = ExcelManager()

        print("\nDatabase initialized successfully.")

        print("\nAvailable sheets:")

        for sheet_name in db.workbook.sheetnames:
            print(f"  ✓ {sheet_name}")

        print("\nDatabase is ready.")

    except Exception as e:

        print("\nDatabase initialization failed.")

        print(f"Error: {e}")


if __name__ == "__main__":
    initialize_database()
