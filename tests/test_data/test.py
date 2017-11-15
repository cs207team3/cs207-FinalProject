import sqlite3

db = sqlite3.connect('nasa.sqlite')
cursor = db.cursor()
ret = cursor.execute('select * from LOW').fetchall()
print(ret)