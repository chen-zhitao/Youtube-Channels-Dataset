import sqlite3
import pandas as pd
import os

cur_path = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(cur_path, "..","..", "data")
db_path = os.path.join(data_directory, "channels.db")
csv_path = os.path.join(data_directory, "channels.csv")

def main():
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM channels"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df.to_csv(csv_path, index=False)
    return


def load_csv():
    df = pd.read_csv(csv_path)
    print(df.head())
    return


if __name__ == '__main__':
    main()
    load_csv()