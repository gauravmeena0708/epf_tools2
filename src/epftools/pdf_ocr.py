from os import listdir, mkdir, startfile
from os.path import isfile, join, exists
from PyPDF2 import PdfWriter
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import io

class PDFOCR:
    @staticmethod
    def convert_images_to_pdf(input_path, output_path, poppler_path):
        pdffiles = [f for f in listdir(input_path) if isfile(join(input_path, f)) and '.pdf' in f]
        print('\nList of PDF Files:\n')
        i = 0
        for file in pdffiles:
            print(file)
            i = i + 1
            images = convert_from_path(join(input_path, file), poppler_path=poppler_path)
            pdf_writer = PdfWriter()
            for image in images:
                page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
                pdf = PyPDF2.PdfReader(io.BytesIO(page))
                pdf_writer.add_page(pdf.pages[0])
            # export the searchable PDF to the output path
            output_file_path = join(output_path, file)
            with open(output_file_path, "wb") as f:
                pdf_writer.write(f)
            print(f"Converted and saved: {output_file_path}")

"""
poppler_path = r"<poppler path>"
pytesseract.pytesseract.tesseract_cmd = r"<tessaract path>"
input_path = "<input dir>"
output_path = "<output dir>"
PDFOCR.convert_images_to_pdf(input_path, output_path, poppler_path)
"""