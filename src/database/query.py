import sqlite3
import os

cur_path = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(cur_path, "..","..", "data")
db_file = os.path.join(data_directory, "channels.db")

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

# cursor.execute("""
#                SELECT * FROM channels
#                LIMIT 10
#                """)

cursor.execute("""
                SELECT count(*) FROM channels
                """)


rows = cursor.fetchall()
for row in rows:
   print(row)
   print()
   print('-'*10)
   print()








