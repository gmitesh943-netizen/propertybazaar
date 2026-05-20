import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(properties_property)")
cols = cursor.fetchall()
with open('debug_db.txt', 'w') as f:
    for col in cols:
        f.write(f"{col[1]}\n")
conn.close()
