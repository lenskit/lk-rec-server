FROM python:3.8-buster

ENV NUMBA_NUM_THREADS 1
ENV MKL_NUM_THREADS 1
ENV OMP_NUM_THREADS 1
ENV OPENBLAS_NUM_THREADS 1

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./lkweb /lkweb
COPY ./app.py app.py
COPY ./wsgi.py wsgi.py
COPY ./config.cfg config.cfg

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-t", "2400", "wsgi:app"]