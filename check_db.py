import sqlite3
import os

db_path = 'db.sqlite3'
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("PRAGMA table_info(properties_property);")
    columns = cursor.fetchall()
    print("Columns in properties_property:")
    for col in columns:
        print(col[1])
except Exception as e:
    print(f"Error: {e}")

conn.close()
