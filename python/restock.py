import sqlite3

def show_restock():

    conn = sqlite3.connect("database/qinxiang_store.db")
    cursor = conn.cursor()

    print("========== 今日補貨清單 ==========")

    cursor.execute("""
    SELECT name, fridge_max, fridge_now
    FROM products
    ORDER BY display_order
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

        if need >= 3:
            print(f"{name}　補 {need} 瓶")
            count += 1

    print()
    print(f"共 {count} 項需要補貨")

    conn.close()