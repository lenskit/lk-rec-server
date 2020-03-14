import sqlalchemy as db

# connstr="Driver={MySQL ODBC 8.0 ANSI Driver};Server=localhost;Port=3306;Database=charity;User=root;Password=dingoabc123;"
# conn = pyodbc.connect(connstr)
# res = conn.execute("select * from donor")
# for r in res:
#     print(r[1])
#     print()

engine = db.create_engine('mysql+mysqlconnector://root:dingoabc123@localhost/db')
connection = engine.connect()
metadata = db.MetaData()
movies = db.Table('movies', metadata, autoload=True, autoload_with=engine)

query = db.select([movies])

ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print(ResultSet[0].keys())

