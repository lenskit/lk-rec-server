Deployment
=============
All the packages necessary to run the recommendation server can be installed by using the requirements.txt file or the environment.yaml file, depending if you use pip or conda. Those packages can be easily installed by running either of these commands: 

    - pip install -r requirements.txt
    - conda env update --file environment.yaml


Docker-compose configuration
-------------------------------
If you just want to deploy the recommendation server and a Postgres database in Docker using data files located in test_db/ then follow these steps:

1) Move to the tests folder: cd tests
2) Run the command "docker-compose up".
3) Update the configuration values from util/train_save_model_config.json to reflect your desired values.
4) Remember to set these keys to true in the util/train_save_model_config.json

    - "create_models": true
    - "upload_models": true
5) Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.


Docker configuration
----------------------
If you want to use your own database, then you can build only the Dockerfile from lkweb folder. The steps to setup the recommendation server using Docker are:

1) Update the database configuration from config.cfg
2) Move to the lkweb folder: cd lkweb
3) Build the rec server image from the Dockerfile: docker build -t rec-server .
4) Update the values from util/train_save_model_config.json to reflect your desired values.
5) Remember to set these keys to true in the util/train_save_model_config.json

    - "create_models": true
    - "upload_models": true
6) Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.


No-Docker configuration
-------------------------
The steps to setup the recommendation server without Docker are:

1) Update the database configuration from config.cfg
2) Install the python packages by using the requirements.txt file or the environment.yaml file.
3) Start the recommendation server with 4 workers in gunicorn: gunicorn -w 4 wsgi:app
4) Update the values from util/train_save_model_config.json to reflect your desired values.
5) Remember to set these keys to true in the util/train_save_model_config.json

    - "create_models": true
    - "upload_models": true
6) Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.

It is recommended to create a virtualenv or anaconda environment before step 2.