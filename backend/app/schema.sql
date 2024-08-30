-- Drop existing tables
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Stores;
DROP TABLE IF EXISTS Store_Products;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Messages;

-- Create tables
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES Users(id)
);

CREATE TABLE IF NOT EXISTS Store_Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (store_id) REFERENCES Stores(id)
);

CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    store_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Users(id),
    FOREIGN KEY (store_id) REFERENCES Stores(id)
);

CREATE TABLE IF NOT EXISTS Order_Items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES Orders(id)
);

CREATE TABLE IF NOT EXISTS Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES Users(id),
    FOREIGN KEY (receiver_id) REFERENCES Users(id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_store_owner ON Stores(owner_id);
CREATE INDEX IF NOT EXISTS idx_store_product ON Store_Products(store_id, product_id);
CREATE INDEX IF NOT EXISTS idx_order_customer ON Orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_store ON Orders(store_id);
CREATE INDEX IF NOT EXISTS idx_order_item_order ON Order_Items(order_id);
CREATE INDEX IF NOT EXISTS idx_message_sender ON Messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_message_receiver ON Messages(receiver_id);