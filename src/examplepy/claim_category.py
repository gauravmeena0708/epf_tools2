import pandas as pd

"""
from claim_category import Claim_Category
df = pd.read_csv('claims.csv')
category_generator = Claim_Category(15, 20)
df  = category_generator.add_bins_and_categories(df)
#category_generator.get_flat_pivot(df,"GROUP ID","INT_CATEGORY")
df.head()
"""
class Claim_Category:
    STATUS_MAPPING  = {
        'Pending at DA Accounts'                          : 'DA',
        'Pending at DA Accounts [EDIT]'                   : 'DA',
        
        'Pending at Dispatch'                             : 'Other',
        'Pending at DA SCROLL'                            : 'Other',
        'Pending at CHEQUE Alottment/Printing'            : 'Other',
        'Pending [ Referred to Other Office ]'            : 'Other',
        
        'Pending at SS/AO/AC Accounts [Rejection]'        : 'Rejection',
        
        'Pending at SS/AO/AC Accounts'                    : 'App',
        'Pending [ Approver Pending ]'                    : 'App',
        'Pending at DA Pension [Worksheet Generation]'    : 'Other',
        'Pending at DA Pension [PPO Generation]'          : 'Other',
        'Pending at DA Pension [SC worksheet generation]' : 'Other',
        'Pending at E-Sign'                               : 'Other',
        'Pending at AC Pension [Worksheet Generation]'    : 'Other',
        'Pending at AC Pension [PPO Generation]'          : 'Other',
        'Pending at DA Pension [SC verification awaited]' : 'Other',
        'Pending at Invalid Status'                       : 'Other',
        'Pending at AC Pension [SC generation]'           : 'Other',
    }
    
    CLAIM_TYPE_MAPPING  = {
        'Form-13 (Transfer Out) [ WITH-MONEY ]'           : 'FORM-13',
        'Form-13 (Transfer In / Same Office)'             : 'FORM-13',
        'Form-10C [ Withdrawal Benefit ] '                : '10C',
        'Form-5IF'                                        : 'Death_Claim',
        'Form-10D'                                        : '10D',
        'Form-13 (Transfer Out) [ OTHERS ]'               : 'FORM-13',
        'Form-20'                                         : 'Death_Claim',
        'Form-10D [ Death Case ]'                         : 'Death_Claim',
        'Form-19'                                         : '19',
        'Form-31'                                         : 'Form-31',
        'Form-31 [ 68J / Illness ]'                       : 'Form-31',
        'Form-31 [ COVID ]'                               : 'Form-31',
        'Form-13 (Transfer Out) [ WITHOUT-MONEY  ]'       : 'FORM-13',
        'Form-10C [ Scheme Certificate ]'                 : '10C'
    }
    
    INT_MAPPING  = {
        'Form-13 (Transfer Out) [ WITH-MONEY ]'           : 'Int',
        'Form-13 (Transfer In / Same Office)'             : 'Int',
        'Form-10C [ Withdrawal Benefit ] '                : 'Non_int',
        'Form-5IF'                                        : 'Death Clm',
        'Form-10D'                                        : 'Non_int',
        'Form-13 (Transfer Out) [ OTHERS ]'               : 'Int',
        'Form-20'                                         : 'Death Clm',
        'Form-10D [ Death Case ]'                         : 'Death Clm',
        'Form-19'                                         : 'Int',
        'Form-31'                                         : 'Non_int',
        'Form-31 [ 68J / Illness ]'                       : 'Non_int',
        'Form-31 [ COVID ]'                               : 'Non_int',
        'Form-13 (Transfer Out) [ WITHOUT-MONEY  ]'       : 'Int',
        'Form-10C [ Scheme Certificate ]'                 : 'Non_int'
    }

    COLUMNS  = ['CLAIM ID', 'TASK ID', 'PENDING DAYS', 'STATUS', 'CLAIM TYPE']
    RENAME_COLS  = {'CLAIM ID': 'ID', 'TASK ID': 'TASK ID'}
    
    def __init__(self, cut_off1, cut_off2):
        self.status_mapping = self.STATUS_MAPPING
        self.claim_type_mapping = self.CLAIM_TYPE_MAPPING
        self.int_mapping = self.INT_MAPPING
        self.cut_off1 = cut_off1
        self.cut_off2 = cut_off2
        self.days_bins = [0,cut_off1,cut_off2,10000]
        self.days_labels = [f'0-{cut_off1}', f'{cut_off1+1}-{cut_off2}',f'>{cut_off2}']
        self.columns = self.COLUMNS
        self.rename_cols = self.RENAME_COLS

    def filter_and_rename_columns(self, df):
        filtered_df = df[self.columns]
        renamed_df = filtered_df.rename(columns=self.rename_cols)
        return renamed_df

    def assign_categories(self, row):
        days = row["days_Group"]
        status = row["STATUS"]
        claim_type = row["INT_CATEGORY"]

        if status == "Other":
            category = "Other"
        elif status == "Rejection":
            category = "Rejection"
        else:
            if claim_type == "Death Clm":
                category = f"{claim_type}"
            elif claim_type == "Int":
                if days != self.days_labels[0]:
                    category = f"{status} {claim_type} >{self.cut_off1}"
                else:
                    category = "Other"  # status
            else:
                if days == self.days_labels[2]:
                    category = f"{status} {claim_type} >{self.cut_off2}"
                else:
                    category = "Other"  # status

        return category

    def add_bins_and_categories(self, df):
        df = self.filter_and_rename_columns(df)
        df['GROUP ID'] = [int(str(x)[:3]) for x in df['TASK ID']]
        df['STATUS'] = df['STATUS'].replace(self.status_mapping)
        df['INT_CATEGORY'] = df['CLAIM TYPE'].replace(self.int_mapping)
        df['CLAIM TYPE'] = df['CLAIM TYPE'].replace(self.claim_type_mapping)
        df['days_Group'] = pd.cut(df['PENDING DAYS'], self.days_bins, labels=self.days_labels)
        df['days_Group'] = df['days_Group'].astype(str)
        df['CATEGORY'] = df.apply(self.assign_categories, axis=1)
        return df

    def get_flat_pivot(self,df,INDEX,COLUMN):
        return pd.pivot_table(df, values='ID', index=[INDEX], columns=[COLUMN], 
                             margins=True, aggfunc='count').fillna(0).astype(int).reset_index()


