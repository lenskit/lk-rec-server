# TODO: change to use any sql db, use sqlite3 for now.
import sqlite3
import pandas as pd
import pyodbc
import sqlalchemy
import urllib

class DbManager:
    def __init__(self):
        self.connString = "data.db" # 'data.db'
        self.type = "sqlite"
    
    def get_odbc_conn(self):
        connstr="Driver={MySQL ODBC 8.0 ANSI Driver};Server=localhost;Port=3306;Database=db;User=root;Password=dingoabc123;charset=UTF8"
        conn = pyodbc.connect(connstr)
        return conn

    def create_structure_with_data(self, movies, ratings, links):
        if self.type == "sqlite":
            conn = sqlite3.connect(self.connString)
            #c = conn.cursor()
            movies.to_sql("movies", conn, if_exists="replace")
            ratings.to_sql("ratings", conn, if_exists="replace")
            links.to_sql("links", conn, if_exists="replace")
        else:
            conn = self.get_odbc_conn()
            # conn = sqlalchemy.create_engine(
            #        "mysql+pyodbc://root:dingoabc123@localhost/db",
            #        echo=False)
            # params = urllib.parse.quote_plus("Driver={MySQL ODBC 8.0 ANSI Driver};Server=localhost;Port=3306;Database=db;User=root;Password=dingoabc123;")
            # conn = sqlalchemy.create_engine("mysql+pyodbc:///?odbc_connect=%s" % params)

            # ratings.to_sql("movies", conn, if_exists="replace")

            # # Drop table
            conn.execute("DROP TABLE IF EXISTS movies")

            # # Create table
            conn.execute('''CREATE TABLE movies
                    (movieId INTEGER, title VARCHAR(200), genres VARCHAR(100))''')
            count = 0

            for index, row in movies.iterrows():
                # Insert a row of data
                #c.execute("INSERT INTO ratings VALUES (" + row['user'] + "," + row['item'] + "," + row['rating'] + ",'" + row['timestamp'] + "')")

                movieId = row['movieId']
                title = row['title']
                genres = row['genres']
                # c.execute("INSERT INTO ratings VALUES (?,?,?,?)", (row['user'], row['item'], row['rating'], row['timestamp']))
                # conn.execute(f"INSERT INTO movies(movieId, title, genres) VALUES ({movieId},'{title}','{genres}')")
                conn.execute("INSERT INTO movies(movieId, genres) VALUES (?,?)", movieId, genres)
                
                count += 1
                if count >= 100:
                    break
            
        conn.commit()
        conn.close()
    
    def get_ratings(self):
        conn = sqlite3.connect(self.connString)
        return pd.read_sql_query("select user, item, rating, timestamp from ratings;", conn)

    def get_movies(self):
        conn = sqlite3.connect(self.connString)
        return pd.read_sql_query("select movieId, title, genres from movies;", conn)

    def get_links(self):
        conn = sqlite3.connect(self.connString)
        return pd.read_sql_query("select movieId, imdbId, tmdbId from links;", conn)