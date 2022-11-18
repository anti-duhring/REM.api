import mysql.connector
from dotenv import load_dotenv
import os

class ConnectDB:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
    
    def exec_DQL(self, sql):
        self.connect()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.disconnect()

        return result
    
    def exec_DML(self, sql):
        self.connect()
        self.cursor.execute(sql)
        self.connection.commit()
        self.disconnect()
