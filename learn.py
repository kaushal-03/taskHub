import pandas as pd

df = pd.read_excel("/Users/kaushalsiriguppa/Downloads/domain_category_mapping.xlsx")
print(df[df['Domain'] == '@redbus.com']['Category'].values)


