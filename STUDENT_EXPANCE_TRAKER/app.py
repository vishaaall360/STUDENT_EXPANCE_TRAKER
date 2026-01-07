from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "expense.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            category TEXT
        )
    """)
    cur.execute("INSERT INTO expenses(title, amount, category) VALUES(?,?,?)",
                (title, amount, category))
    conn.commit()
    conn.close()

    return redirect("/expenses")

@app.route("/expenses")
def expenses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    data = cur.fetchall()

    total = sum([row[2] for row in data])
    conn.close()

    return render_template("expenses.html", expenses=data, total=total)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/expenses")

if __name__ == "__main__":
    app.run(debug=True)
