# The Recommendation Server for Lenskit

The recommendation server for Lenskit is a web server that exposes LensKit’s recommendation and rating prediction capabilities.

The recommendation server makes it much easier to use LensKit in deployed applications and interactive research where end users are actively involved, extending the reach and research impact of LensKit. 

The user of the recommendation server can be anyone who knows how to build a web application, such as a software developer or a researcher. They need to create an application, which will itself have end users, and the recommendation server will generate recommendations for them. 

The recommendation server is able to handle multiple concurrent requests and load and reload of recommendation models. It also provides recommendations on demand based on the latest ratings end users have provided.

## User guide

To start using the recommendation server we need to follow some steps:

1. Create your model files by using util/train_save_model.py script. You need to have the ratings in your database or in a file. You can configure the database connection, folder paths and file names on util/train_save_model_config.json

2. As an optional step, you can create a python virtual environment or an anaconda environment.

3. Install the python dependencies by executing pip install -r lkweb/requirements.txt

4. Configure your database connection and default algorithm in lkweb/config.cfg

5. Start gunicorn. For instance, you can start it with 4 workers using the default port by running: gunicorn -w 4 wsgi:app

6. Place the model files inside the lkweb/models folder manually or upload them by using the endpoint ‘/algorithms/<algo>/modelfile’


## Functional testing

To make sure everything works fine, you can execute the functional tests by running pytest. We use pytest-docker, so all functional tests will be executed in a docker environment. The whole docker machines (recommendation server and database) will be created for you. You only need to place your items.csv and ratings.csv in the test_db folder and the whole process is automatically executed for you.


## Deployment
All the packages necessary to run the recommendation server are in lkweb/requirements.txt file, which can be easily installed with the command: pip -r lkweb/requirements.txt

### Docker-compose configuration
If you just want to deploy the recommendation server and a postgres database in docker using data files located in test_db/ then follow these steps:

1. Move to the tests folder

2. Run the command “docker-compose up”

3. Update the configuration values from util/train_save_model_config.json to reflect your desired values.

4. Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.

### Docker configuration
If you want to use a your own database, then you can build only the Dockerfile from lkweb folder.

The steps to setup the recommendation server using Docker are:

1. Update the db configuration from config.cfg

2. Move to the lkweb folder: cd lkweb

3. Build the rec server image from the Dockerfile: docker build -t rec-server .

4. Update the values from util/train_save_model_config.json to reflect your desired values.

5. Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.

### No-Docker configuration
The steps to setup the recommendation server without Docker are:

1. Update the db configuration from config.cfg

2. Install the python packages from lkweb/requirements.txt by calling: pip install -r requirements.txt

3. Start the recommendation server with 4 workers in gunicorn: gunicorn -w 4 wsgi:app

4. Update the values from util/train_save_model_config.json to reflect your desired values.

5. Run the util/train_save_model.py script to create the model files and upload them to the recommendation server.

It is recommended to create a python virtual environment before step 2.