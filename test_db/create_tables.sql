-- CREATE DATABASE db OWNER postgres;

CREATE TABLE items (item INTEGER PRIMARY KEY, title VARCHAR(200) NOT NULL, genres VARCHAR(100));
CREATE TABLE rating ("user" INTEGER, item INTEGER, rating FLOAT, timestamp bigint, PRIMARY KEY ("user", item));

-- only used for the demo app:
CREATE TABLE users ("user" INTEGER PRIMARY KEY NOT NULL, userName varchar(100) NULL)