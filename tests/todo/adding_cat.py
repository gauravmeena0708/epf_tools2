
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Assuming df is your training dataframe with 'text_column' and 'reason_category'
# columns, and df_all2 is your testing dataframe with 'text_column' and 'reason_category' columns

# Read your CSV file for training
df = pd.read_csv("reason_category.csv")
df['reason'] = df['reason'].fillna('')

# Vectorize the text_column for training
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(df['reason'])
y_train = df['category']

# Model selection and training
model = LogisticRegression()
model.fit(X_train, y_train)



# Handle missing values in the 'reason' column for testing
dall2['reason1'] = dall2['reason1'].fillna('').copy()

# Vectorize the text_column for testing
X_all2 = vectorizer.transform(dall2['reason1'])

# Prediction on the entire dataset df_all2
all2_predictions = model.predict(X_all2)

# Probability estimates for each class on the entire dataset df_all2
all2_probabilities = model.predict_proba(X_all2)

# Get the predicted category and confidence based on the maximum probability on df_all2
dall2['predicted_category'] = all2_predictions.copy()
dall2['confidence'] = all2_probabilities.max(axis=1).copy()

# Display the dataframe df_all2 with predicted categories and confidence
display(dall2.head())
cols = ["GROUP_ID","TASK_ID","EST","CLAIM_ID","PARA_DETAILS","MEMBER_ID","reason1","predicted_category","confidence"]
dall2[(dall2['STATUS']=='Rejected') & (dall2['FORM_NAME']=='31')][cols].to_excel("december1.xlsx",index=False)