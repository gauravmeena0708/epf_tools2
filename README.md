# EPF Tools

[![version number](https://img.shields.io/github/v/release/gauravmeena0708/epf_tools2.svg)](https://github.com/gauravmeena0708/epf_tools2/releases) [![Actions Status](https://github.com/gauravmeena0708/epf_tools2/workflows/Test/badge.svg)](https://github.com/gauravmeena0708/epf_tools2/actions) [![License](https://img.shields.io/github/license/gauravmeena0708/epf_tools2)](https://github.com/gauravmeena0708/epf_tools2/blob/main/LICENSE)

This is an alpha repo for EPF analysis tools


## install

```bash
pip install -e git+https://github.com/gauravmeena0708/epf_tools2#egg=epftools2
```

### Example Use: Generating bins and categories and flat pivot

```python

import pandas as pd
from epftools import  ClaimProcessor, PDFGenerator, , PDFGenerator2

df = pd.read_csv('data/claims.csv')
processor = ClaimProcessor(15, 20)
df  = processor.add_bins_and_categories(df)
print(df.head())
```

```python
df1 = processor.get_flat_pivot(df,"GROUP ID","days_Group")
df2 = processor.get_flat_pivot(df,"GROUP ID","STATUS")
df3 = processor.get_flat_pivot(df,"GROUP ID","CATEGORY")
df4 = processor.get_flat_pivot(df,"GROUP ID","CLAIM TYPE")
df5 = processor.get_flat_pivot(df,"TASK ID","CATEGORY")
df6 = processor.get_flat_pivot(df,"TASK ID","STATUS")
dataframes =[df1,df2,df3,df4,df5,df6]
```

## PdfGenerator

```python

pdf_generator = PDFGenerator(pdf_file="data/report.pdf")
pdf_generator.create_pdf(dataframes)

```
## PdfGenerator2: if wkhtmmltopdf is installed
```python

# Example usage:
html_template_path = 'data/template.html'
output_pdf_path = 'data/out.pdf'
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


pdf_generator = PDFGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(dataframes)
```
