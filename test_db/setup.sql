-- CREATE DATABASE db OWNER postgres;

CREATE TABLE public.items (itemId INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL, genres VARCHAR(100));
CREATE TABLE public.ratings (userId INTEGER, itemId INTEGER, rating FLOAT, timestamp bigint, PRIMARY KEY (userId, itemId));