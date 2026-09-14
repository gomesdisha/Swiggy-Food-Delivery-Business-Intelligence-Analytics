# Swiggy Business Intelligence — Data Dictionary

This document provides a detailed breakdown of all 6 relational tables used in the Swiggy Data Analytics & Business Intelligence project.

---

## 1. Table: `users`
Captures registered Swiggy customer profiles, geographic location, and subscription status.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | `INT` | Primary Key | Unique 4-digit identifier for each customer | `1001`, `1002` |
| `name` | `VARCHAR(100)` | - | Full name of the customer | `"Rahul Sharma"`, `"Priya Patel"` |
| `gender` | `VARCHAR(10)` | - | Gender of the customer (`Male` / `Female`) | `"Female"`, `"Male"` |
| `age` | `INT` | - | Customer age (19 to 52) | `26`, `34` |
| `city` | `VARCHAR(50)` | - | Primary delivery city of the user | `"Bangalore"`, `"Mumbai"`, `"Delhi"` |
| `signup_date`| `DATE` | - | Date of user account creation (ISO format) | `2023-04-15`, `2024-02-10` |
| `is_swiggy_one`| `TINYINT(1)` | - | Swiggy One membership flag (`1` = Member, `0` = Regular) | `1`, `0` |

---

## 2. Table: `restaurants`
Contains real scraped Swiggy restaurant metadata across 7 major Indian metro cities.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `restaurant_id` | `INT` | Primary Key | Unique identifier for each restaurant | `101`, `102` |
| `restaurant_name` | `VARCHAR(150)` | - | Real trading name of the restaurant on Swiggy | `"Meghana Foods"`, `"Tandoor Hut"` |
| `city` | `VARCHAR(50)` | - | City where the restaurant operates | `"Bangalore"`, `"Hyderabad"`, `"Pune"` |
| `cuisine` | `VARCHAR(100)` | - | Primary cuisine specialty | `"Biryani"`, `"North Indian"`, `"Cafe"` |
| `rating` | `DECIMAL(3,1)` | - | Customer average rating on Swiggy (out of 5.0) | `4.6`, `4.2` |
| `rating_count` | `INT` | - | Total number of customer reviews logged | `1200`, `5000` |
| `cost_for_two` | `DECIMAL(10,2)`| - | Approximate dining/ordering cost for two people (₹) | `600.00`, `350.00` |
| `swiggy_url` | `VARCHAR(255)` | - | Official live Swiggy listing URL | `https://www.swiggy.com/restaurants/...` |

---

## 3. Table: `menu_items`
Catalog of authentic scraped dishes, categories, and pricing.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `item_id` | `INT` | Primary Key | Unique identifier for each menu item | `1`, `2` |
| `item_name` | `VARCHAR(150)` | - | Name of the dish/item as shown on Swiggy menu | `"Chicken Dum Biryani"`, `"Masala Dosa"` |
| `menu_category` | `VARCHAR(100)` | - | Category within the menu | `"Main Course"`, `"Starters"`, `"Desserts"` |
| `price` | `DECIMAL(10,2)`| - | Menu price per unit in Indian Rupees (₹) | `320.00`, `120.00` |
| `veg_or_non_veg`| `VARCHAR(15)` | - | Dietary classification (`Veg` / `Non-veg`) | `"Veg"`, `"Non-veg"` |

---

## 4. Table: `delivery_partners`
Details of delivery fleet executives, operational cities, and vehicle types.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `partner_id` | `INT` | Primary Key | Unique identifier for delivery partner | `501`, `502` |
| `partner_name` | `VARCHAR(100)` | - | Name of the delivery executive | `"Vikram Rao"`, `"Suresh Nair"` |
| `city` | `VARCHAR(50)` | - | City where the rider is stationed | `"Bangalore"`, `"Mumbai"`, `"Delhi"` |
| `vehicle_type` | `VARCHAR(30)` | - | Transport mode (`Motorcycle`, `Scooter`, `Electric Vehicle (EV)`) | `"Electric Vehicle (EV)"`, `"Motorcycle"` |
| `rating` | `DECIMAL(3,1)` | - | Average customer delivery rating (out of 5.0) | `4.8`, `4.5` |

---

## 5. Table: `orders`
Header transaction table recording each order placed on Swiggy in 2024.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | `INT` | Primary Key | Unique 6-digit transaction ID | `200001`, `200002` |
| `user_id` | `INT` | Foreign Key | References `users.user_id` | `1042` |
| `restaurant_id` | `INT` | Foreign Key | References `restaurants.restaurant_id` | `112` |
| `partner_id` | `INT` | Foreign Key | References `delivery_partners.partner_id` | `518` |
| `order_date` | `DATE` | - | Date order was placed (2024-01-01 to 2024-12-31) | `2024-05-18` |
| `order_time` | `TIME` | - | Time order was placed (24-hour format) | `20:42:00` |
| `order_status` | `VARCHAR(20)` | - | Fulfillment status (`Delivered` / `Cancelled`) | `"Delivered"`, `"Cancelled"` |
| `total_amount` | `DECIMAL(10,2)`| - | Final invoice total paid by customer (₹) | `485.00` |
| `discount_amount`| `DECIMAL(10,2)`| - | Discounts applied (Swiggy One / coupon promo) | `75.00`, `0.00` |
| `delivery_fee` | `DECIMAL(10,2)`| - | Delivery charge (₹0 for Swiggy One on orders ≥ ₹149) | `0.00`, `35.00` |
| `delivery_time_mins`| `INT` | - | Total minutes from order placement to delivery | `32`, `44` |
| `payment_method`| `VARCHAR(30)` | - | Payment gateway channel used | `"UPI"`, `"Credit Card"`, `"COD"` |

---

## 6. Table: `order_items`
Granular line-item breakdown of every dish ordered within each order.

| Column Name | Data Type | Key Type | Description | Sample Values |
| :--- | :--- | :--- | :--- | :--- |
| `order_item_id` | `INT` | Primary Key | Unique line-item identifier | `1`, `2` |
| `order_id` | `INT` | Foreign Key | References `orders.order_id` | `200001` |
| `item_id` | `INT` | Foreign Key | References `menu_items.item_id` | `45` |
| `item_name` | `VARCHAR(150)` | - | Name of the ordered item | `"Paneer Butter Masala"` |
| `price` | `DECIMAL(10,2)`| - | Unit price of the dish at time of ordering (₹) | `260.00` |
| `quantity` | `INT` | - | Quantity of units ordered | `1`, `2` |
| `line_total` | `DECIMAL(10,2)`| - | Calculated line total (`price * quantity`) (₹) | `520.00` |
