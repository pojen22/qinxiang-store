import sqlite3
import traceback
from datetime import datetime

from backup import backup_database
from search import search_product
from scan_fridge import scan_fridge
from restock import show_restock
from product_manage import product_manage
from export_excel import export_excel

backup_database()

conn = sqlite3.connect("database/qinxiang_store.db")
cursor = conn.cursor()

while True:

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM products
    WHERE fridge_max - fridge_now >= restock_threshold
    """)
    restock_count = cursor.fetchone()[0]

    print("\n==============================")
    print("      親鄉商店數位助理")
    print("==============================")
    print("日期：", today)
    print("商品總數：", product_count, "項")
    print("待補貨：", restock_count, "項")
    print("==============================")

    print("1. 商品詢價")
    print("2. 巡冰箱")
    print("3. 今日補貨")
    print("4. 商品管理")
    print("5. 匯出Excel")
    print("6. 離開")

    choice = input("請選擇：")

    if choice == "1":
        search_product()

    elif choice == "2":
        scan_fridge()

    elif choice == "3":
        show_restock()

    elif choice == "4":
        try:
            product_manage()
        except Exception:
            traceback.print_exc()

    elif choice == "5":
        export_excel()

    elif choice == "6":
        conn.close()
        print("系統結束")
        break

    else:
        print("輸入錯誤")