from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
import config_reader
from pandas.io import sql
from datetime import datetime
import time

def get_conn_string():
    db_connection = config_reader.get_value("db_connection")        
    conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}'.format(
        db_engine=db_connection['db_engine'],
        connector=db_connection['connector'],
        user=db_connection['user'],
        password=db_connection['password'],
        server=db_connection['server'],
        database=db_connection['database'])
    return conn_string

def get_ratings_for_user(user_id):
    count = 0
    return try_connect_db("SELECT itemId as item, rating FROM ratings WHERE userId = {userId}".format(
                userId=user_id), count)

def try_connect_db(sql_statement, count):
    try:
        return sql.read_sql(sql_statement, create_engine(get_conn_string()))
    except:
        count += 1
        print("Trying to call the database again. Attempt number: " + str(count))
        time.sleep(3)
        if count > 5:
            raise
        else:
            return try_connect_db(sql_statement)

    # def get_ratings(self):
    #     return sql.read_sql("SELECT userId as user, itemId as item, rating, timestamp FROM ratings;", create_engine(conn_string))
