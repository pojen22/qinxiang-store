import sqlite3

def product_manage():

    conn = sqlite3.connect("database/qinxiang_store.db")
    cursor = conn.cursor()

    while True:

        print()
        print("====== 商品管理 ======")
        print("1. 新增商品")
        print("2. 修改商品")
        print("3. 刪除商品")
        print("4. 顯示全部商品")
        print("5. 查詢商品")
        print("6. 返回主選單")

        choice = input("請選擇：")

        if choice == "1":

            name = input("商品名稱：")
            barcode = input("條碼：")
            price = int(input("價格："))
            fridge_max = int(input("冰箱容量："))
            display_order = int(input("巡冰箱順序："))

            cursor.execute("""
            INSERT INTO products
            (name, barcode, price, fridge_max, fridge_now, display_order)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                barcode,
                price,
                fridge_max,
                fridge_max,
                display_order
            ))

            conn.commit()

            print("新增完成！")

        elif choice == "2":

            name = input("要修改的商品名稱：")

            cursor.execute("""
            SELECT *
            FROM products
            WHERE name = ?
            """, (name,))

            row = cursor.fetchone()

            if row is None:
                print("找不到商品")
                continue

            print()
            print("========== 目前商品資料 ==========")
            print("商品名稱：", row[1])
            print("條碼：", row[2])
            print("售價：", row[3], "元")
            print("冰箱容量：", row[4])
            print("目前剩餘：", row[5])
            print("巡冰箱順序：", row[7])
            print("補貨門檻：", row[6])
            print("=================================")
            print()

            new_name = input(f"新商品名稱（直接 Enter 保持 {row[1]}）：")
            barcode = input(f"新條碼（直接 Enter 保持 {row[2]}）：")
            price_text = input(f"新價格（直接 Enter 保持 {row[3]}）：")
            fridge_text = input(f"新冰箱容量（直接 Enter 保持 {row[4]}）：")
            order_text = input(f"巡冰箱順序（直接 Enter 保持 {row[7]}）：")
            threshold_text = input(f"補貨門檻（直接 Enter 保持 {row[6]}）：")

            if new_name == "":
                new_name = row[1]

            if barcode == "":
                barcode = row[2]

            if price_text == "":
                price = row[3]
            else:
                price = int(price_text)

            if fridge_text == "":
                fridge_max = row[4]
            else:
                fridge_max = int(fridge_text)

            if threshold_text == "":
                restock_threshold = row[6]
            else:
                restock_threshold = int(threshold_text)

            if order_text == "":
                display_order = row[7]
            else:
                display_order = int(order_text)
            cursor.execute("""
            UPDATE products
            SET
                name=?,
                barcode=?,
                price=?,
                fridge_max=?,
                display_order=?,
                restock_threshold=?
            WHERE name=?
            """, (
                new_name,
                barcode,
                price,
                fridge_max,
                display_order,
                restock_threshold,
                name
            ))

            conn.commit()

            print("修改完成！")
  
        elif choice == "3":

            name = input("要刪除的商品名稱：")

            cursor.execute("""
            SELECT name
            FROM products
            WHERE name=?
            """, (name,))

            row = cursor.fetchone()

            if row is None:

                print("找不到商品")

            else:

                answer = input(f"確定要刪除【{row[0]}】嗎？(Y/N)：")

                if answer.upper() == "Y":

                    cursor.execute("""
                    DELETE FROM products
                    WHERE name=?
                    """, (name,))

                    conn.commit()

                    print("✅ 商品已刪除")

                else:

                    print("已取消刪除")

        elif choice == "4":

            cursor.execute("""
            SELECT display_order,name,price,fridge_max,fridge_now
            FROM products
            ORDER BY display_order
            """)

            rows = cursor.fetchall()

            print()

            for row in rows:

                print(
                    row[0],
                    row[1],
                    row[2],
                    "元",
                    "容量",
                    row[3],
                    "目前",
                    row[4]
                )

        elif choice == "5":

             keyword = input("請輸入商品名稱：")

             cursor.execute("""
             SELECT display_order,
                    name,
                    price,
                    fridge_max,
                    fridge_now,
                    restock_threshold
             FROM products
             WHERE name LIKE ?
             ORDER BY display_order
             """, ("%" + keyword + "%",))

             rows = cursor.fetchall()

             if len(rows) == 0:

                 print("找不到商品")

             else:

                 print()

                 for row in rows:

                     print("==============================")
                     print("巡冰箱順序：", row[0])
                     print("商品名稱：", row[1])
                     print("售價：", row[2], "元")
                     print("冰箱容量：", row[3])
                     print("目前剩餘：", row[4])
                     print("補貨門檻：", row[5])
                     print("==============================")

        elif choice == "6":
             break

        else:
            print("輸入錯誤")

    conn.close()