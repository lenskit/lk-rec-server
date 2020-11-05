User guide
=========================
To start using the recommendation server we need to follow some steps:

1) First, you need to create a python virtualenv or an anaconda environment.
2) Install the python dependencies by executing pip or conda.

    - pip install -r requirements.txt
    - conda env update --file environment.yaml
3) Create your model files by using util/train_save_model.py script. You need to have the ratings in your database or in a file. You can configure the database connection, folder paths and file names on util/train_save_model_config.json
4) Configure your database connection and default algorithm for the recommendation server in config.cfg
5) Start gunicorn. For instance, you can start it with 4 workers using the default port by running: gunicorn -w 4 wsgi:app
6) Place the model files inside the lkweb/models folder manually or upload them by using the endpoint '/algorithms/<algo>/modelfile'

You can find more information about how to create the model files in the `Training & quality check process`_

You can easily create a docker image for the recommendation server by using the Dockerfile at the root of the project. For more information read the `Deployment guide`_.

.. _Training & quality check process: training_quality.html
.. _Deployment guide: deployment.html

Functional testing
-----------------------
To make sure everything works fine, you can execute the functional tests by running pytest. 
We use pytest-docker, so all functional tests will be executed in a docker environment. The whole docker machines (recommendation server and database) will be created for you. 
You only need to place your items.csv and ratings.csv in the test_db folder and the whole process is automatically executed for you.

