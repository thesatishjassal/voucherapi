import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

DB_HOST = os.getenv("DATABASE_HOST")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_NAME = os.getenv("DATABASE_NAME")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        # password= DB_PASSWORD,
        database = DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None