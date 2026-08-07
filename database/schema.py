"""
schema.py

Central definition of all Excel sheet names, headers,
default company information, and software settings.

Ramdev Billing Software
"""

# ============================
# Workbook Name
# ============================

DATABASE_NAME = "Database.xlsx"

# ============================
# Sheet Names
# ============================

COMPANY_SHEET = "Company"
USERS_SHEET = "Users"
CUSTOMERS_SHEET = "Customers"
PRODUCTS_SHEET = "Products"
INVOICES_SHEET = "Invoices"
INVOICE_ITEMS_SHEET = "InvoiceItems"
SETTINGS_SHEET = "Settings"
AUDIT_LOG_SHEET = "AuditLog"
BACKUP_HISTORY_SHEET = "BackupHistory"
PURCHASES_SHEET = "Purchases"
SUPPLIERS_SHEET = "Suppliers"


# ============================
# Company Sheet
# ============================

COMPANY_HEADERS = [
    "Company Name",
    "Business Type",
    "Address",
    "Phone",
    "Email",
    "GSTIN",
    "Website",
    "Logo",
    "Bank Name",
    "Account Number",
    "IFSC Code",
    "UPI ID",
    "Terms & Conditions"
]

# ============================
# Default Company Data (Demo)
# ============================

DEFAULT_COMPANY = [
    "Ramdev Enterprises",
    "Thread Supplier",
    "102, Shree Krishna Industrial Estate, Ring Road, Surat, Gujarat - 395002",
    "+91 9876543210",
    "sales@ramdeventerprises.com",
    "24ABCDE1234F1Z5",
    "www.ramdeventerprises.com",
    "assets/logo.png",
    "State Bank of India",
    "123456789012",
    "SBIN0001234",
    "ramdev@upi",
    "Goods once sold will not be taken back."
]

# ============================
# Users Sheet
# ============================

USERS_HEADERS = [
    "Username",
    "Password",
    "Role",
    "Status",
    "Created Date",
    "Last Login"
]

# Password will be hashed later
DEFAULT_USER = [
    "owner",
    "owner123",
    "Owner",
    "Active",
    "",
    ""
]

# ============================
# Customers Sheet
# ============================

CUSTOMERS_HEADERS = [
    "Customer ID",
    "Customer Name",
    "Phone Number",
    "Address",
    "GSTIN",
    "Email",
    "Created Date"
]

# ============================
# Products Sheet
# ============================

PRODUCTS_HEADERS = [
    "Product ID",
    "Thread Type",
    "Product Name",
    "Color",
    "Shade Number",
    "Size",
    "Unit",
    "Rate",
    "GST %",
    "Stock"
]

PURCHASES_HEADERS = [
    "Purchase ID",
    "Purchase Date",
    "Supplier Name",
    "Supplier Phone",
    "Product ID",
    "Product Name",
    "Quantity",
    "Purchase Rate",
    "Amount",
    "Remarks"
]

# ============================
# Invoice Sheet
# ============================

INVOICES_HEADERS = [
    "Invoice Number",
    "Invoice Date",
    "Invoice Time",
    "Customer ID",
    "Customer Name",
    "Phone Number",
    "Subtotal",
    "Discount",
    "GST",
    "Grand Total",
    "Payment Mode",
    "Payment Status",
    "PDF Path",
    "Excel Path"
]

# ============================
# Invoice Items Sheet
# ============================

INVOICE_ITEMS_HEADERS = [
    "Invoice Number",
    "Product ID",
    "Thread Type",
    "Product Name",
    "Color",
    "Shade Number",
    "Size",
    "Unit",
    "Quantity",
    "Rate",
    "GST %",
    "Amount"
]

# ============================
# Settings Sheet
# ============================

SETTINGS_HEADERS = [
    "Key",
    "Value"
]

DEFAULT_SETTINGS = [
    ["Theme", "Dark"],
    ["Invoice Prefix", "INV"],
    ["Next Invoice Number", "1"],
    ["Auto Backup", "Yes"],
    ["Auto Save", "Yes"],
    ["Currency", "₹"],
    ["PDF Folder", "Invoices"],
    ["Report Folder", "Reports"]
]

# ============================
# Audit Log
# ============================

AUDIT_HEADERS = [
    "Date",
    "Time",
    "Username",
    "Action",
    "Details"
]

# ============================
# Backup History
# ============================

BACKUP_HEADERS = [
    "Backup Date",
    "Backup Time",
    "Backup File",
    "Created By"
]

SUPPLIERS_HEADERS = [
    "Supplier ID",
    "Supplier Name",
    "Phone Number",
    "Address",
    "GSTIN",
    "Email",
    "Created Date"
]

# ============================
# Sheet Collection
# ============================

WORKBOOK_STRUCTURE = {
    COMPANY_SHEET: COMPANY_HEADERS,
    USERS_SHEET: USERS_HEADERS,
    CUSTOMERS_SHEET: CUSTOMERS_HEADERS,
    PRODUCTS_SHEET: PRODUCTS_HEADERS,
    INVOICES_SHEET: INVOICES_HEADERS,
    INVOICE_ITEMS_SHEET: INVOICE_ITEMS_HEADERS,
    SETTINGS_SHEET: SETTINGS_HEADERS,
    AUDIT_LOG_SHEET: AUDIT_HEADERS,
    BACKUP_HISTORY_SHEET: BACKUP_HEADERS,
    PURCHASES_SHEET: PURCHASES_HEADERS,
    SUPPLIERS_SHEET: SUPPLIERS_HEADERS,
}

