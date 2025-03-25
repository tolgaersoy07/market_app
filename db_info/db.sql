-- Yeni veritabanı oluşturuluyor
CREATE DATABASE market_db;

-- Oluşturduğumuz veritabanına geçiş yapıyoruz
USE market_db;



CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) CHECK (LENGTH(first_name) > 0),
    last_name VARCHAR(30) CHECK (LENGTH(last_name) > 0),
    email VARCHAR(50) UNIQUE CHECK (LENGTH(email) > 0),
    password_hash VARCHAR(150) CHECK (LENGTH(password_hash) > 0),
    phone VARCHAR(15) UNIQUE CHECK (LENGTH(phone) > 0),
    balance DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) CHECK (LENGTH(first_name) > 0),
    last_name VARCHAR(30) CHECK (LENGTH(last_name) > 0),
    email VARCHAR(50) UNIQUE CHECK (LENGTH(email) > 0),
    password_hash VARCHAR(150) CHECK (LENGTH(password_hash) > 0),
    phone VARCHAR(15) UNIQUE CHECK (LENGTH(phone) > 0)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) CHECK (LENGTH(name) > 0),
    info VARCHAR(200) CHECK (LENGTH(info) > 0),
    barcode VARCHAR(13) UNIQUE CHECK (LENGTH(barcode) = 13),
    price DECIMAL(10,2) CHECK (price > 0),
    stock_quantity INT DEFAULT 0
);

CREATE TABLE topups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL CHECK (user_id > 0),
    amount DECIMAL(10,2) CHECK (amount > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL CHECK (user_id > 0),
    total_price DECIMAL(10,2) CHECK (total_price > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL CHECK (order_id > 0),
    product_id INT NOT NULL CHECK (product_id > 0),
    quantity INT CHECK (quantity > 0),
    unit_price DECIMAL(10,2) CHECK (unit_price > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,               -- ID, otomatik artan birincil anahtar
    refresh_token VARCHAR(1024) NOT NULL,                  -- Refresh token (64 karakterli, şifrelenmiş)
    email VARCHAR(255) NOT NULL,                      -- Kullanıcı e-posta adresi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    -- Token oluşturulma zamanı (otomatik olarak oluşturulacak)
);

CREATE TABLE carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,  -- Kullanıcıyı tanımlayan ID
    expires_at DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP + INTERVAL 60 MINUTE),  -- Sepetin geçerlilik tarihi 60 dakika sonra
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


