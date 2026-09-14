-- ============================================================================
-- Swiggy Food Delivery & Business Intelligence Analytics
-- Script 02: Data Ingestion into MySQL
-- Database: swiggy_db
-- ============================================================================

USE swiggy_db;

-- ----------------------------------------------------------------------------
-- METHOD 1: Using MySQL Workbench Table Data Import Wizard (RECOMMENDED FOR WINDOWS)
-- ----------------------------------------------------------------------------
-- Because MySQL on Windows frequently enforces strict `secure_file_priv` policies,
-- the fastest and most foolproof way in MySQL Workbench is:
--
-- 1. Open MySQL Workbench and connect to your local instance.
-- 2. In the left Schema panel, expand `swiggy_db` -> `Tables`.
-- 3. Right-click on each table and select "Table Data Import Wizard":
--    - Import `users.csv`            -> Into table `users`
--    - Import `restaurants.csv`      -> Into table `restaurants`
--    - Import `menu_items.csv`       -> Into table `menu_items`
--    - Import `delivery_partners.csv`-> Into table `delivery_partners`
--    - Import `orders.csv`           -> Into table `orders`
--    - Import `order_items.csv`      -> Into table `order_items`
-- 4. Follow the on-screen wizard (accept UTF-8 encoding) and click Next.
--
-- NOTE: Always import in the exact order listed above to satisfy Foreign Key constraints!

-- ----------------------------------------------------------------------------
-- METHOD 2: Direct SQL LOAD DATA INFILE (If secure_file_priv is configured)
-- ----------------------------------------------------------------------------
-- Replace `D:/Desktop/Projects/PowerBI_DA/data/` with your exact path.
-- Forward slashes `/` must be used in Windows file paths for MySQL.

/*
SET FOREIGN_KEY_CHECKS = 0;

-- 1. Users
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(user_id, name, gender, age, city, signup_date, is_swiggy_one);

-- 2. Restaurants
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/restaurants.csv'
INTO TABLE restaurants
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(restaurant_id, restaurant_name, city, cuisine, rating, rating_count, cost_for_two, swiggy_url);

-- 3. Menu Items
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/menu_items.csv'
INTO TABLE menu_items
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(item_id, item_name, menu_category, price, veg_or_non_veg);

-- 4. Delivery Partners
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/delivery_partners.csv'
INTO TABLE delivery_partners
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(partner_id, partner_name, city, vehicle_type, rating);

-- 5. Orders
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_id, user_id, restaurant_id, partner_id, order_date, order_time, order_status, total_amount, discount_amount, delivery_fee, @delivery_time_mins, payment_method)
SET delivery_time_mins = NULLIF(@delivery_time_mins, '');

-- 6. Order Items
LOAD DATA LOCAL INFILE 'D:/Desktop/Projects/PowerBI_DA/data/order_items.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_item_id, order_id, item_id, item_name, price, quantity, line_total);

SET FOREIGN_KEY_CHECKS = 1;
*/

-- ----------------------------------------------------------------------------
-- Verification: Check row counts after import
-- ----------------------------------------------------------------------------
SELECT 'users' AS table_name, COUNT(*) AS total_rows FROM users
UNION ALL
SELECT 'restaurants', COUNT(*) FROM restaurants
UNION ALL
SELECT 'menu_items', COUNT(*) FROM menu_items
UNION ALL
SELECT 'delivery_partners', COUNT(*) FROM delivery_partners
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;
