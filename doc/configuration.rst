Configuration
===============
The main configuration file is config.cfg in the root folder. The things you can configure in this file are:

* DEFAULT_ALGORITHM. It specifies the default algorithm to be used in the recommendation server.
* DB_CONNECTION_*Extending the recommendation server.
* It specifies the different parts of the database connection string.
* RATING_TABLE_TABLE_NAME. It specifies the rating table name.
* RATING_TABLE_USER_COLUMN_NAME. It specifies the user column name of the rating table.
* RATING_TABLE_ITEM_COLUMN_NAME. It specifies the item column name of the rating table.
* RATING_TABLE_RATING_COLUMN_NAME. It specifies the rating column name of the rating table.

How to extend the recommendation server
------------------------------------------
It is easy to add a new endpoint in the recommendation server that uses the current model files. We used python decorators to make the methods extensibles. 
The two files that need to be modified to add new endpoints are app.py and model_manager.py. For an example, check the section "Extending the recommendation server" of `Examples`_

.. _Examples: examples.html#Extending-the-recommendation-server
