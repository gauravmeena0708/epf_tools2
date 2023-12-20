from PyPDF2 import PdfReader, PdfWriter

class PDFTools:
     @staticmethod
     def split_pdf(input_path, output_path_template, page_ranges):
        reader = PdfReader(open(input_path, "rb"))
        

        for start_page, end_page in page_ranges:
            writer = PdfWriter()
            for page_number in range(start_page, end_page + 1):
                writer.add_page(reader.pages[page_number - 1])

            output_path = output_path_template.format(start_page, end_page)
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
                print(f"Created PDF: {output_path}")

        reader.stream.close()