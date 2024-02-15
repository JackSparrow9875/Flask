import mysql.connector

my_db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root'
)

cur = my_db.cursor()

cur.execute("CREATE DATABASE NovaCart")

cur.execute("SHOW DATABASES")
for db in cur:
    print(db)