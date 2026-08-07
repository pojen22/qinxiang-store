import sqlite3

conn = sqlite3.connect("database/qinxiang_store.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    barcode TEXT,
    price INTEGER,
    fridge_max INTEGER,
    fridge_now INTEGER
)
""")

conn.commit()

print("資料庫建立成功！")

conn.close()