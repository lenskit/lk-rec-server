Get up and running guide
=========================
To start using the recommendation server we need to follow some steps:
1) Create your model files by using util/train_save_model.py script. You need to have the ratings in your database or in a file. You can configure the database connection, folder paths and file names on util/train_save_model_config.json
2) Place the model files inside the /models folder.
3) As an optional step, you can create a python virtual environment or an anaconda environment.
4) Install the python dependencies by executing pip install -r requirements.txt
5) Configure your database connection and default algorithm in config.json
6) Start gunicorn. For instance, you can start it with 4 workers by running: gunicorn -w 4 wsgi:app