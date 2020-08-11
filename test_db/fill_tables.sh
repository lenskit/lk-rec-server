#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
\copy items FROM '/var/lib/postgresql/items.csv' DELIMITER ',' CSV HEADER;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
\copy ratings FROM '/var/lib/postgresql/ratings.csv' DELIMITER ',' CSV;
EOSQL
