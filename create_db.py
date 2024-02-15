import sqlite3

con = sqlite3.connect('NovaCart.db')
cur = con.cursor()

con.execute("CREATE TABLE Users(Name TEXT, Email TEXT, Password TEXT)")
cur.close()
