-- CREATE DATABASE db OWNER postgres;

CREATE TABLE public.items (item INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL, genres VARCHAR(100));
CREATE TABLE public.ratings (user INTEGER, item INTEGER, rating FLOAT, timestamp bigint, PRIMARY KEY (user, item));