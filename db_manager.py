# TODO: change to use any sql db, use sqlite3 for now.
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime

class DbManager:
    def __init__(self):
        # self.connString = "data.db" # 'data.db'
        # self.type = "sqlite"
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}+{connector}://{user}:{password}@{server}/{database}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'])
    
    # def get_odbc_conn(self):
    #     connstr="Driver={MySQL ODBC 8.0 ANSI Driver};Server=localhost;Port=3306;Database=db;User=root;Password=dingoabc123;charset=UTF8"
    #     conn = pyodbc.connect(connstr)
    #     return conn

    def create_db_structure_with_data(self, movies, ratings):
    #     if self.type == "sqlite":
    #         conn = sqlite3.connect(self.connString)
    #         #c = conn.cursor()
    #         movies.to_sql("movies", conn, if_exists="replace")
    #         ratings.to_sql("ratings", conn, if_exists="replace")
    #     else:

            engine = create_engine(self.conn_string)

            # # Drop tables
            # sql.execute("DROP TABLE IF EXISTS movies", engine)
            # sql.execute("DROP TABLE IF EXISTS ratings", engine)

            # # # Create tables
            # sql.execute('''CREATE TABLE movies
            #         (movieId INTEGER, title VARCHAR(200), genres VARCHAR(100))''', engine)
            # sql.execute('''CREATE TABLE ratings
            #         (userId INTEGER, itemId INTEGER, rating FLOAT, timestamp DATETIME)''', engine)
           
            movies.to_sql('movies', con=engine, if_exists='replace', index=False)
            # #count = 0
            # for index, row in movies.iterrows():
            #     sql.execute("INSERT INTO movies VALUES ({movieId}, '{title}', '{genres}')".format(
            #         movieId=row['movieId'],
            #         title=row['title'].replace("'", r"\'"),
            #         genres=row['genres']), 
            #         engine)
            #     # count += 1
            #     # if count >= 100:
            #     #     break

            ratings.to_sql('ratings', con=engine, if_exists='replace', index=False, chunksize=10000)
            # # count = 0
            # for index, row in ratings.iterrows():
            #     sql.execute("INSERT INTO ratings VALUES ({userId}, {itemId}, {rating}, '{timestamp}')".format(
            #         userId=row['userId'],
            #         itemId=row['movieId'],
            #         rating=row['rating'],
            #         timestamp=datetime.utcfromtimestamp(int(row['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')),
            #         engine)
            #     # count += 1
            #     # if count >= 100:
            #     #     break

            # Create index
            sql.execute('''CREATE INDEX idx1 ON ratings (userId, movieId)''', engine)
            sql.execute('''CREATE INDEX idx1 ON movies (movieId);''', engine)

 
    def get_ratings(self):
        return sql.read_sql("SELECT userId as user, movieId as item, rating, timestamp FROM ratings;", create_engine(self.conn_string))

    def get_movies(self):
        return sql.read_sql("SELECT movieId, title, genres FROM movies;", create_engine(self.conn_string))

    def get_links(self):
        return sql.read_sql("SELECT movieId, imdbId, tmdbId FROM links;", create_engine(self.conn_string))

    def get_ratings_for_user(self, user_id):
        return sql.read_sql("SELECT movieId as item, rating FROM ratings WHERE userId = {userId}".format(
                    userId=user_id), create_engine(self.conn_string))