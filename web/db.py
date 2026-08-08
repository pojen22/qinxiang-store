import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "database", "qinxiang_store.db")


def get_connection():
    return sqlite3.connect(DATABASE)