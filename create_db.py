import sqlite3

con = sqlite3.connect('NovaCart.db')
cur = con.cursor()

con.execute("CREATE TABLE Users(ID INTEGER PRIMARY KEY,Name TEXT, Email TEXT, Fav_Color TEXT)")
con.commit()
cur.close()
