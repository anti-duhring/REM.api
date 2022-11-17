import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def connect_mysql(func):
    def wrapper():
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
        )
        cursor = connection.cursor()

        func(cursor=cursor, connection=connection)

        cursor.close()
        connection.close()

    return wrapper
