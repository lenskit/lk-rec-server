FROM python:3.8-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

# ENTRYPOINT ["python"]
# CMD ["app.py"]
#CMD ["python", "app.py"]
CMD ["gunicorn --bind 0.0.0.0:5000 -w 4 wsgi:app"]