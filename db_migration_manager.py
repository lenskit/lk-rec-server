import sqlalchemy as db
from config_reader import ConfigReader

# connstr="Driver={MySQL ODBC 8.0 ANSI Driver};Server=localhost;Port=3306;Database=charity;User=root;Password=dingoabc123;"
# conn = pyodbc.connect(connstr)
# res = conn.execute("select * from donor")
# for r in res:
#     print(r[1])
#     print()

reader = ConfigReader()
db_connection = reader.get_value("db_connection")
print(db_connection)

#engine = db.create_engine('mysql+mysqlconnector://root:dingoabc123@localhost/db')
conn_string = '{db_engine}+{connector}://{user}:{password}@{server}/{database}'.format(
    db_engine=db_connection['db_engine'],
    connector=db_connection['connector'],
    user=db_connection['user'],
    password=db_connection['password'],
    server=db_connection['server'],
    database=db_connection['database'])
engine = db.create_engine(conn_string)
connection = engine.connect()
metadata = db.MetaData()
movies = db.Table('movies', metadata, autoload=True, autoload_with=engine)

query = db.select([movies])

ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet)

