import sqlite3

def scan_fridge():

    print("========== 親鄉商店 ==========")
    print("開始巡冰箱")
    print()

    conn = sqlite3.connect("database/qinxiang_store.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, fridge_max, fridge_now
    FROM products
    ORDER BY display_order
    """)

    products = cursor.fetchall()

    total = len(products)

    for index, product in enumerate(products, start=1):

        id = product[0]
        name = product[1]
        max_stock = product[2]
        now_stock = product[3]

        print()
        print("========================")
        print(f"第 {index} / {total} 項")
        print("========================")

        print("商品：", name)
        print("冰箱容量：", max_stock)

        now_text = input(f"目前剩幾瓶（直接 Enter 保持 {now_stock}）：")

        if now_text == "":
            now = now_stock
        else:
            now = int(now_text)
        cursor.execute("""
        UPDATE products
        SET fridge_now = ?
        WHERE id = ?
        """, (now, id))

    conn.commit()

    print()
    print("========== 今日補貨清單 ==========")

    cursor.execute("""
    SELECT name, fridge_max, fridge_now
    FROM products
    ORDER BY id
    """)

    products = cursor.fetchall()

    count = 0

    for product in products:

        name = product[0]
        max_stock = product[1]
        now = product[2]

        if now is None:
            continue

        need = max_stock - now

        # 少於 3 瓶才補貨
        if need >= 3:

            print(f"{name}　補 {need} 瓶")
            count += 1

    print()
    print(f"共 {count} 項需要補貨")
    print()

    answer = input("補貨完成了嗎？(Y/N)：")

    if answer.upper() == "Y":

        cursor.execute("""
        UPDATE products
        SET fridge_now = fridge_max
        """)

        conn.commit()

        print()
        print("✅ 冰箱庫存已全部更新完成！")
    conn.close()