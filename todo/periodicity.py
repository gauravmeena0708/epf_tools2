import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px

def read_periodicity(fname, year):
    df = pd.read_csv(fname, encoding = 'unicode_escape')
    df['RECEIPT_DATE'] = pd.to_datetime(df['RECEIPT_DATE'])
    df.dropna(subset=['SETTLED_REJECT_DATE'], how='all', inplace=True)
    df['SETTLED_REJECT_DATE'] = pd.to_datetime(df['SETTLED_REJECT_DATE'])
    df['FORM_NAME']    = [str(x)[:8].strip() for x in df['FORM_NAME']] 
    df['EST']          = [str(x)[:15] for x in df['MEMBER_ID']]
    df['month']        = df['SETTLED_REJECT_DATE'].dt.month
    df['week']         = df['SETTLED_REJECT_DATE'].dt.isocalendar().week
    df['weekday']      = df['SETTLED_REJECT_DATE'].dt.day_name()
    df['mday']         = df['SETTLED_REJECT_DATE'].dt.day
    df['yday']         = df['SETTLED_REJECT_DATE'].dt.dayofyear
    df['TASK_ID']      = df['TASK_ID'].astype("category")
    df['GROUP_ID']     = df['GROUP_ID'].astype("category")
    df['FORM_NAME']    = df['FORM_NAME'].astype("category")
    df['PARA_DETAILS'] = df['PARA_DETAILS'].astype("category")
    df['fy']           = year
    df.loc[df['DAYS_TAKEN_FOR_REJECTION'].isnull(), 'outcome'] = 'settled'
    df.loc[df['DAYS_TAKEN_FOR_SETTLEMENT'].isnull(), 'outcome'] = 'rejected'
    dfs = df.loc[df['DAYS_TAKEN_FOR_REJECTION'].isnull()]
    dfs['TOTAL_AMOUNT'] = dfs['TOTAL_AMOUNT'].str.replace(',', '').astype(float)
    #dfs.loc[dfs['TOTAL_AMOUNT'].between(0, 499999, 'both'), 'cat'] = '<5lakh'
    #dfs.loc[dfs['TOTAL_AMOUNT'].between(500000, 2499999, 'both'), 'cat'] = '5lakh-25lakh'
    #dfs.loc[dfs['TOTAL_AMOUNT'].ge(2500000), 'cat'] = '>=25lakh'
    
    #dfr = df.loc[df['DAYS_TAKEN_FOR_SETTLEMENT'].isnull()]
    

    return df

dall = read_periodicity(".//periodicity//claims_2022-23.csv",2023)


dall.info()

"""
df3 = dset.groupby(['FORM_NAME'],as_index=False).agg({'TOTAL_AMOUNT':np.sum})
df3

import plotly.graph_objects as go

fig = go.Figure(go.Bar(
            x=df3['TOTAL_AMOUNT'],
            y=df3['FORM_NAME'],
            orientation='h'))

fig.show()
"""