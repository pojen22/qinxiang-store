import sqlite3

def search_product():

    conn = sqlite3.connect("database/qinxiang_store.db")
    cursor = conn.cursor()

    keyword = input("請輸入商品名稱或條碼：")

    cursor.execute("""
    SELECT name,
           price,
           fridge_max,
           fridge_now,
           restock_threshold
    FROM products
    WHERE name LIKE ?
       OR barcode = ?
    ORDER BY display_order
    """, ("%" + keyword + "%", keyword))

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("找不到商品")

    else:

        print()
        print("========== 查詢結果 ==========")

        for index, row in enumerate(rows, start=1):

            print(f"{index}. {row[0]}")

        print()

        while True:

            choice = input("請選擇商品：")

            if choice.isdigit():

                number = int(choice)

                if 1 <= number <= len(rows):
                    break

            print("❌ 輸入錯誤，請重新輸入。")

        row = rows[number - 1]

        print()
        print("==============================")
        print("商品名稱：", row[0])
        print("售價：", row[1], "元")
        print("冰箱容量：", row[2], "瓶")
        print("目前庫存：", row[3], "瓶")
        print("補貨門檻：", row[4], "瓶")
        print("==============================")

    conn.close()