import os
import sqlite3

# ==============================
# PostgreSQL / SQLite 資料庫連線
# ==============================

DATABASE_URL = os.environ.get("DATABASE_URL")

# ------------------------------
# PostgreSQL Cursor
# 將原本 SQLite 的 ? 參數
# 自動轉成 PostgreSQL 的 %s
# ------------------------------

class PostgreSQLCursor:

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, sql, params=()):
        sql = sql.replace("?", "%s")
        return self.cursor.execute(sql, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __iter__(self):
        return iter(self.cursor)


class PostgreSQLConnection:

    def __init__(self, connection):
        self.connection = connection

    def cursor(self):
        return PostgreSQLCursor(
            self.connection.cursor()
        )

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()


# ==============================
# 取得資料庫連線
# ==============================

def get_connection():

    # Render / 正式網站
    if DATABASE_URL:

        import psycopg2

        connection = psycopg2.connect(
            DATABASE_URL
        )

        return PostgreSQLConnection(
            connection
        )

    # 本機測試
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    DATABASE = os.path.join(
        BASE_DIR,
        "database",
        "qinxiang_store.db"
    )

    return sqlite3.connect(
        DATABASE
    )