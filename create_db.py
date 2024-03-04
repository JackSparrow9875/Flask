import sqlite3

con = sqlite3.connect('NovaCart.db')
con.close()

print('NovaCart database has been successfully created')
