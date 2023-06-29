import sqlite3

con = sqlite3.connect('sqlite.db')

cur = con.cursor()

# 新建資料表
cur.execute("CREATE TABLE movie(title, year, score)")
con.commit()
con.close()