Get up and running guide
=========================
To start using the recommendation server we need to follow some steps:
1) Create your model files by using util/train_save_model.py script. You need to have the ratings in your database or in a file. You can configure the database connection, folder paths and file names on util/train_save_model_config.json
2) As an optional step, you can create a python virtual environment or an anaconda environment.
3) Install the python dependencies by executing pip install -r requirements.txt
4) Configure your database connection and default algorithm in config.json
5) Start gunicorn. For instance, you can start it with 4 workers using the default port by running: gunicorn -w 4 wsgi:app
6) Place the model files inside the /models folder manually or by using the endpoint '/algorithms/<algo>/modelfile'

Deployment
=========================
You can easily create a docker image for the recommendation server by using the Dockerfile at the root of the project.

Testing
=========================
You can execute the functional tests by creating a docker environment. We use pytest-docker, so you only need to execute pytest in the command line. The whole docker machines (recommendation server and database) will be created for you. You only need to place your items.csv and ratings.csv in test_db folder. 

