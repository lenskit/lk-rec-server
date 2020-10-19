Deployment
=============
All the packages necessary to run the recommendation server are in the requirements.txt file, which can be easily installed with the command: pip -r requirements.txt

Docker configuration
======================
If you want to use a test db in Docker, then you can build the Dockerfile from test_db folder.
You can even build those two images and create a subnetwork by using the docker-compose.yml located in tests folder.

The steps to setup the recommendation server using Docker are:
1) Update the db configuration from config.cfg
2) Move to the service folder: cd service
3) Build the rec server image from the Dockerfile: docker build -t rec-server .
4) Run the train_save_model.py script to create the model files and upload them to the recommendation server.


No-Docker configuration
=========================
The steps to setup the recommendation server using Docker are:
1) Update the db configuration from config.cfg
2) Install the python packages from service\requirements.txt by calling: pip install -r requirements.txt
3) Start the recommendation server with 4 workers in gunicorn: gunicorn -w 4 wsgi:app
4) Run the train_save_model.py script to create the model files and upload them to the recommendation server.
