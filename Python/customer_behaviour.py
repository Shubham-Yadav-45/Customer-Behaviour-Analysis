import pandas as pd

df=pd.read_csv('customer_shopping_behavior.csv')
# print(df.head(5))
# print(df.info())
# print(df.describe(include='all'))
# print(df.isnull().sum())

df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
# print(df.isnull().sum())

df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
# print(df.columns)
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
# # print(df.columns)

labels=['Young_adult','Adult','Middle_age','Senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)

# # print(df[['age','age_group']].head(10))

frequency_maping={
'Fortnightly':14,
'Annually':365,
'Monthly':30,
'Weekly':7,
'Bi-Weekly':14,
'Quarterly':90,
'Every 3 Months':90
}

df['days_of_purchase']=df['frequency_of_purchases'].map(frequency_maping)
# # print(df[['frequency_of_purchases','days_of_purchase']])
# # print((df['discount_applied']==df['promo_code_used']).all())

df=df.drop('promo_code_used',axis=1)
# print(df.columns)


# import pandas as pd
from sqlalchemy import create_engine

# Read CSV
# df = pd.read_csv("customer_shopping_behavior.csv")

# MySQL Details
username = "root"
password = "shubham"      # apna password
host = "localhost"
port = "3306"
database = "customer_behavior"

# Create Engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# Upload DataFrame to MySQL
df.to_sql(
    name="customer",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data uploaded successfully!")

# Read data back
query = "SELECT * FROM customer LIMIT 5"

with engine.connect() as conn:
    result = pd.read_sql(query, conn)

print(result)

