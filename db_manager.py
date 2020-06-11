# TODO: change to use any sql db, use sqlite3 for now.
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from config_reader import ConfigReader
from pandas.io import sql
from datetime import datetime

class DbManager:
    def __init__(self):
        reader = ConfigReader()
        db_connection = reader.get_value("db_connection")        
        self.conn_string = '{db_engine}+{connector}://{user}:{password}@{server}/{database}'.format(
            db_engine=db_connection['db_engine'],
            connector=db_connection['connector'],
            user=db_connection['user'],
            password=db_connection['password'],
            server=db_connection['server'],
            database=db_connection['database'])

    def get_ratings_for_user(self, user_id):
        return sql.read_sql("SELECT movieId as item, rating FROM ratings WHERE userId = {userId}".format(
                    userId=user_id), create_engine(self.conn_string))