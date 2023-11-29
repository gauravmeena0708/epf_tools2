"""
For anomaly analysis following type of analysis may be checked
- Claims - monthwise, genderwise
- Claims - monthwise, formwise
- Claims - monthwise, estwise
- Claims - monthwise, Sectiowise

df_pivot = pd.pivot_table(df, values='CLAIM_ID', index=['month'], columns=["GROUP_ID"], 
                             margins=True,
                             aggfunc=lambda x: len(x))
df_pivot.to_excel("monthwise_groupwise.xlsx")
"""