-- root tolgaersoy
-- Insert 5 users (Users unchanged)
INSERT INTO users (first_name, last_name, email, password_hash, phone, balance) 
VALUES
('John', 'Doe', 'john.doe@example.com', 'hashedpassword1', '555-0001', 100.00),
('Jane', 'Smith', 'jane.smith@example.com', 'hashedpassword2', '555-0002', 200.00),
('Alice', 'Johnson', 'alice.johnson@example.com', 'hashedpassword3',  '555-0003', 150.00),
('Bob', 'Brown', 'bob.brown@example.com', 'hashedpassword4', '555-0004', 50.00),
('Charlie', 'Davis', 'charlie.davis@example.com', 'hashedpassword5', '555-0005', 250.00);

-- Insert 2 admins (Admins unchanged)
INSERT INTO admins (first_name, last_name, email, password_hash, phone)
VALUES
('Admin', 'One', 'admin1@example.com', 'adminpassword1', '555-1001'),
('Admin', 'Two', 'admin2@example.com', 'adminpassword2', '555-1002');

-- Insert 10 products (Products unchanged)
INSERT INTO products (name, info, barcode, price, stock_quantity)
VALUES
('Laptop', 'High-performance laptop', '1234567890123', 1200.00, 5),
('Phone', 'Latest smartphone model', '1234567890124', 800.00, 10),
('Tablet', '10-inch tablet', '1234567890125', 500.00, 7),
('Headphones', 'Noise-canceling headphones', '1234567890126', 150.00, 15),
('Smartwatch', 'Fitness tracking smartwatch', '1234567890127', 250.00, 20),
('Keyboard', 'Mechanical keyboard', '1234567890128', 100.00, 25),
('Mouse', 'Wireless mouse', '1234567890129', 50.00, 30),
('Monitor', '24-inch HD monitor', '1234567890130', 300.00, 12),
('Camera', 'Digital camera', '1234567890131', 600.00, 8),
('Speakers', 'Bluetooth speakers', '1234567890132', 120.00, 18);

-- Insert 8 topups (Updated topups with more variety)
INSERT INTO topups (user_id, amount)
VALUES
(1, 100.00),
(2, 150.00),
(3, 50.00),
(4, 75.00),
(5, 200.00),
(1, 50.00),
(3, 100.00),
(2, 75.00),
(5, 300.00),  -- Additional topup for variety
(4, 120.00);  -- Additional topup for variety

-- Insert 10 orders (Adding more varied orders)
INSERT INTO orders (user_id, total_price)
VALUES
(1, 1350.00),
(2, 1150.00),
(3, 650.00),
(4, 850.00),
(5, 1200.00),
(1, 750.00),
(2, 450.00),  -- Order 7: Lower priced
(3, 850.00),  -- Order 8: Medium priced
(4, 1500.00),  -- Order 9: High priced
(5, 1800.00);  -- Order 10: High priced

-- Insert 20 order_items (Adding variety and complexity to order_items)
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 1200.00), -- Order 1: Laptop
(1, 2, 1, 800.00), -- Order 1: Phone
(2, 3, 2, 500.00), -- Order 2: Tablet
(2, 4, 1, 150.00), -- Order 2: Headphones
(3, 5, 1, 250.00), -- Order 3: Smartwatch
(3, 6, 1, 100.00), -- Order 3: Keyboard
(4, 7, 2, 50.00), -- Order 4: Mouse (2 pieces)
(4, 8, 1, 300.00), -- Order 4: Monitor
(5, 9, 1, 600.00), -- Order 5: Camera
(5, 10, 1, 120.00), -- Order 5: Speakers
(6, 1, 1, 1200.00), -- Order 6: Laptop
(6, 2, 1, 800.00), -- Order 6: Phone
(7, 3, 1, 500.00), -- Order 7: Tablet (1 piece)
(7, 4, 1, 150.00), -- Order 7: Headphones (1 piece)
(8, 5, 2, 250.00), -- Order 8: Smartwatch (2 pieces)
(8, 6, 1, 100.00), -- Order 8: Keyboard
(9, 1, 2, 1200.00), -- Order 9: Laptop (2 pieces)
(9, 8, 1, 300.00), -- Order 9: Monitor
(10, 7, 3, 50.00), -- Order 10: Mouse (3 pieces)
(10, 9, 1, 600.00);  -- Order 10: Camera

