from .db import get_connection
from .myutils import arr2json

# Users
def add_user(username, password, email, phone_numer, user_type):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    INSERT INTO users (username, password, email, phone_number, user_type) 
                    VALUES (?, ?, ?, ?, ?);
                '''
        cursor.execute(query, (username, password, email, phone_numer, user_type))
        return cursor.lastrowid

def get_user_by_username(username):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM users WHERE username = ?;
                '''
        cursor.execute(query, (username,))
        return cursor.fetchone()
    
#Stores

def add_store(store_name, onwer_id, address, phone_number):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    INSERT INTO stores (store_name, owner_id, address, phone_number) 
                    VALUES (?, ?, ?, ?);
                '''
        cursor.execute(query, (store_name, onwer_id, address, phone_number))
        return cursor.lastrowid

def get_store_by_id(store_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM stores WHERE store_id = ?;
                '''
        cursor.execute(query, (store_id,))
        return cursor.fetchone()
    
def get_store_by_owner_id(owner_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM stores WHERE owner_id = ?;
                '''
        cursor.execute(query, (owner_id,))
        return cursor.fetchall()
    
# Products

def add_product(product_name, description, category, price, image_url):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    INSERT INTO products (product_name, description, category, price, image_url) 
                    VALUES (?, ?, ?, ?, ?);
                '''
        cursor.execute(query, (product_name, description, category, price, image_url))
        return cursor.lastrowid

def get_product_by_id(product_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM products WHERE product_id = ?;
                '''
        cursor.execute(query, (product_id,))
        return cursor.fetchone()
    
# store products

def add_store_product(store_id, product_id, quantity, price):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    INSERT INTO store_products (store_id, product_id, price, quantity) 
                    VALUES (?, ?, ?);
                '''
        cursor.execute(query, (store_id, product_id, quantity))
        return cursor.lastrowid

def get_store_product_by_id(store_product_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM store_products WHERE store_product_id = ?;
                '''
        cursor.execute(query, (store_product_id,))
        return cursor.fetchone()
    
# Orders

def add_order(user_id, customer_id, store_id, order_date, total_price, status, address, order_items):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        order_itemsjson = arr2json(order_items)
        query = '''
                    INSERT INTO orders (user_id, customer_id, store_id, order_date, total_price, status, address, order_items) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                '''
        cursor.execute(query, (user_id, customer_id, store_id, order_date, total_price, status, address, order_itemsjson))
        return cursor.lastrowid

def get_order_by_id(order_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM orders WHERE order_id = ?;
                '''
        cursor.execute(query, (order_id,))
        return cursor.fetchone()
    
def get_order_by_user_id(user_id):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    SELECT * FROM orders WHERE user_id = ?;
                '''
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
