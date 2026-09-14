-- ============================================================================
-- Swiggy Food Delivery & Business Intelligence Analytics
-- Script 01: Database & Relational Schema Definition
-- Database Engine: MySQL 8.0+
-- ============================================================================

-- Create and switch to the database
CREATE DATABASE IF NOT EXISTS swiggy_db;
USE swiggy_db;

-- ----------------------------------------------------------------------------
-- 1. Table: users
-- Stores customer profiles, locations, and Swiggy One subscription status
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS delivery_partners;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    city VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL,
    is_swiggy_one TINYINT(1) NOT NULL DEFAULT 0,
    INDEX idx_user_city (city),
    INDEX idx_user_membership (is_swiggy_one)
);

-- ----------------------------------------------------------------------------
-- 2. Table: restaurants
-- Stores actual scraped Swiggy restaurant details across major Indian cities
-- ----------------------------------------------------------------------------
CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    restaurant_name VARCHAR(150) NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL,
    rating_count INT DEFAULT 0,
    cost_for_two DECIMAL(10, 2) NOT NULL,
    swiggy_url VARCHAR(255),
    INDEX idx_rest_city (city),
    INDEX idx_rest_cuisine (cuisine),
    INDEX idx_rest_rating (rating)
);

-- ----------------------------------------------------------------------------
-- 3. Table: menu_items
-- Catalog of dishes, categories, pricing, and dietary classification
-- ----------------------------------------------------------------------------
CREATE TABLE menu_items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(150) NOT NULL,
    menu_category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    veg_or_non_veg VARCHAR(15) NOT NULL,
    INDEX idx_item_category (menu_category),
    INDEX idx_item_type (veg_or_non_veg)
);

-- ----------------------------------------------------------------------------
-- 4. Table: delivery_partners
-- Details of Swiggy delivery executives, vehicles, and ratings
-- ----------------------------------------------------------------------------
CREATE TABLE delivery_partners (
    partner_id INT PRIMARY KEY,
    partner_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(30) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL,
    INDEX idx_partner_city (city)
);

-- ----------------------------------------------------------------------------
-- 5. Table: orders
-- Header table capturing order timestamp, amounts, delivery duration, and status
-- ----------------------------------------------------------------------------
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    partner_id INT,
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    order_status VARCHAR(20) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    delivery_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    delivery_time_mins INT,
    payment_method VARCHAR(30) NOT NULL,
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_partner FOREIGN KEY (partner_id) REFERENCES delivery_partners(partner_id) ON DELETE SET NULL,
    INDEX idx_order_date (order_date),
    INDEX idx_order_status (order_status),
    INDEX idx_order_payment (payment_method)
);

-- ----------------------------------------------------------------------------
-- 6. Table: order_items
-- Line-item breakdown of dishes ordered, quantity, and line totals
-- ----------------------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    line_total DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_items_item FOREIGN KEY (item_id) REFERENCES menu_items(item_id) ON DELETE CASCADE,
    INDEX idx_order_item_name (item_name)
);
