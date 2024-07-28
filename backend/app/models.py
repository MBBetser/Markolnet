from .db import get_connection


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

def add_store(store_name, onwer_id, address, phone_number, email):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        query = '''
                    INSERT INTO stores (store_name, owner_id, address, phone_number, email) 
                    VALUES (?, ?, ?, ?, ?);
                '''
        cursor.execute(query, (store_name, onwer_id, address, phone_number, email))
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