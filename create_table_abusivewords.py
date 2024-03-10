# import module 
import sqlite3
import pandas as pd 

#create connection to database
conn = sqlite3.connect('simple_apiv3/data/abusive.db')

try:
    #create table
    conn.execute("""create table abusivewords (abusive varchar(255));""")
    print("Table created")
except:
    #if exist, do nothing
    print("Table already exist")

#import data to dataframe
df = pd.read_csv("simple_apiv3\data/abusive.csv", names = ['abusive'], encoding = 'latin-1', header = None)

#import df to db
df.to_sql(name='abusivewords', con=conn, if_exists = 'replace', index = False)

conn.commit()
conn.close()