# import module 
import sqlite3
import pandas as pd 

#create connection to database
conn = sqlite3.connect('simple_apiv3/upload/Text_input.db')

try:
    #create table
    conn.execute("""create table cleansed_text (id INTEGER PRIMARY KEY AUTOINCREMENT, original_text TEXT, cleaned_text TEXT);""")
    print("Table created")
except:
    #if exist, do nothing
    print("Table already exist")


conn.commit()
conn.close()