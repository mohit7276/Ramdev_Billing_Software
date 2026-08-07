from pathlib import Path

# ==========================
# SOFTWARE INFORMATION
# ==========================

SOFTWARE_NAME = "Ramdev Billing Software"
VERSION = "1.0.0"

# ==========================
# COMPANY DEMO DETAILS
# ==========================

COMPANY_NAME = "Ramdev Enterprises"
COMPANY_ADDRESS = (
    "102, Shree Krishna Industrial Estate,\n"
    "Ring Road, Surat, Gujarat - 395002"
)
COMPANY_PHONE = "+91 9876543210"
COMPANY_EMAIL = "sales@ramdeventerprises.com"
COMPANY_GST = "24ABCDE1234F1Z5"

# ==========================
# PROJECT PATHS
# ==========================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"
INVOICE_DIR = BASE_DIR / "invoices"
REPORT_DIR = BASE_DIR / "reports"
BACKUP_DIR = BASE_DIR / "backups"
LOG_DIR = BASE_DIR / "logs"
LAYOUT_DIR = BASE_DIR / "layouts"
TEMP_DIR = BASE_DIR / "temp"

DATABASE_FILE = DATABASE_DIR / "Database.xlsx"

# ==========================
# INVOICE SETTINGS
# ==========================

INVOICE_PREFIX = "INV"
START_INVOICE_NUMBER = 1

# ==========================
# THEME
# ==========================

THEME = "dark"   # dark / light

# ==========================
# SECURITY
# ==========================

MAX_LOGIN_ATTEMPTS = 5
AUTO_LOGOUT_MINUTES = 15

# ==========================
# PDF SETTINGS
# ==========================

PDF_PAGE_SIZE = "A4"

# ==========================
# BACKUP
# ==========================

AUTO_BACKUP = True
