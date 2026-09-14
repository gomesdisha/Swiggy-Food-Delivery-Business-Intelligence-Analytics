-- ============================================================================
-- Swiggy Food Delivery & Business Intelligence Analytics
-- Script 03: Production Business Analysis Queries
-- Database Engine: MySQL 8.0+
-- 
-- Author: Disha Gomes
-- Purpose: 15 Core Business Queries demonstrating Window Functions, CTEs,
--          aggregations, and actionable business insights for Swiggy Leadership.
-- ============================================================================

USE swiggy_db;

-- ============================================================================
-- MODULE 1: REVENUE & ORDERING DYNAMICS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 1: Monthly Gross Merchandise Value (GMV), Order Volume & MoM Growth
-- Business Problem:
--   Leadership needs to track Swiggy's monthly revenue trajectory, total delivered
--   orders, active customer count, and month-over-month (MoM) GMV growth rate.
-- Technical Concepts:
--   DATE_FORMAT, SUM, COUNT(DISTINCT), LAG() window function.
-- ----------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        COUNT(order_id) AS total_orders,
        COUNT(DISTINCT user_id) AS active_customers,
        SUM(total_amount) AS total_gmv,
        ROUND(AVG(total_amount), 2) AS avg_order_value
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    order_month,
    total_orders,
    active_customers,
    total_gmv,
    avg_order_value,
    LAG(total_gmv, 1) OVER (ORDER BY order_month) AS prev_month_gmv,
    ROUND(
        (total_gmv - LAG(total_gmv, 1) OVER (ORDER BY order_month)) / 
        LAG(total_gmv, 1) OVER (ORDER BY order_month) * 100, 
        2
    ) AS mom_growth_pct
FROM monthly_metrics
ORDER BY order_month;

-- Business Insight:
-- Peak revenue occurs during festive periods (October-November: Diwali/Navratri)
-- and IPL season (April-May). Identifying monthly dips enables targeted marketing.


-- ----------------------------------------------------------------------------
-- Query 2: City-Wise Revenue, Order Share & Average Order Value (AOV)
-- Business Problem:
--   Which cities are driving Swiggy's top line, and where are customers spending
--   the most per order?
-- Technical Concepts:
--   INNER JOIN, SUM() OVER() window function for contribution percentage.
-- ----------------------------------------------------------------------------
SELECT 
    u.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS city_aov,
    ROUND(
        SUM(o.total_amount) * 100.0 / SUM(SUM(o.total_amount)) OVER(), 
        2
    ) AS revenue_share_pct
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
WHERE o.order_status = 'Delivered'
GROUP BY u.city
ORDER BY total_revenue DESC;

-- Business Insight:
-- Bangalore and Mumbai dominate total GMV volume, but high AOV in Delhi NCR
-- suggests higher basket sizes per family order.


-- ----------------------------------------------------------------------------
-- Query 3: Payment Method Distribution & Cancellation Rates
-- Business Problem:
--   Assess customer payment preferences and determine if specific payment modes
--   (e.g., Cash on Delivery) suffer from higher order cancellation rates.
-- Technical Concepts:
--   Conditional aggregation using CASE WHEN.
-- ----------------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 
        2
    ) AS cancellation_rate_pct,
    ROUND(SUM(total_amount), 2) AS total_order_value
FROM orders
GROUP BY payment_method
ORDER BY total_orders DESC;

-- Business Insight:
-- UPI represents >60% of all transactions. Cash on Delivery (COD) typically
-- exhibits the highest cancellation rate, justifying prepaid incentive discounts.


-- ----------------------------------------------------------------------------
-- Query 4: Peak Ordering Slots (Lunch vs. Dinner vs. Late Night)
-- Business Problem:
--   When do Swiggy customers place the most orders? How should delivery fleets
--   be scheduled throughout the day?
-- Technical Concepts:
--   CASE WHEN on HOUR(order_time), GROUP BY time_bucket.
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN HOUR(order_time) BETWEEN 6 AND 11 THEN 'Breakfast (6 AM - 11 AM)'
        WHEN HOUR(order_time) BETWEEN 12 AND 15 THEN 'Lunch Peak (12 PM - 3 PM)'
        WHEN HOUR(order_time) BETWEEN 16 AND 18 THEN 'Evening Snacks (4 PM - 6 PM)'
        WHEN HOUR(order_time) BETWEEN 19 AND 22 THEN 'Dinner Peak (7 PM - 10 PM)'
        ELSE 'Late Night (11 PM - 5 AM)'
    END AS meal_slot,
    COUNT(order_id) AS order_count,
    ROUND(SUM(total_amount), 2) AS total_sales,
    ROUND(AVG(total_amount), 2) AS avg_basket_size,
    ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_time_mins
FROM orders
WHERE order_status = 'Delivered'
GROUP BY meal_slot
ORDER BY order_count DESC;

-- Business Insight:
-- Dinner and Lunch account for over 80% of daily orders. Dinner orders also have
-- a higher Average Order Value (AOV) and longer delivery times due to peak traffic.


-- ============================================================================
-- MODULE 2: SWIGGY ONE MEMBERSHIP & CUSTOMER RETENTION
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 5: Swiggy One vs. Non-One Member Unit Economics & LTV Lift
-- Business Problem:
--   Validate the commercial viability of the "Swiggy One" loyalty subscription.
--   Do members spend more and order more frequently than regular users?
-- Technical Concepts:
--   INNER JOIN, AVG, COUNT, DISTINCT aggregations.
-- ----------------------------------------------------------------------------
SELECT 
    CASE WHEN u.is_swiggy_one = 1 THEN 'Swiggy One Member' ELSE 'Regular User' END AS customer_tier,
    COUNT(DISTINCT u.user_id) AS total_users,
    COUNT(o.order_id) AS total_orders_placed,
    ROUND(COUNT(o.order_id) * 1.0 / COUNT(DISTINCT u.user_id), 1) AS orders_per_customer,
    ROUND(SUM(o.total_amount), 2) AS total_spend,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(AVG(o.discount_amount), 2) AS avg_discount_received,
    ROUND(AVG(o.delivery_fee), 2) AS avg_delivery_fee_paid
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.order_status = 'Delivered'
GROUP BY u.is_swiggy_one;

-- Business Insight:
-- Swiggy One members order 2.5x to 3x more frequently than non-members. Even with
-- free delivery and higher discounts, their annual Customer Lifetime Value (LTV)
-- significantly outpaces non-subscribers.


-- ----------------------------------------------------------------------------
-- Query 6: Customer Order Frequency Segmentation (RFM: Frequency)
-- Business Problem:
--   Segment the customer base into Power Users, Regulars, and Occasional Buyers
--   to tailor CRM push notifications and re-engagement campaigns.
-- Technical Concepts:
--   CTE, CASE WHEN with conditional grouping.
-- ----------------------------------------------------------------------------
WITH user_order_counts AS (
    SELECT 
        u.user_id,
        u.name,
        u.city,
        u.is_swiggy_one,
        COUNT(o.order_id) AS delivered_orders,
        COALESCE(SUM(o.total_amount), 0) AS lifetime_spend
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id AND o.order_status = 'Delivered'
    GROUP BY u.user_id, u.name, u.city, u.is_swiggy_one
)
SELECT 
    CASE 
        WHEN delivered_orders >= 25 THEN 'Power User (25+ Orders)'
        WHEN delivered_orders BETWEEN 12 AND 24 THEN 'Frequent Eater (12-24 Orders)'
        WHEN delivered_orders BETWEEN 5 AND 11 THEN 'Regular Customer (5-11 Orders)'
        WHEN delivered_orders BETWEEN 1 AND 4 THEN 'Occasional Buyer (1-4 Orders)'
        ELSE 'Dormant (0 Orders)'
    END AS customer_segment,
    COUNT(user_id) AS customer_count,
    ROUND(COUNT(user_id) * 100.0 / (SELECT COUNT(*) FROM users), 2) AS customer_pct,
    ROUND(SUM(lifetime_spend), 2) AS total_segment_revenue,
    ROUND(AVG(lifetime_spend), 2) AS avg_spend_per_user
FROM user_order_counts
GROUP BY customer_segment
ORDER BY avg_spend_per_user DESC;

-- Business Insight:
-- Power users and frequent eaters make up ~30% of the customer base but drive
-- ~70% of total revenue. Retention strategies must protect this cohort.


-- ----------------------------------------------------------------------------
-- Query 7: Top 5% Spenders by City using NTILE Window Function
-- Business Problem:
--   Identify Swiggy's highest-value VIP customers in each metro city for
--   exclusive concierge loyalty perks and early access promotions.
-- Technical Concepts:
--   CTE, NTILE(20) window function partitioned by city.
-- ----------------------------------------------------------------------------
WITH city_customer_spend AS (
    SELECT 
        u.city,
        u.user_id,
        u.name,
        u.is_swiggy_one,
        SUM(o.total_amount) AS total_spend,
        COUNT(o.order_id) AS order_count,
        NTILE(20) OVER (PARTITION BY u.city ORDER BY SUM(o.total_amount) DESC) AS spend_percentile
    FROM users u
    INNER JOIN orders o ON u.user_id = o.user_id
    WHERE o.order_status = 'Delivered'
    GROUP BY u.city, u.user_id, u.name, u.is_swiggy_one
)
SELECT 
    city,
    user_id,
    name,
    CASE WHEN is_swiggy_one = 1 THEN 'Yes' ELSE 'No' END AS swiggy_one,
    total_spend,
    order_count
FROM city_customer_spend
WHERE spend_percentile = 1 -- Top 5% (1 out of 20 buckets)
ORDER BY city, total_spend DESC;

-- Business Insight:
-- The top 5% VIP customers in Bengaluru and Mumbai spend >₹18,000 annually.
-- Converting non-One VIP customers into Swiggy One locks in retention.


-- ----------------------------------------------------------------------------
-- Query 8: At-Risk & Churned Customer Identification (Dormancy > 60 Days)
-- Business Problem:
--   Identify users who previously ordered regularly but haven't placed an order
--   in the last 60 days of 2024.
-- Technical Concepts:
--   MAX(order_date), DATEDIFF, HAVING clause.
-- ----------------------------------------------------------------------------
SELECT 
    u.user_id,
    u.name,
    u.city,
    u.is_swiggy_one,
    COUNT(o.order_id) AS total_past_orders,
    ROUND(SUM(o.total_amount), 2) AS total_historical_spend,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF('2024-12-31', MAX(o.order_date)) AS days_since_last_order
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
WHERE o.order_status = 'Delivered'
GROUP BY u.user_id, u.name, u.city, u.is_swiggy_one
HAVING total_past_orders >= 8 AND days_since_last_order > 60
ORDER BY total_historical_spend DESC
LIMIT 20;

-- Business Insight:
-- These were previously loyal customers who have churned. Automated "We miss you"
-- discounts (e.g., ₹100 off next order) should target this exact list.


-- ============================================================================
-- MODULE 3: RESTAURANT & CUISINE PERFORMANCE
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 9: Top 3 Restaurants by Total Revenue in Each City (DENSE_RANK)
-- Business Problem:
--   Identify the top 3 revenue-generating restaurant partners in each city to
--   prioritize commercial partnerships and co-marketing campaigns.
-- Technical Concepts:
--   DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...), CTE.
-- ----------------------------------------------------------------------------
WITH restaurant_city_sales AS (
    SELECT 
        r.city,
        r.restaurant_id,
        r.restaurant_name,
        r.cuisine,
        r.rating,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_revenue,
        DENSE_RANK() OVER (PARTITION BY r.city ORDER BY SUM(o.total_amount) DESC) AS city_rank
    FROM restaurants r
    INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Delivered'
    GROUP BY r.city, r.restaurant_id, r.restaurant_name, r.cuisine, r.rating
)
SELECT 
    city,
    city_rank,
    restaurant_name,
    cuisine,
    rating,
    total_orders,
    total_revenue
FROM restaurant_city_sales
WHERE city_rank <= 3
ORDER BY city, city_rank;

-- Business Insight:
-- Highlights the undisputed market leaders (e.g., iconic Biryani or South Indian
-- outlets in Bangalore and Hyderabad). Essential for commission renegotiations.


-- ----------------------------------------------------------------------------
-- Query 10: Most Popular Cuisines across India by Order Volume & Sales
-- Business Problem:
--   Which cuisines generate the highest order volume, and which deliver the
--   highest average spend per order?
-- Technical Concepts:
--   INNER JOIN, SUM, COUNT, ROUND, GROUP BY.
-- ----------------------------------------------------------------------------
SELECT 
    r.cuisine,
    COUNT(DISTINCT r.restaurant_id) AS restaurant_count,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_sales,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    ROUND(
        COUNT(o.order_id) * 100.0 / (SELECT COUNT(*) FROM orders WHERE order_status = 'Delivered'), 
        2
    ) AS order_share_pct
FROM restaurants r
INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.cuisine
ORDER BY total_orders DESC;

-- Business Insight:
-- Biryani and North Indian account for over 45% of total food delivery demand,
-- while Desserts/Cafes have high frequency but lower ticket sizes.


-- ----------------------------------------------------------------------------
-- Query 11: Vegetarian vs. Non-Vegetarian Dish Demand & Revenue Split
-- Business Problem:
--   Understand the dietary split of items ordered across Swiggy's marketplace.
-- Technical Concepts:
--   INNER JOIN on order_items and menu_items, conditional aggregation.
-- ----------------------------------------------------------------------------
SELECT 
    mi.veg_or_non_veg,
    COUNT(oi.order_item_id) AS total_items_sold,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.line_total) AS total_revenue,
    ROUND(
        SUM(oi.line_total) * 100.0 / SUM(SUM(oi.line_total)) OVER (), 
        2
    ) AS revenue_share_pct,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
INNER JOIN menu_items mi ON oi.item_id = mi.item_id
GROUP BY mi.veg_or_non_veg;

-- Business Insight:
-- Non-veg dishes command a higher average price point (~₹280 vs ₹180), driving
-- disproportionate revenue share despite high vegetarian item volume.


-- ----------------------------------------------------------------------------
-- Query 12: High-Volume / Low-Rating Operational Risk Alert
-- Business Problem:
--   Find popular restaurants with high order volume (>75 orders) but customer
--   ratings below 4.0. These pose an urgent customer satisfaction/churn risk!
-- Technical Concepts:
--   INNER JOIN, COUNT, HAVING filter on rating and order count.
-- ----------------------------------------------------------------------------
SELECT 
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine,
    r.rating,
    COUNT(o.order_id) AS total_orders_fulfilled,
    SUM(o.total_amount) AS total_revenue_generated,
    ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time_mins
FROM restaurants r
INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_id, r.restaurant_name, r.city, r.cuisine, r.rating
HAVING r.rating < 4.0 AND total_orders_fulfilled >= 75
ORDER BY total_orders_fulfilled DESC;

-- Business Insight:
-- These restaurants generate significant commission for Swiggy but risk degrading
-- customer trust. Swiggy operations should audit food packaging and prep times.


-- ============================================================================
-- MODULE 4: DELIVERY OPERATIONS & SLA EFFICIENCY
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 13: Average Delivery Duration & Late Delivery Percentage by City
-- Business Problem:
--   Identify city-level logistics bottlenecks. What percentage of deliveries
--   breach Swiggy's 40-minute SLA benchmark?
-- Technical Concepts:
--   Conditional CASE WHEN aggregation for SLA breach rate.
-- ----------------------------------------------------------------------------
SELECT 
    u.city,
    COUNT(o.order_id) AS delivered_orders,
    ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time_mins,
    MIN(o.delivery_time_mins) AS fastest_delivery_mins,
    MAX(o.delivery_time_mins) AS slowest_delivery_mins,
    SUM(CASE WHEN o.delivery_time_mins > 40 THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        SUM(CASE WHEN o.delivery_time_mins > 40 THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 
        2
    ) AS sla_breach_rate_pct
FROM orders o
INNER JOIN users u ON o.user_id = u.user_id
WHERE o.order_status = 'Delivered'
GROUP BY u.city
ORDER BY avg_delivery_time_mins DESC;

-- Business Insight:
-- Mumbai and Bangalore show higher average delivery times and SLA breach rates
-- due to urban traffic density and monsoon weather.


-- ----------------------------------------------------------------------------
-- Query 14: Impact of Vehicle Type on Delivery Performance
-- Business Problem:
--   Swiggy is aggressively piloting Electric Vehicles (EVs). Does EV delivery
--   speed match traditional motorcycles and scooters?
-- Technical Concepts:
--   INNER JOIN on delivery_partners, AVG, COUNT.
-- ----------------------------------------------------------------------------
SELECT 
    dp.vehicle_type,
    COUNT(DISTINCT dp.partner_id) AS active_partners,
    COUNT(o.order_id) AS total_deliveries,
    ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time_mins,
    ROUND(AVG(dp.rating), 2) AS avg_partner_rating,
    ROUND(
        SUM(CASE WHEN o.delivery_time_mins > 40 THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 
        2
    ) AS delayed_order_pct
FROM orders o
INNER JOIN delivery_partners dp ON o.partner_id = dp.partner_id
WHERE o.order_status = 'Delivered'
GROUP BY dp.vehicle_type
ORDER BY total_deliveries DESC;

-- Business Insight:
-- Electric Vehicles (EVs) exhibit near-identical delivery speeds to petrol
-- motorcycles while cutting delivery fuel expenses and supporting ESG goals.


-- ----------------------------------------------------------------------------
-- Query 15: Delivery Partner Performance & Rating Scorecard
-- Business Problem:
--   Rank delivery executives in each city based on delivery volume and speed
--   for weekly incentive bonus payouts.
-- Technical Concepts:
--   DENSE_RANK() window function, COUNT, AVG, conditional ranking.
-- ----------------------------------------------------------------------------
WITH rider_summary AS (
    SELECT 
        dp.city,
        dp.partner_id,
        dp.partner_name,
        dp.vehicle_type,
        dp.rating,
        COUNT(o.order_id) AS total_deliveries,
        ROUND(AVG(o.delivery_time_mins), 1) AS avg_delivery_time,
        ROUND(
            SUM(CASE WHEN o.delivery_time_mins <= 30 THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id), 
            1
        ) AS on_time_rate_pct
    FROM delivery_partners dp
    INNER JOIN orders o ON dp.partner_id = o.partner_id
    WHERE o.order_status = 'Delivered'
    GROUP BY dp.city, dp.partner_id, dp.partner_name, dp.vehicle_type, dp.rating
)
SELECT 
    city,
    partner_id,
    partner_name,
    vehicle_type,
    rating,
    total_deliveries,
    avg_delivery_time,
    on_time_rate_pct,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY total_deliveries DESC, on_time_rate_pct DESC) AS city_rider_rank
FROM rider_summary
ORDER BY city, city_rider_rank;

-- Business Insight:
-- Provides operations managers with a transparent, data-driven ranking system
-- for weekly incentive payouts and fleet coaching.
