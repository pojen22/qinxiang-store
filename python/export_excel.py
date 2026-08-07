import sqlite3
import os
from datetime import datetime
from openpyxl import Workbook


def export_excel():

    conn = sqlite3.connect("database/qinxiang_store.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        barcode,
        price,
        fridge_max,
        fridge_now,
        display_order,
        restock_threshold
    FROM products
    ORDER BY display_order
    """)

    rows = cursor.fetchall()

    if not os.path.exists("export"):
        os.mkdir("export")

    filename = datetime.now().strftime("商品資料_%Y%m%d_%H%M%S.xlsx")

    filepath = os.path.join("export", filename)

    wb = Workbook()

    ws = wb.active

    ws.title = "商品資料"

    ws.append([
        "商品名稱",
        "條碼",
        "售價",
        "冰箱容量",
        "目前庫存",
        "巡冰箱順序",
        "補貨門檻"
    ])

    for row in rows:
        ws.append(row)

    wb.save(filepath)

    conn.close()

    print("✅ 匯出完成")
    print(filepath)