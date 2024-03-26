import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from epftools import PeriodicityProcessor as pp
import pandas as pd


pd.options.mode.copy_on_write = True
path = 'data/2024.csv'
dall = pp.read_periodicity(path, '2023-24')
temp_df = pd.DataFrame(columns=['text_column', 'blank', 'reason1', 'reason2', 'reason_category'])
temp_df[['blank', 'reason1', 'reason2']] = dall['REJECT_REASON'].str.split(r'\d\)', n=2, expand=True)

dall['reason1'] = temp_df['reason1'].str.strip()
dall['reason2'] = temp_df['reason2'].str.strip()
dall['days_taken'] = dall['DAYS_TAKEN_FOR_REJECTION'].combine_first(dall['DAYS_TAKEN_FOR_SETTLEMENT'])
dall = dall.drop(['DAYS_TAKEN_FOR_REJECTION', 'DAYS_TAKEN_FOR_SETTLEMENT'], axis=1)
dall['days_category'] = pd.cut(dall['days_taken'],
                             bins=[0, 5, 10, 15, 20, float('inf')],
                             labels=['0-5', '6-10', '11-15', '16-20', '>20'],
                             right=False)
dall2 = dall[dall['outcome'] == 'rejected']
dall2.head()

df = pd.read_csv("F:\\git\\epftools\\tests\\todo\\reason_category.csv")
df['reason'] = df['reason'].fillna(' ')
df['category'] = df['category'].fillna(' ')
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(df['reason'])
y_train = df['category']


model = LogisticRegression()
model.fit(X_train, y_train)

"""
For ML based Rejection categorization
"""
dall2['reason1'] = dall2['reason1'].fillna('').copy()
X_all2 = vectorizer.transform(dall2['reason1'])
all2_predictions = model.predict(X_all2)
all2_probabilities = model.predict_proba(X_all2)
dall2['predicted_category'] = all2_predictions.copy()
dall2['confidence'] = all2_probabilities.max(axis=1).copy()
display(dall2.head())
cols = ["GROUP_ID","TASK_ID","EST","CLAIM_ID","PARA_DETAILS","MEMBER_ID","reason1","predicted_category","confidence"]
dall2[(dall2['STATUS']=='Rejected')][cols].to_excel("rejection_cat.xlsx",index=False)