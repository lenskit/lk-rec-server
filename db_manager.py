# TODO: change to use any sql db, use sqlite3 for now.
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime
import time

class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'])
        self.count = 0

    def get_ratings_for_user(self, user_id):
        return self.try_connect_db("SELECT itemId as item, rating FROM ratings WHERE userId = {userId}".format(
                    userId=user_id))

    def try_connect_db(self, sql_statement):
        try:
            return sql.read_sql(sql_statement, create_engine(self.conn_string))
        except:
            self.count += 1
            print("Trying to call the database again. Attempt number: " + str(self.count))
            time.sleep(3)
            if self.count > 5:
                raise
            else:
                return self.try_connect_db(sql_statement)

    def get_ratings(self):
        return sql.read_sql("SELECT userId as user, itemId as item, rating, timestamp FROM ratings;", create_engine(self.conn_string))
