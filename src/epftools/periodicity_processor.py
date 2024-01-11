import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

#pd.options.mode.copy_on_write = True

FORM_NAME_MAPPING = {
    'Form-31': '31',
    'Form-31 [ COVID-2 ]': '31',
    'Form-31 [ COVID ]': '31',
    'Form-31 [ 68J / Illness ]': '31',
    'Form-13 (Transfer Out) [ WITHOUT-MONEY  ]': '13',
    'Form-13 (Transfer Out) [ OTHERS ]': '13',
    'Form-10D': '10D',
    'Form-19': '19',
    'Form-10C [ Withdrawal Benefit ] ': '10C',
    'Form-13 (Transfer Out) [ WITH-MONEY ]': '13',
    'Form-10D [ Death Case ]': 'Death-10D',
    'Form-10C [ Scheme Certificate ]': '10C',
    'Form-5IF': 'Death-5IF',
    'Form-20': 'Death-20',
    'Form-13 (Transfer In / Same Office)': '13',
    'Form-14 (Funding of LIP)': '14'
}

PARA_DETAILS_MAPPING = {
    'Marriage ': 'Advance - Marriage',
    'DECLARED AS AFFECTED BY OUTBREAK OF EPIDEMIC OR PANDEMIC  BY APPROPRIATE GOVERNMENT (COVID-19)': 'Advance - Covid',
    'Illness': 'Advance - Illness',
    'Transfer (Unexempted to Unexempted in other region or to Exempted Establishments)': 'Transfer',
    'Transfer (Unexempted to Unexempted in the same region (office)': 'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)\r\n':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office) ':'Transfer',
    'Monthly Pension - Member': 'Pension - 10D',
    'Resign': 'Final - 19',
    'Settelment to Survivor on death of member':'Death-20',
    'Non Receipt of Wages (>2 months)':'Advance - NRW2M',
    'ADVANCE FOR CONTINUOUS UNEMPLOYMENT FOR ABOVE ONE MONTH': 'Advance - Unemployment 1M',
    'Withdrawal Benefit / Scheme Certificate': 'Pension - 10C',
    'Additions / Alterations of House': 'Advance - Alteration',
    'Construction of House': 'Advance - Construction',
    'Purchase of House / Flat / Construction including acquisition if site from agency': 'Advance - Agency',
    'Natural Calamities': 'Advance - NC',
    'Purchase of Site for Construction of Dwelling House': 'Advance - Construction',
    'Non-Receipt of Wages (>2 months)': 'Advance - NRW_2M',
    ' Higher Education': 'Advance - Higher Education',
    'Purchase of Dwelling House/ Flat from a Promoter ': 'Advance - Promoter',
    'Purchase of Handicap equipment': 'Advance - Handicap',
    'Retirement from service after attaining the age of 55 years': 'Final - 19',
    'Termination of service in the case of mass or individual retrenchment': 'Advance - Mass Retrenchment',
    '90% Withdrawal before retirement': 'Advance - Before Retirement 90',
    'Monthly Pension - Survivors': 'Death-Pension',
    'EDLI Assurance Benefit': 'Death-EDLI',
    'Settlement to Survivor on the death of a member': 'Death-PF',
    'Power Cut': 'Advance - PowerCut',
    'nan': 'Not Available',
    'Payment of Accumulations in the case of Beneficiary charged with the offense of Murder of the deceased member ': 'Advance - ChargedWithMurder',
    'Payment of LIP Premium': 'Advance - LIP',
    np.nan: 'Death-20'
}

PARA_DETAILS_MAPPING1 = {
    'Marriage ': 'Advance',
    'DECLARED AS AFFECTED BY OUTBREAK OF EPIDEMIC OR PANDEMIC  BY APPROPRIATE GOVERNMENT (COVID-19)': 'Advance',
    'Illness': 'Advance',
    'Transfer (Unexempted to Unexempted in other region or to Exempted Establishments)': 'Transfer',
    'Transfer (Unexempted to Unexempted in the same region (office)': 'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)\r\n':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office) ':'Transfer',
    'Monthly Pension - Member': 'Final',
    'Resign': 'Final',
    'ADVANCE FOR CONTINUOUS UNEMPLOYMENT FOR ABOVE ONE MONTH': 'Advance',
    'Withdrawal Benefit / Scheme Certificate': '10C',
    'Additions / Alterations of House': 'Advance',
    'Construction of House': 'Advance',
    'Purchase of House / Flat / Construction including acquisition if the site from the agency': 'Advance',
    'Natural Calamities': 'Advance',
    'Purchase of Site for Construction of Dwelling House': 'Advance',
    'Non-Receipt of Wages (>2 months)': 'Advance',
    ' Higher Education': 'Advance',
    'Purchase of Dwelling House/ Flat from a Promoter ': 'Advance',
    'Purchase of Handicap equipment': 'Advance',
    'Retirement from service after attaining the age of 55 years': 'Final',
    'Termination of service in the case of mass or individual retrenchment': 'Advance',
    '90% Withdrawal before retirement': 'Advance',
    'Monthly Pension - Survivors': 'Death',
    'EDLI Assurance Benefit': 'Death',
    'Settlement to Survivor on the death of a member': 'Death',
    'Power Cut': 'Advance',
    'Payment of Accumulations in the case of Beneficiary charged with the offense of Murder of the deceased member ': 'Advance',
    'Payment of LIP Premium': 'Advance',
    np.nan: 'Death'
}

PARA_DETAILS_MAPPING2 = {
    'Marriage ': 'Others',
    'DECLARED AS AFFECTED BY OUTBREAK OF EPIDEMIC OR PANDEMIC  BY APPROPRIATE GOVERNMENT (COVID-19)': 'Advance - Covid',
    'Illness': 'Advance - Illness',
    'Transfer (Unexempted to Unexempted in other region or to Exempted Establishments)': 'Transfer',
    'Transfer (Unexempted to Unexempted in the same region (office)': 'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office)\r\n':'Transfer',
    'Transfer (Unexempted to Unexempted in same region (office) ':'Transfer',
    'Monthly Pension - Member': 'Others',
    'Resign': 'Final - 19',
    'ADVANCE FOR CONTINUOUS UNEMPLOYMENT FOR ABOVE ONE MONTH': 'Others',
    'Withdrawal Benefit / Scheme Certificate': 'Pension - 10C',
    'Additions / Alterations of House': 'Advance - Alteration',
    'Construction of House': 'Advance - Construction',
    'Purchase of House / Flat / Construction including acquisition if the site from the agency': 'Others',
    'Natural Calamities': 'Advance - NC',
    'Purchase of Site for Construction of Dwelling House': 'Advance - Construction',
    'Non-Receipt of Wages (>2 months)': 'Advance - NRW_2M',
    ' Higher Education': 'Others',
    'Purchase of Dwelling House/ Flat from a Promoter ': 'Others',
    'Purchase of Handicap equipment': 'Others',
    'Retirement from service after attaining the age of 55 years': 'Final - 19',
    'Termination of service in the case of mass or individual retrenchment': 'Others',
    '90% Withdrawal before retirement': 'Others',
    'Monthly Pension - Survivors': 'Others',
    'EDLI Assurance Benefit': 'Death',
    'Settlement to Survivor on the death of a member': 'Death',
    'Power Cut': 'Others',
    'nan': 'Death',
    'Payment of Accumulations in the case of Beneficiary charged with the offense of Murder of the deceased member ': 'Others',
    'Payment of LIP Premium': 'Others',
    np.nan: 'Death'
}

OUTCOME_MAPPING = {
    'settled': 0,
    'rejected': 1
}


def process_row(value):
    if value == 'nan' or value == '' or value == ' ':
        return np.nan
    else:
        return float(value.replace(',', ''))

def get_financial_year_quarter(date):
    if date.month >= 4:
        return (date.month - 4) // 3 + 1
    else:
        return (date.month + 8) // 3



class PeriodicityProcessor:
    def __init__(self, path, year):
        self.df = self.read_periodicity(path, year)

    def read_periodicity(self, fname, year):
        df = pd.read_csv(fname, encoding='latin1')  # encoding = 'unicode_escape'
        df['RECEIPT_DATE'] = pd.to_datetime(df['RECEIPT_DATE'])
        df.dropna(subset=['SETTLED_REJECT_DATE'], how='all', inplace=True)
        df['SETTLED_REJECT_DATE'] = pd.to_datetime(df['SETTLED_REJECT_DATE'])

        df['FORM_NAME'].replace(FORM_NAME_MAPPING, inplace=True)
        df['PARA_DETAILS1'] = df['PARA_DETAILS']
        df['PARA_DETAILS2'] = df['PARA_DETAILS']
        df['PARA_DETAILS'].replace(PARA_DETAILS_MAPPING, inplace=True)
        df['PARA_DETAILS1'].replace(PARA_DETAILS_MAPPING1, inplace=True)
        df['PARA_DETAILS2'].replace(PARA_DETAILS_MAPPING2, inplace=True)

        df['EST'] = [str(x)[:15] for x in df['MEMBER_ID']]
        df['month'] = df['SETTLED_REJECT_DATE'].dt.month
        df['week'] = df['SETTLED_REJECT_DATE'].dt.isocalendar().week
        df['weekday'] = df['SETTLED_REJECT_DATE'].dt.day_name()
        df['mday'] = df['SETTLED_REJECT_DATE'].dt.day
        df['yday'] = df['SETTLED_REJECT_DATE'].dt.dayofyear
        df['TASK_ID'] = df['TASK_ID'].astype("int").astype("category")
        df['GROUP_ID'] = df['GROUP_ID'].astype("int").astype("category")
        df['FORM_NAME'] = df['FORM_NAME'].astype("category")
        df['PARA_DETAILS'] = df['PARA_DETAILS'].astype("category")
        df['dt'] = pd.to_datetime(df['SETTLED_REJECT_DATE']).dt.date
        df['month'] = pd.to_datetime(df['SETTLED_REJECT_DATE']).dt.month.astype(str).str.zfill(2)
        df['monthn'] = pd.to_datetime(df['SETTLED_REJECT_DATE'], format='%d/%m/%y, %I:%M %p').dt.month_name()
        df['date'] = pd.to_datetime(df['SETTLED_REJECT_DATE']).dt.day
        df['day'] = pd.to_datetime(df['SETTLED_REJECT_DATE']).dt.day_name()
        df['year'] = pd.to_datetime(df['SETTLED_REJECT_DATE']).dt.year
        df['ym'] = df['year'].astype(str) + df['month'].astype(str)
        df['md'] = df['monthn'].astype(str) + '-' + df['date'].astype(str)
        df['fy'] = year
        # Apply the function to the datetime column to get the quarter number
        df['quarter'] = df['SETTLED_REJECT_DATE'].apply(get_financial_year_quarter)

        df.loc[df['DAYS_TAKEN_FOR_REJECTION'].isnull(), 'outcome'] = 'settled'
        df.loc[df['DAYS_TAKEN_FOR_SETTLEMENT'].isnull(), 'outcome'] = 'rejected'

        df['TOTAL_AMOUNT'] = df['TOTAL_AMOUNT'].apply(process_row)

        df.loc[df['TOTAL_AMOUNT'].between(0, 499999, 'both'), 'cat'] = '<5lakh'
        df.loc[df['TOTAL_AMOUNT'].between(500000, 2499999, 'both'), 'cat'] = '5lakh-25lakh'
        df.loc[df['TOTAL_AMOUNT'].ge(2500000), 'cat'] = '>=25lakh'
        return df
    
    @staticmethod
    def col_grouped_rejection(df, filter_col):
        df['rejected'] = df.groupby(['month',filter_col ])['outcome'].transform(lambda x: (x == 'rejected').sum())
        df['settled'] = df.groupby(['month', filter_col])['outcome'].transform(lambda x: (x == 'settled').sum())
        df['total'] = df.groupby(['month', filter_col])['outcome'].transform('count')
        df['Rejected_Ratio'] = round(df['rejected']*100 / df['total'], 2)
        pivot_table = df.pivot_table(index=filter_col, columns='month', values='Rejected_Ratio', fill_value=0)
        pivot_table = pivot_table.round(2)
        for index, row in pivot_table.iterrows():
            form_name = index

            # Calculate the 'total', 'settled', and 'rejected' counts for this 'FORM_NAME'
            total_count = df[df[filter_col] == form_name]['total'].count()
            settled_count = df[(df[filter_col] == form_name) & (df['outcome'] == 'settled')]['settled'].count()
            rejected_count = df[(df[filter_col] == form_name) & (df['outcome'] =='rejected')]['rejected'].count()

            # Update the pivot table with the calculated values
            pivot_table.at[index, 'rejected'] = int(rejected_count)
            pivot_table.at[index, 'settled'] = int(settled_count)
            pivot_table.at[index, 'total'] = int(total_count)
            pivot_table.at[index, 'overall_ratio'] = round(int(rejected_count)*100/int(total_count),2)


            normal_table = pivot_table.reset_index()

        return normal_table

"""
from epftools import PeriodicityProcessor
path = '2022.csv'
processor = PeriodicityProcessor(path, '2023-10')
dall = processor.df
dall.head()
death10d = dall[dall['FORM_NAME']=="Death-10D"]
display(len(death10d))
display(death10d)
df2 = processor.col_grouped_rejection(dall,"GROUP_ID")
display(df2.head())
"""