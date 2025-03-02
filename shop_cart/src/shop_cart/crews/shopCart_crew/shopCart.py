from crewai import Agent, Crew
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                      (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, stock INTEGER, reviews TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees 
                      (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary REAL)''')
    conn.commit()
    conn.close()

# Department Classes
class Inventory:
    def add_product(self, name, category, price, stock):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock, reviews) VALUES (?, ?, ?, ?, '')", 
                       (name, category, price, stock))
        conn.commit()
        conn.close()

class Sales:
    def process_sale(self, product_id, quantity):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM products WHERE id=?", (product_id,))
        stock = cursor.fetchone()[0]
        if stock >= quantity:
            cursor.execute("UPDATE products SET stock=stock-? WHERE id=?", (quantity, product_id))
            conn.commit()
        conn.close()

class Accounting:
    def generate_report(self):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        return products

class HR:
    def add_employee(self, name, department, salary):
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", (name, department, salary))
        conn.commit()
        conn.close()

# Product Categories
class Electronics:
    pass

class Clothing:
    pass

class Groceries:
    pass

# CrewAI Agents
inventory_agent = Agent(role="Inventory Manager", goal="Manage stock and ensure product availability.", backstory="Handles product stock levels.")
sales_agent = Agent(role="Sales Manager", goal="Process transactions and track sales.", backstory="Handles customer orders.")
accounting_agent = Agent(role="Finance Manager", goal="Generate financial reports.", backstory="Manages revenue and expenses.")
hr_agent = Agent(role="HR Manager", goal="Manage employee records.", backstory="Oversees hiring and payroll.")

crew = Crew(agents=[inventory_agent, sales_agent, accounting_agent, hr_agent])

# Web Interface (Flask)
app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route('/add_review', methods=['POST'])
def add_review():
    product_id = request.form['product_id']
    review = request.form['review']
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET reviews=reviews || ? WHERE id=?", (review + "\n", product_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
