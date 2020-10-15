from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib
from pandas.io import sql
from datetime import datetime
import time
import logging
import sys

def get_conn_string(config):
    conn_string = '{db_engine}{connector}://{user}:{password}@{server}/{database}'.format(
        db_engine=config['DB_CONNECTION_DB_ENGINE'],
        connector=config['DB_CONNECTION_CONNECTOR'],
        user=config['DB_CONNECTION_USER'],
        password=config['DB_CONNECTION_PASSWORD'],
        server=config['DB_CONNECTION_SERVER'],
        database=config['DB_CONNECTION_DATABASE'])
    return conn_string

def get_ratings_for_user(user_id, config):
    count = 0
    rating_table_name = config["RATING_TABLE_TABLE_NAME"]
    user_column_name = config["RATING_TABLE_USER_COLUMN_NAME"]
    item_column_name = config["RATING_TABLE_ITEM_COLUMN_NAME"]
    rating_column_name = config["RATING_TABLE_RATING_COLUMN_NAME"]

    # if user_column_name == 'user':
    #     user_column_name = f"\"{user_column_name}\""

    check_sql = f"""SELECT 1 as "value"
        FROM information_schema.columns 
        WHERE table_name='{rating_table_name}' and column_name='{rating_column_name}';"""
    check_rating_column = try_connect_db(check_sql, count, config)
    if len(check_rating_column) > 0:
        count = 0
        return try_connect_db(f'''SELECT {item_column_name}, {rating_column_name} 
            FROM {rating_table_name} t WHERE t.{user_column_name} = {user_id}''', count, config)
    else:
        count = 0
        logging.info("No column rating. Using 1 as rating value.")
        return try_connect_db(f'''SELECT {item_column_name}, 1
            FROM {rating_table_name} t WHERE t.{user_column_name} = {user_id}''', count, config)

def try_connect_db(sql_statement, count, config):
    try:
        engine = create_engine(get_conn_string(config), pool_size=config["DB_CONNECTION_POOL_SIZE"])
        result = sql.read_sql(sql_statement, engine)
        engine.dispose()
        return result
    except:
        count += 1
        logging.error(f"Unexpected error: {sys.exc_info()[0]}")
        logging.warning("Trying to call the database again. Attempt number: " + str(count))
        time.sleep(3)
        if count > 4:
            raise
        else:
            return try_connect_db(sql_statement, count, config)