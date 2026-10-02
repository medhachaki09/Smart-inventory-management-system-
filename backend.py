import sqlite3
from datetime import datetime
import pandas as pd

# Database Setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Create Inventory Table
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (
                 inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 stock_level INTEGER NOT NULL,
                 restock_threshold INTEGER NOT NULL)''')
    
    # Create Orders Table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                 order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 customer_id INTEGER,
                 product_id INTEGER,
                 quantity_ordered INTEGER,
                 order_status TEXT,
                 order_date TEXT,
                 FOREIGN KEY (product_id) REFERENCES inventory(inventory_id),
                 FOREIGN KEY (customer_id) REFERENCES customers(customer_id))''')
    
    # Create Suppliers Table
    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                 supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 contact_details TEXT,
                 restocking_order_details TEXT)''')
    
    # Create Customers Table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                 customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 contact_details TEXT)''')
    
    # Create Transactions Table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 supplier_id INTEGER,
                 amount REAL,
                 transaction_date TEXT,
                 description TEXT,
                 FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id))''')
    
    # Create Admins Table
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
                 admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL)''')
    
    # Create Alerts Table
    c.execute('''CREATE TABLE IF NOT EXISTS restock_alerts (
                 alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 product_id INTEGER,
                 alerted BOOLEAN DEFAULT 0,
                 FOREIGN KEY (product_id) REFERENCES inventory(inventory_id))''')
    
    # Insert or update default admin
    c.execute("INSERT OR REPLACE INTO admins (admin_id, username, password) "
              "VALUES ((SELECT admin_id FROM admins WHERE username = ?), ?, ?)",
              ('attm', 'attm', 'd3n!3d'))
    
    conn.commit()
    conn.close()

# Admin Validation
def validate_admin(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE username = ? AND password = ?",
              (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Inventory Operations
def add_product(name, stock, threshold):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Check if product already exists
    c.execute("SELECT inventory_id, stock_level FROM inventory WHERE name = ?", (name,))
    existing_product = c.fetchone()
    
    if existing_product:
        # Update existing product's stock
        product_id, current_stock = existing_product
        new_stock = current_stock + int(stock)
        c.execute("UPDATE inventory SET stock_level = ?, restock_threshold = ? WHERE inventory_id = ?",
                  (new_stock, int(threshold), product_id))
    else:
        # Create new product
        c.execute("INSERT INTO inventory (name, stock_level, restock_threshold) VALUES (?, ?, ?)",
                  (name, int(stock), int(threshold)))
    
    conn.commit()
    conn.close()

def update_product(product_id, name, stock, threshold):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET name = ?, stock_level = ?, restock_threshold = ? WHERE inventory_id = ?",
              (name, int(stock), int(threshold), product_id))
    # Clear alert if stock is now above threshold
    c.execute("UPDATE restock_alerts SET alerted = 0 WHERE product_id = ? AND EXISTS (SELECT 1 FROM inventory WHERE inventory_id = ? AND stock_level > restock_threshold)",
              (product_id, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    # Check if product has associated orders
    c.execute("SELECT COUNT(*) FROM orders WHERE product_id = ?", (product_id,))
    order_count = c.fetchone()[0]
    
    if order_count > 0:
        conn.close()
        return False, "Cannot delete product with existing orders"
    
    # Delete from restock_alerts first
    c.execute("DELETE FROM restock_alerts WHERE product_id = ?", (product_id,))
    # Delete from inventory
    c.execute("DELETE FROM inventory WHERE inventory_id = ?", (product_id,))
    conn.commit()
    conn.close()
    return True, "Product deleted successfully"

def load_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    conn.close()
    return rows

def check_restock_alerts():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    # Get products needing restock that haven't been alerted
    c.execute("SELECT i.name, i.stock_level, i.restock_threshold, i.inventory_id "
              "FROM inventory i LEFT JOIN restock_alerts ra ON i.inventory_id = ra.product_id "
              "WHERE i.stock_level <= i.restock_threshold AND (ra.alerted = 0 OR ra.alerted IS NULL)")
    low_stock = c.fetchall()
    
    # Mark alerted products
    for product in low_stock:
        product_id = product[3]
        c.execute("INSERT OR REPLACE INTO restock_alerts (product_id, alerted) VALUES (?, 1)",
                  (product_id,))
    
    conn.commit()
    conn.close()
    return [(name, stock, threshold) for name, stock, threshold, _ in low_stock]

# Order Operations
def place_order(customer_id, product_id, quantity, status):
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Check if product and customer exist
    c.execute("SELECT stock_level FROM inventory WHERE inventory_id = ?", (product_id,))
    stock = c.fetchone()
    c.execute("SELECT customer_id FROM customers WHERE customer_id = ?", (customer_id,))
    customer = c.fetchone()
    
    if stock and customer and stock[0] >= int(quantity):
        c.execute("INSERT INTO orders (customer_id, product_id, quantity_ordered, order_status, order_date) VALUES (?, ?, ?, ?, ?)",
                  (customer_id, product_id, quantity, status, order_date))
        c.execute("UPDATE inventory SET stock_level = stock_level - ? WHERE inventory_id = ?",
                  (quantity, product_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def load_orders():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    rows = c.fetchall()
    conn.close()
    return rows

# Supplier Operations
def add_supplier(name, contact, restock):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO suppliers (name, contact_details, restocking_order_details) VALUES (?, ?, ?)",
              (name, contact, restock))
    conn.commit()
    conn.close()

def add_transaction(supplier_id, amount, desc):
    transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (supplier_id, amount, transaction_date, description) VALUES (?, ?, ?, ?)",
              (supplier_id, float(amount), transaction_date, desc))
    conn.commit()
    conn.close()

def load_suppliers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM suppliers")
    rows = c.fetchall()
    conn.close()
    return rows

# Customer Operations
def add_customer(name, contact):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, contact_details) VALUES (?, ?)",
              (name, contact))
    conn.commit()
    conn.close()

def load_customers():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    conn.close()
    return rows

# Report Operations
def generate_sales_report():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT o.order_id, c.name, i.name, o.quantity_ordered, o.order_status, o.order_date "
              "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
              "JOIN inventory i ON o.product_id = i.inventory_id")
    orders = c.fetchall()
    
    df = pd.read_sql_query("SELECT i.name, SUM(o.quantity_ordered) as total "
                           "FROM orders o JOIN inventory i ON o.product_id = i.inventory_id "
                           "GROUP BY i.name", conn)
    conn.close()
    return orders, df