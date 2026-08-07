import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():

    rows = []
    keyword = ""

    if request.method == "POST":

        keyword = request.form["keyword"].strip()

        conn = sqlite3.connect("../database/qinxiang_store.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            name,
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

        conn.close()

    return render_template(
        "search.html",
        rows=rows,
        keyword=keyword
    )


@app.route("/scan/<int:order>", methods=["GET", "POST"])
def scan(order):

    conn = sqlite3.connect("../database/qinxiang_store.db")
    cursor = conn.cursor()

    if request.method == "POST":

        now = request.form["fridge_now"]

        cursor.execute("""
        UPDATE products
        SET fridge_now=?
        WHERE display_order=?
        """, (now, order))

        conn.commit()

        order += 1

        cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE display_order=?
        """, (order,))

        if cursor.fetchone()[0] == 0:

            conn.close()

            return redirect("/restock")

    cursor.execute("""
    SELECT
        name,
        fridge_max,
        fridge_now,
        restock_threshold
    FROM products
    WHERE display_order=?
    """, (order,))

    product = cursor.fetchone()

    conn.close()

    return render_template(
        "scan.html",
        product=product,
        order=order
    )


@app.route("/restock")
def restock():

    conn = sqlite3.connect("../database/qinxiang_store.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        fridge_max-fridge_now
    FROM products
    WHERE fridge_max-fridge_now>=restock_threshold
    ORDER BY display_order
    """)

    rows = cursor.fetchall()

    conn.close()

    return render_template(
        "restock.html",
        rows=rows
    )


if __name__ == "__main__":
    app.run(debug=True)