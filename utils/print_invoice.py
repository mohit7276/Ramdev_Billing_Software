"""
print_invoice.py

Print Utility

Ramdev Billing Software
"""

import os
import platform
import subprocess


class PrintInvoice:

    @staticmethod
    def open_pdf(pdf_file):
        """
        Open PDF using the default application.
        """

        if not os.path.exists(pdf_file):
            raise FileNotFoundError(pdf_file)

        if platform.system() == "Windows":
            os.startfile(pdf_file)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", pdf_file])
        else:
            subprocess.Popen(["xdg-open", pdf_file])

    # ---------------------------------------------------------

    @staticmethod
    def print_pdf(pdf_file):
        """
        Print PDF using default printer.
        """

        if not os.path.exists(pdf_file):
            raise FileNotFoundError(pdf_file)

        if platform.system() == "Windows":
            os.startfile(pdf_file, "print")
        else:
            raise NotImplementedError(
                "Direct printing is currently supported only on Windows."
            )

    # ---------------------------------------------------------

    @staticmethod
    def print_preview(pdf_file):
        """
        Open PDF for print preview.
        """

        PrintInvoice.open_pdf(pdf_file)
