import sqlite3

con = sqlite3.connect('sqlite.db')

f = open('bicasa.db.sql','r')
str = f.read()
cur = con.cursor()
cur.executescript(str)

con.commit()
con.close()