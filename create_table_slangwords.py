# import module 
import sqlite3
import pandas as pd 

#create connection to database
conn = sqlite3.connect('simple_apiv3\data\slang.db')

try:
    #create table
    conn.execute("""create table slangwords (alay varchar(255), normal varchar(255));""")
    print("Table created")
except:
    #if exist, do nothing
    print("Table already exist")

#import data to dataframe
df = pd.read_csv("simple_apiv3\data/new_kamusalay.csv", names = ['alay', 'normal'], encoding = 'latin-1', header = None)

#import df to db
df.to_sql(name='slangwords', con=conn, if_exists = 'replace', index = False)

conn.commit()
conn.close()