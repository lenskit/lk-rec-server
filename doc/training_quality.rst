Training & quality check process
==================================

How to create the model files
-------------------------------
The script train_save_model.py located in the util folder is used to create the model files. Before running the script, you would like to update the get_algo_class() or get_topn_algo_class() methods to use your desired parameters in each algorithm.

You can simply call it like this: python train_save_model.py

You need to modify the file train_save_model_config.json to reflect your configuration. 
You can configure the database connection string, the recommendation server url, how to create the models, the algorithms to create models for, and other parameters.

The configuration for the script is defined in train_save_model_config.json. The different keys are:

* data_folder_path. The folder where the data file is.
* models_folder_path. The folder where the models will be saved.
* ratings_file_name. The name of the rating file.
* db_connection. It defines the different parts of the sql connection string.
* create_models. A flag used to indicate if new models will be created in the process.
* create_top_n_models. It is a boolean value (True or False) that specifies if the script will create the models using the topn algorithm.
* create_memory_optimized_models. It is a boolean value (True or False) that specifies if the models will be created with memory maps.
* from_data_files. It is a boolean value (True or False) that specifies if the data comes fron a file or a database.
* upload_models. A flag used to indicate if the models located in /models folder will be uploaded to the recommendation server.
* rec_server_base_url. The url of the recommendation server.
* algorithms. The algorithms to be used in the process. It is an array of strings.

How to extend the algorithms
------------------------------
If you want to create custom algorithms, simply you can extend the existing ones from Lenskit or create new ones by extending the base classes of Predictor or Recommender.
Then, you should modify the script train_save_model.py to import the new algorithm and then update the get_algo_class() or get_topn_algo_class() methods to include the new algorithm in the logic with your desired parameters.
Finally, just execute the script train_save_model.py
