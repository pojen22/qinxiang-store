from routes.home import register as home_register
from db import get_connection
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
home_register(app)


@app.route("/search", methods=["GET", "POST"])
def search():

    rows = []
    keyword = ""

    if request.method == "POST":

        keyword = request.form["keyword"].strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            name,
            price,
            fridge_max,
            fridge_now,
            restock_threshold,
            display_order
        FROM products
        WHERE name LIKE ?
           OR barcode = ?
        ORDER BY
            CASE WHEN display_order = 0 THEN 1 ELSE 0 END,
            display_order
        """, ("%" + keyword + "%", keyword))

        rows = cursor.fetchall()

        conn.close()

    return render_template(
        "search.html",
        rows=rows,
        keyword=keyword
    )


@app.route("/scan/<int:order>", methods=["GET", "POST"])
def scan(order):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        now = request.form["fridge_now"]

        cursor.execute("""
        UPDATE products
        SET fridge_now=?
        WHERE display_order=?
          AND display_order>0
        """, (now, order))

        conn.commit()

        cursor.execute("""
        SELECT display_order
        FROM products
        WHERE display_order>?
          AND display_order>0
        ORDER BY display_order
        LIMIT 1
        """, (order,))

        next_product = cursor.fetchone()

        if next_product is None:

            conn.close()

            return redirect("/restock")

        order = next_product[0]

    cursor.execute("""
    SELECT
        name,
        fridge_max,
        fridge_now,
        restock_threshold
    FROM products
    WHERE display_order=?
      AND display_order>0
    """, (order,))

    product = cursor.fetchone()

    conn.close()

    if product is None:

        return redirect("/restock")

    return render_template(
        "scan.html",
        product=product,
        order=order
    )


@app.route("/restock")
def restock():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        fridge_max-fridge_now
    FROM products
    WHERE display_order>0
      AND fridge_max-fridge_now>=restock_threshold
    ORDER BY display_order
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "restock.html",
        rows=rows
    )


@app.route("/products")
def products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        display_order,
        name,
        price,
        fridge_now
    FROM products
    ORDER BY
        CASE WHEN display_order=0 THEN 1 ELSE 0 END,
        display_order,
        name
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "products.html",
        rows=rows
    )


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        fridge_max = request.form["fridge_max"]
        fridge_now = request.form["fridge_now"]
        display_order = request.form["display_order"]
        restock_threshold = request.form["restock_threshold"]

        # 一般商品：巡冰箱順序為 0
        if int(display_order) == 0:

            fridge_max = 0
            fridge_now = 0
            restock_threshold = 0

        cursor.execute("""
        UPDATE products
        SET
            name=?,
            price=?,
            fridge_max=?,
            fridge_now=?,
            display_order=?,
            restock_threshold=?
        WHERE id=?
        """, (
            name,
            price,
            fridge_max,
            fridge_now,
            display_order,
            restock_threshold,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/products")

    cursor.execute("""
    SELECT
        id,
        name,
        price,
        fridge_max,
        fridge_now,
        display_order,
        restock_threshold
    FROM products
    WHERE id=?
    """, (id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return redirect("/products")

    return render_template(
        "edit.html",
        row=row
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        barcode = request.form["barcode"]
        price = request.form["price"]
        fridge_max = request.form["fridge_max"]
        fridge_now = request.form["fridge_now"]
        display_order = request.form["display_order"]
        restock_threshold = request.form["restock_threshold"]

        # 一般商品：巡冰箱順序輸入 0
        if int(display_order) == 0:

            fridge_max = 0
            fridge_now = 0
            restock_threshold = 0

        cursor.execute("""
        INSERT INTO products(
            name,
            barcode,
            price,
            fridge_max,
            fridge_now,
            display_order,
            restock_threshold
        )
        VALUES(?,?,?,?,?,?,?)
        """, (
            name,
            barcode,
            price,
            fridge_max,
            fridge_now,
            display_order,
            restock_threshold
        ))

        conn.commit()
        conn.close()

        return redirect("/products")

    conn.close()

    return render_template("add_product.html")


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/products")


if __name__ == "__main__":
    app.run(debug=True)