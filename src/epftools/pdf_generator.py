import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape


"""
Example usecase:
dataframes =[]
dataframes.append(df)
from pdf_generator import PDFGenerator
pdf_generator = PDFGenerator(pdf_file="my_report.pdf")
pdf_generator.create_pdf(dataframes)
"""
class PDFGenerator:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def dataframe_to_list(self, df):
        data = [df.columns.tolist()] + df.values.tolist()
        return data

    def get_intensity_color(self, value, max_value):
        intensity = 1 - value / max_value if value > 10 else 1
        return colors.Color(1, intensity, intensity)

    def convert_df2table(self, df):
        data = self.dataframe_to_list(df)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BACKGROUND', (1, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Create a table with the DataFrame
        table = Table(data)
        table.setStyle(table_style)

        """max_value = 88
        for row in range(1, len(data)):
            value = data[row][1]  # Assuming 'Age' is in the second column (index 1)
            cell_color = self.get_intensity_color(value, max_value)
            cell_style = [('BACKGROUND', (1, row), (1, row), cell_color)]
            table.setStyle(TableStyle(cell_style))"""

        return table

    def create_pdf(self, dataframes,with_break=False):
        doc = SimpleDocTemplate(self.pdf_file, pagesize=landscape(letter))
        elements = []
        empty_line = Paragraph("")
        for i, df in enumerate(dataframes):
            table = self.convert_df2table(df)
            elements.append(table)
            elements.append(empty_line)
            if i < len(dataframes) - 1 and with_break:
                elements.append(PageBreak())

        doc.build(elements)
        print(f'PDF saved to {self.pdf_file}')
