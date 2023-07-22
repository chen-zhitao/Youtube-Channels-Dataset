import sqlite3
import os

cur_path = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(cur_path, "..","..", "data")
db_file = os.path.join(data_directory, "channels.db")

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id TEXT PRIMARY KEY NOT NULL,
        url TEXT,
        description TEXT
    )
""")

cursor.close()
conn.commit()
conn.close()        

