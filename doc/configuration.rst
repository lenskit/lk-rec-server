Configuration
===============
The main configuration file is config.cfg with the extension .cfg. The things you can configure in this file are:
    DEFAULT_ALGORITHM: it specifies the default algorithm to be used in the recommendation server.
    DB_CONNECTION_*: it specifies the different parts of the database connection string.
    RATING_TABLE_TABLE_NAME: it specifies the rating table name.
    RATING_TABLE_USER_COLUMN_NAME: it specifies the user column name of the rating table.
    RATING_TABLE_ITEM_COLUMN_NAME: it specifies the item column name of the rating table.
    RATING_TABLE_RATING_COLUMN_NAME: it specifies the rating column name of the rating table.

All the packages necessary to run the recommendation server are in the requirements.txt file, which can be easily installed with the command: pip -r requirements.txt

Docker configuration
The steps to setup the recommendation server using Docker are:
    1) 

How to extend the recommendation server
==========================================
It is easy to add a new endpoint in the recommendation server that uses the current model files. We used python decorators to make the methods extensibles. The two files that need to be modified are app.py and model_manager.py.
