import pandas as pd

dict_month = {
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
}


def change_col(x):
    year=x[-4:]
    month = dict_month[x[:3]]
    return str(year)+'-'+str(month)

def parse_estmst(filename):
    df = pd.read_csv(filename,low_memory=False)
    df = df.set_index("EST ID")
    dft = df.transpose()
    dft =dft.reset_index()
    dft["index"] = dft['index'].str[13:21]
    dft.drop(dft.tail(1).index,inplace=True)

    dft['index'] = dft['index'].apply(change_col)
    df_multiindex = dft.set_index(['index', 'EST ID'])
    return dft
    


df16 = parse_estmst("2016.csv")
df17 = parse_estmst("2017.csv")
df18 = parse_estmst("2018.csv")
df19 = parse_estmst("2019.csv")
df20 = parse_estmst("2020.csv")
df21 = parse_estmst("2021.csv")
df22 = parse_estmst("12months.csv")

df_common = pd.concat([df16, df17,df18, df19, df20, df21, df22])#, ignore_index = True)
df_common.rename(columns = {'index':'date','EST ID':'type'}, inplace = True)
df_common=df_common.set_index(['date','type'])
df_common=df_common.stack()
df1 = df_common.unstack(level=1)
df1 =df1.reset_index()
cols = ['AMOUNT','ECR','MEMBER']
for col in cols:
    df1[col] =df1[col].astype(int)
df1['date'] = pd.to_datetime(df1['date'])
df1 = df1.sort_values(by=['EST ID','date'])

"""
import plotly.express as px

fig = px.line(df1[:85*20], x="date", y="MEMBER", color='EST ID')
fig.show()
"""
print(df1.dtypes)
df2 = df1[['date','EST ID','MEMBER']]
df3 = df2.reset_index(drop=True)
df3.index.rename('index',inplace=True)
df3=df3[['EST ID','date','MEMBER']]

"""
import plotly.graph_objects as go

import pandas as pd
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
cols = ['PYKRP0000024000','PYKRP0000032000','PYKRP0000063000']
for col in cols:
    dfm[col] =dfm[col].astype(int)

fig = go.Figure([go.Scatter(x=dfm['date'], y=dfm[cols])])
fig.show()

"""