# TODO: change to use any sql db, use sqlite3 for now.
import sqlite3
import pandas as pd

class DbManager:
    def __init__(self):
        self.connString = "data.db" # 'data.db'
    
    def create_structure_with_data(self, ratings):
        conn = sqlite3.connect(self.connString)
#        c = conn.cursor()

        ratings.to_sql("ratings", conn, if_exists="replace")

        # # Drop table
        # c.execute("DROP TABLE ratings")

        # # Create table
        # c.execute('''CREATE TABLE ratings
        #      (user integer, item integer, rating real, timestamp text)''')
        # count = 0

        # for index, row in ratings.iterrows():
        #     # Insert a row of data
        #     #c.execute("INSERT INTO ratings VALUES (" + row['user'] + "," + row['item'] + "," + row['rating'] + ",'" + row['timestamp'] + "')")

        #     user = row['user']
        #     item = row['item']
        #     rating = row['rating']
        #     timestamp = row['timestamp']
        #     #c.execute("INSERT INTO ratings VALUES (?,?,?,?)", (row['user'], row['item'], row['rating'], row['timestamp']))
        #     c.execute("INSERT INTO ratings VALUES (?,?,?,?)", (user, item, rating, timestamp))
            
        #     count += 1
        #     if count >= 100:
        #         break
        
        conn.commit()
        conn.close()
    
    def get_ratings(self):
        conn = sqlite3.connect(self.connString)
        return pd.read_sql_query("select user, item, rating, timestamp from ratings LIMIT 5;", conn)
