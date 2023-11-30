# EPF Tools

[![version number](https://img.shields.io/github/v/release/gauravmeena0708/epf_tools2.svg)](https://github.com/gauravmeena0708/epf_tools2/releases) [![Actions Status](https://github.com/gauravmeena0708/epf_tools2/workflows/Test/badge.svg)](https://github.com/gauravmeena0708/epf_tools2/actions) [![License](https://img.shields.io/github/license/gauravmeena0708/epf_tools2)](https://github.com/gauravmeena0708/epf_tools2/blob/main/LICENSE)

This is an alpha repo for EPF analysis tools


## install

```bash
pip install -e git+https://github.com/gauravmeena0708/epf_tools2#egg=epftools2
```

### Example Use

```python

import pandas as pd
from epftools import  ClaimProcessor, PDFGenerator

df = pd.read_csv('data/claims.csv')
category_generator = ClaimProcessor(15, 20)
df  = category_generator.add_bins_and_categories(df)
#category_generator.get_flat_pivot(df,"GROUP ID","INT_CATEGORY")
df.head()
#==============================================================


dataframes =[]
dataframes.append(category_generator.get_flat_pivot(df,"GROUP ID","days_Group"))
dataframes.append(category_generator.get_flat_pivot(df,"GROUP ID","STATUS"))
dataframes.append(category_generator.get_flat_pivot(df,"GROUP ID","CATEGORY"))
dataframes.append(category_generator.get_flat_pivot(df,"GROUP ID","CLAIM TYPE"))
dataframes.append(category_generator.get_flat_pivot(df,"TASK ID","CATEGORY"))
dataframes.append(category_generator.get_flat_pivot(df,"TASK ID","STATUS"))


pdf_generator = PDFGenerator(pdf_file="data/report.pdf")
pdf_generator.create_pdf(dataframes)

```
