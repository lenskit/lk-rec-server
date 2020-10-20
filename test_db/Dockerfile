FROM postgres

#VOLUME ./files:/var/lib/postgresql/data

ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB db 

ADD create_tables.sql /docker-entrypoint-initdb.d
ADD fill_tables.sh /docker-entrypoint-initdb.d
ADD insert_new_ratings.sql /docker-entrypoint-initdb.d

RUN chmod a+r /docker-entrypoint-initdb.d/*

ADD files/items.csv /var/lib/postgresql
ADD files/ratings.csv /var/lib/postgresql

#EXPOSE 6000