Training & quality check process
=====================================

How to create the model files
===============================
The script train_save_model.py located in the util folder is used to create the model files. You can simply call it like this:
    python train_save_model.py algos from_data_files
Where:
    algos are the name of the algorithms separated by commas.

A usage example could be:
    python train_save_model.py popular,bias,itemitem,useruser,biasedmf,implicitmf,funksvd,bpr

The configuration for the script is defined in train_save_model_config.json. The different keys are:
    data_folder_path: It specifies the folder where the data file is.
    models_folder_path: It specifies the folder where the models will be saved.
    ratings_file_name: It specifies the name of the rating file.
    db_connection: It defines the different parts of the sql connection string.
    create_top_n_models: It is a boolean value (True or False) that specifies if the script will create the models using the topn algorithm.
    create_memory_optimized_models: It is a boolean value (True or False) that specifies if the models will be created with memory maps.
    from_data_files: It is a boolean value (True or False) that specifies if the data comes fron a file or a database.

How to extend the algorithms
===============================
If you want to create custom algorithms, simply you can extend the existing ones from Lenskit or create new ones by extending the base classes of Predictor or Recommender.
Then, you should modify the script train_save_model.py to import the new algorithm and then update the get_algo_class() or get_topn_algo_class() methods to include the new algorithm in the logic.
Finally, just execute the script train_save_model.py
