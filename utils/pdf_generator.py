"""
pdf_generator.py

Generate PDF Invoice

Ramdev Billing Software
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # -----------------------------------------------------

    def generate(
        self,
        company,
        customer,
        invoice,
        items,
        output_file
    ):

        os.makedirs(
            os.path.dirname(output_file),
            exist_ok=True
        )

        pdf = SimpleDocTemplate(
            output_file,
            pagesize=A4
        )

        elements = []

        # -------------------------------------------------
        # Company
        # -------------------------------------------------

        elements.append(
            Paragraph(
                f"<b><font size=18>{company['Company Name']}</font></b>",
                self.styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                company["Address"],
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Phone : {company['Phone']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"GSTIN : {company['GSTIN']}",
                self.styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # -------------------------------------------------
        # Invoice
        # -------------------------------------------------

        elements.append(
            Paragraph(
                f"<b>Invoice No :</b> {invoice['Invoice Number']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Date :</b> {invoice['Invoice Date']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Customer :</b> {customer['Customer Name']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Phone :</b> {customer['Phone Number']}",
                self.styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        # -------------------------------------------------
        # Product Table
        # -------------------------------------------------

        table_data = [[

            "Product",

            "Color",

            "Qty",

            "Rate",

            "GST",

            "Amount"

        ]]

        for item in items:

            amount = item["Quantity"] * item["Rate"]

            gst = amount * item["GST %"] / 100

            total = amount + gst

            table_data.append([

                item["Product Name"],

                item["Color"],

                item["Quantity"],

                f"{item['Rate']:.2f}",

                f"{item['GST %']}%",

                f"{total:.2f}"

            ])

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.grey),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

                ("ALIGN", (0,0), (-1,-1), "CENTER"),

                ("BOTTOMPADDING", (0,0), (-1,0), 10)

            ])

        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        # -------------------------------------------------
        # Totals
        # -------------------------------------------------

        elements.append(
            Paragraph(
                f"<b>Subtotal :</b> ₹ {invoice['Subtotal']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>GST :</b> ₹ {invoice['GST']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Discount :</b> ₹ {invoice['Discount']}",
                self.styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Grand Total :</b> ₹ {invoice['Grand Total']}",
                self.styles["Heading2"]
            )
        )

        elements.append(Spacer(1, 20))

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        elements.append(
            Paragraph(
                "<b>Thank You For Your Business!</b>",
                self.styles["Heading3"]
            )
        )

        elements.append(
            Paragraph(
                company["Terms & Conditions"],
                self.styles["Normal"]
            )
        )

        pdf.build(elements)

        return output_file
