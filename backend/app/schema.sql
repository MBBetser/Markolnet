-- Users Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_type ENUM('store_owner', 'customer') NOT NULL
);

-- Stores Table
CREATE TABLE Stores (
    store_id INT PRIMARY KEY AUTO_INCREMENT,
    store_name VARCHAR(100) NOT NULL,
    owner_id INT NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    FOREIGN KEY (owner_id) REFERENCES Users(user_id)
);

-- Products Table
CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    default_price DECIMAL(10, 2),
    image_url VARCHAR(255)
);

-- Store_Products Table
CREATE TABLE Store_Products (
    store_product_id INT PRIMARY KEY AUTO_INCREMENT,
    store_id INT NOT NULL,
    product_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT,
    FOREIGN KEY (store_id) REFERENCES Stores(store_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Orders Table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    store_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_method VARCHAR(50),
    delivery_address TEXT,
    order_items TEXT,
    FOREIGN KEY (customer_id) REFERENCES Users(user_id),
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
);


-- Indexes for better query performance
CREATE INDEX idx_store_owner ON Stores(owner_id);
CREATE INDEX idx_store_product ON Store_Products(store_id, product_id);
CREATE INDEX idx_order_customer ON Orders(customer_id);
CREATE INDEX idx_order_store ON Orders(store_id);
CREATE INDEX idx_order_item_order ON Order_Items(order_id);
CREATE INDEX idx_message_sender ON Messages(sender_id);
CREATE INDEX idx_message_receiver ON Messages(receiver_id);