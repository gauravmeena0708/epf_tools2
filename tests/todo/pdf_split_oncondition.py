"""
This code is create separate pdf filtering pages based on certain condition on each page's text
"""
from PyPDF4 import PdfFileReader, PdfFileWriter
import numpy as np
import pandas as pd
import os
import re

writer = PdfFileWriter()
path = "./dlc/"

ind_pos = [0,18,19,20,38,39, 42,41,43,45,48]
rows = []
arr =[]

pdffiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.PDF')]

sentence_year_pattern = re.compile(r'Stoppage of pension from .* (\d{4}) -Regarding\.')
    
for fname in pdffiles:
    fullpath = path+fname
    pdf_file = open(fullpath, 'rb')
    pdf_reader = PdfFileReader(pdf_file)
    print(pdf_reader.numPages)
    for num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(num)
        text = page.extractText()
        matches = sentence_year_pattern.findall(text)
        if len(matches):
            if int(matches[0])<2019:
                writer.addPage(page)

        
with open('olddlc.pdf', 'wb') as output_pdf:
    writer.write(output_pdf)
