import pdfkit
from pathlib import Path
from bs4 import BeautifulSoup


"""
Example usecase:
# Example usage:
html_template_path = 'data/template.html'
output_pdf_path    = 'data/out.pdf'
wkhtmltopdf_path   = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


pdf_generator = PdfGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(df1)
"""
class PDFGenerator2:
    def __init__(self, html_template_path, output_path, wkhtmltopdf_path):
        self.template = Path(html_template_path).read_text()
        self.output_path = output_path
        self.wkhtmltopdf_path = wkhtmltopdf_path
        self.classes = 'table table-sm table-bordered border-primary d-print-table fs-6'
        self.options = {
            'page-size': 'A4',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.2in',
            'margin-left': '0.2in'
        }

    def modify_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        for table in soup.find_all('table'):
            table["class"] = self.classes
        for td in soup.find_all('td'):
            td["style"] = "font-size:10px;padding:2px;text-align:center;" 
        for th in soup.find_all('th'):
            th["style"] = "font-size:10px;padding:2px;text-align:center;"
        return str(soup)

    def generate_pdf(self, dataframes,html=True):
        table_html = ""
        for i, df in enumerate(dataframes):
            if html:
                table_html = table_html+ "<br/><h5>Table "+str(i+1)+"</h5>" + df.to_html(classes=self.classes) + ""
            else:
                table_html = table_html+ "<br/><h5>Table "+str(i+1)+"</h5>" + df + ""
        html_content = self.template % (table_html)
        modified_html = self.modify_html(html_content)

        config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
        pdfkit.from_string(modified_html, self.output_path, options=self.options, configuration=config)