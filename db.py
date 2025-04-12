# import sqlite3

# def init_db():
#     conn = sqlite3.connect('specimens.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS measurements (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT,
#             microscope_size REAL,
#             actual_size REAL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def save_to_db(username, microscope_size, actual_size):
#     conn = sqlite3.connect('specimens.db')
#     c = conn.cursor()
#     c.execute('INSERT INTO measurements (username, microscope_size, actual_size) VALUES (?, ?, ?)',
#               (username, microscope_size, actual_size))
#     conn.commit()
#     conn.close()

import os
import sqlite3
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")

# SQLite setup
SQLITE_DB = 'specimens.db'

# MongoDB setup (only for production)
MONGO_URI = os.getenv("MONGO_URI")
# mongo_client = MongoClient(MONGO_URI) if ENV == "production" else None
mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
mongo_db = mongo_client.get_default_database() if mongo_client is not None else None
# print("mongo_db", mongo_db)
mongo_collection = mongo_db["measurements"] if mongo_db is not None else None

print(MONGO_URI)

try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def init_db():
    if ENV == "production":
        # MongoDB doesn't need table creation
        return
    else:
        conn = sqlite3.connect(SQLITE_DB)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                microscope_size REAL,
                actual_size REAL
            )
        ''')
        conn.commit()
        conn.close()


def save_to_db(username, microscope_size, actual_size):
    if ENV == "production":
        mongo_collection.insert_one({
            "username": username,
            "microscope_size": microscope_size,
            "actual_size": actual_size
        })
    else:
        conn = sqlite3.connect(SQLITE_DB)
        c = conn.cursor()
        c.execute('INSERT INTO measurements (username, microscope_size, actual_size) VALUES (?, ?, ?)',
                  (username, microscope_size, actual_size))
        conn.commit()
        conn.close()
