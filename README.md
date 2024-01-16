# EPF Tools

[![version number](https://img.shields.io/github/v/release/gauravmeena0708/epf_tools2.svg)](https://github.com/gauravmeena0708/epf_tools2/releases) [![Actions Status](https://github.com/gauravmeena0708/epf_tools2/workflows/Test/badge.svg)](https://github.com/gauravmeena0708/epf_tools2/actions) [![License](https://img.shields.io/github/license/gauravmeena0708/epf_tools2)](https://github.com/gauravmeena0708/epf_tools2/blob/main/LICENSE)

This is an alpha repo for EPF analysis tools


## install

```bash
pip install -e git+https://github.com/gauravmeena0708/epftools#egg=epftools
```

### Example Use: Generating bins and categories and flat pivot

```python

import pandas as pd
from epftools import  ClaimProcessor, PDFGenerator, PDFGenerator2

df = pd.read_csv('data/claims.csv')
processor = ClaimProcessor(15, 20)
df  = processor.add_bins_and_categories(df)
print(df.head())
```

```python
df1 = processor.get_flat_pivot(df,"GROUP","days_Group")
df2 = processor.get_flat_pivot(df,"GROUP","STATUS")
df3 = processor.get_flat_pivot(df,"GROUP","CATEGORY")
df4 = processor.get_flat_pivot(df,"GROUP","CLAIM TYPE")
df5 = processor.get_flat_pivot(df,"TASK","CATEGORY")
df6 = processor.get_flat_pivot(df,"TASK","STATUS")
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

[Table Style](https://pandas.pydata.org/docs/user_guide/style.html)
[Chart Style](https://pandas.pydata.org/docs/user_guide/visualization.html)

## When you need to add series of images in PDF
```python

from PIL import Image
import os, re, glob, base64
from epftools import  ClaimProcessor, PDFGenerator, PDFGenerator2

def get_image_file_as_base64_data(file):
    with open(file, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()

directory_path = "./"
pattern = re.compile(r"figure_\d+.png")
all_files = os.listdir(directory_path)

matching_files = [filename for filename in all_files if pattern.match(filename)]
dataframes=[]
for file in matching_files:
    dataframes.append(f'<img src="data:;base64,{ get_image_file_as_base64_data(file) }">')

# Example usage:
html_template_path = 'data/template.html'
output_pdf_path = 'data/out.pdf'
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


pdf_generator = PDFGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(dataframes, False)
```

## Making a stylized dataframes

```python
import pandas as pd
from epftools import  ClaimProcessor, PDFGenerator, PDFGenerator2

df = pd.read_csv('data/claims.csv')
processor = ClaimProcessor(15, 20)
df = processor.add_bins_and_categories(df)
df1 = processor.get_flat_pivot(df, "days_Group", "GROUP")
df2 = processor.get_flat_pivot(df, "STATUS", "GROUP")

# Define style function for cell formatting
def highlight_min(s, color='green'):
    is_max = s == s.min()
    attr = 'background-color: {}'.format(color)
    return [attr if v else '' for v in is_max]

def highlight_max(s, color='yellow'):
    is_max = s == s.max()
    attr = 'background-color: {}'.format(color)
    return [attr if v else '' for v in is_max]

def highlight_top3(s, color='darkorange'):
    top3_values = s.nlargest(3).index
    is_top3 = s.index.isin(top3_values)
    attr = 'color: {};font-weight: bold;'.format(color)
    return [attr if v else '' for v in is_top3]

def conditional_color(val,cutoff=100,color = 'red'):
    color = color if val > cutoff else "black"
    return f"color: {color}"

def color_quantile(s, color='red'):
    quantile_4_threshold = s.quantile(0.75)
    is_in_quantile_4 = s >= quantile_4_threshold
    attr = 'background-color: {}'.format(color)
    return [attr if v else '' for v in is_in_quantile_4]
    

"""\
    .map(conditional_color,cutoff=2000, color='red',subset = pd.IndexSlice[u[:-1], ['0-15']])\
    .map(conditional_color,cutoff=400, color='red',subset = pd.IndexSlice[u[:-1], ["16-20"]]) \
    .map(conditional_color,cutoff=10, color='red',subset = pd.IndexSlice[u[:-1], [">20"]])
"""

def get_styled(df):
    u = df.index.get_level_values(0)
    cols = df.columns
    df_styled = df.style.apply(highlight_top3,color='orangered',subset = pd.IndexSlice[u[:-1], cols[:-1]],axis=1) \
    .apply(color_quantile,color='khaki',subset = pd.IndexSlice[u[:-1], cols[:-1]],axis=1) 
    return df_styled

df1_styled = get_styled(df1)
df2 = get_styled(df2)
# Display the styled DataFrame
display(df1_styled)
```


## Coverting Stylyzed dataframes and images in pdf

```python
import os, re, base64
from epftools import  ClaimProcessor, PDFGenerator, PDFGenerator2

def get_image_file_as_base64_data(file):
    with open(file, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()

directory_path = "./"
pattern = re.compile(r"figure_\d+.png")
all_files = os.listdir(directory_path)
matching_files = [filename for filename in all_files if pattern.match(filename)]

elements=[]
elements.append(df1_styled.to_html())
elements.append(df2.to_html())
for file in matching_files:
    elements.append(f'<img src="data:;base64,{ get_image_file_as_base64_data(file) }">')

# Example usage:
html_template_path = 'data/template.html'
output_pdf_path = 'data/out.pdf'
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
pdf_generator = PDFGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(elements,html=False)
```

## Using DataFrameStyler and PDFGenerator2(wkhtmltopdf -windows)

```python
#!pip install -e git+https://github.com/gauravmeena0708/epf_tools2#egg=epftools2
import pandas as pd
from epftools import  ClaimProcessor, PDFGenerator, PDFGenerator2, DataFrameStyler

df = pd.read_csv('data/claims_26_12_23.csv')
processor = ClaimProcessor(10, 20)
df = processor.add_bins_and_categories(df)

def info(df):
    display(df.head())
    print(df['CATEGORY'].unique())
    print(df['CLAIM TYPE'].unique())
    print(df['INT_CATEGORY'].unique())
    print(df['STATUS2'].unique())
    
info(df)


elements = processor.get_elements_daily_summary(df, DataFrameStyler)
# Example usage:
html_template_path = 'data/template.html'
output_pdf_path = 'data/out.pdf'
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
pdf_generator = PDFGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(elements,html=False)


```

## Generate pdf from a folder of images

```python
import os
import re
import base64
from epftools import ClaimProcessor, PDFGenerator, PDFGenerator2
from glob import glob

matching_files = glob(os.path.join("./data/", "figure_*.png"))
print(matching_files)
def get_image_file_as_base64_data(file_path):
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def generate_html_elements(matching_files):
    elements=[]
    image_elements = map(lambda f: f'<img src="data:;base64,{get_image_file_as_base64_data(f)}">', matching_files)
    elements.extend(list(image_elements))

    return elements




html_template_path = 'data/template.html'
output_pdf_path = 'data/out.pdf'
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    
elements = generate_html_elements(matching_files)
    
pdf_generator = PDFGenerator2(html_template_path, output_pdf_path, wkhtmltopdf_path)
pdf_generator.generate_pdf(elements, html=False)
```

## PDF Split

```python
from epftools import  PDFTools as pt
input_path = "in.pdf"
output_path_template = "output_{0}_{1}.pdf"
page_ranges = [(1, 1), (2, 2), (3, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18)]
pt.split_pdf(input_path, output_path_template, page_ranges)
```

## Excel Merge

```python
from epftools import  ExcelMerger
folder_path = './/due2//'
merger = ExcelMerger(folder_path,ext=".xls")
merger.merge_and_save()
```

## Periodicity analysis

```python

!pip install -e git+https://github.com/gauravmeena0708/epftools#egg=epftools
!pip install epftools
!pip install reportlab pdfkit PyPDF2 pytesseract pdf2image

from epftools import PeriodicityProcessor
import pandas as pd

path24 = '<path>'
processor = PeriodicityProcessor(path24, '2023-12')
dall = processor.df
dall.head()
dall2 = pd.DataFrame(columns=['text_column', 'blank', 'reason1', 'reason2', 'reason_category'])
dall2[['blank', 'reason1', 'reason2']] = dall['REJECT_REASON'].str.split(r'\d\)', n=2, expand=True)

dall['reason1'] = dall2['reason1'].str.strip()
dall['reason2'] = dall2['reason2'].str.strip()
death10d = dall[dall['FORM_NAME']=="Death-10D"]
display(len(death10d))
display(death10d.head())
df2 = processor.col_grouped_rejection(dall,"GROUP_ID")

```