import mysql.connector
import pandas as pd

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def query(self, query):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            data = pd.read_sql(query, connection)
            connection.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return pd.DataFrame()
