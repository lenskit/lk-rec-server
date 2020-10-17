-- CREATE DATABASE db OWNER postgres;

CREATE TABLE items (id INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL, genres VARCHAR(100));
CREATE TABLE rating ("user" INTEGER, item INTEGER, rating FLOAT, timestamp bigint(20), PRIMARY KEY ("user", item));