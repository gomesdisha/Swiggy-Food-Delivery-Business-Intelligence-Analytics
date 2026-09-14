# Swiggy Business Intelligence — Interview Discussion & Q&A Guide

Use this guide to prepare for interview discussions with recruiters, hiring managers, and lead data engineers.

---

## 1. The 60-Second Project Elevator Pitch

> **Interviewer:** *"Can you walk me through your Swiggy project?"*
>
> **Your Scripted Answer:**
> *"I designed an end-to-end business intelligence project analyzing Swiggy's food delivery marketplace across 7 top Indian metro cities, covering 15,000 orders, 175 real scraped restaurants, and over 1,200 menu items.
>
> The core objective was answering three strategic business questions:
> 1. **Customer Loyalty & Unit Economics:** What is the actual financial lift of the **Swiggy One** membership program?
> 2. **Restaurant & Cuisine Dynamics:** Which restaurants and cuisines drive marketplace gross merchandise value (GMV), and where are customer quality risks located?
> 3. **Logistics & Delivery SLAs:** Where do delivery delays occur, and how do Electric Vehicles perform compared to petrol motorcycles?
>
> I used **MySQL** to design a relational schema and write complex analytical queries utilizing Window Functions like `DENSE_RANK()`, `LAG()`, `NTILE()`, and CTEs. Then, I built an interactive **Power BI dashboard** with a Star Schema data model and custom DAX measures for executive visibility, accompanied by an **Excel** monthly review model for unit economics and commission analysis."*

---

## 2. Technical SQL Questions & Scripted Answers

### Q1: *"How did you find the top 3 restaurants by revenue in each city?"*
* **Answer:** *"I used a Common Table Expression (CTE) to aggregate total sales by restaurant and city, and applied the `DENSE_RANK()` window function partitioned by `city` and ordered by `total_revenue DESC`. Then, in the outer query, I filtered for `city_rank <= 3`. I specifically chose `DENSE_RANK()` over `ROW_NUMBER()` to ensure restaurants with tied revenues received the same ranking without skipping ranks."*

### Q2: *"How did you calculate Month-over-Month (MoM) revenue growth in SQL?"*
* **Answer:** *"I aggregated delivered order revenue by month using `DATE_FORMAT(order_date, '%Y-%m')`, and used the `LAG(total_gmv, 1) OVER (ORDER BY order_month)` window function to retrieve the previous month's revenue. From there, I calculated `(Current_GMV - Prev_GMV) / Prev_GMV * 100`."*

### Q3: *"How did you prevent double counting or cartesian fan-out between orders and order items?"*
* **Answer:** *"In relational schemas, order-level attributes like `delivery_fee` and total `discount_amount` exist at the order grain, while dish prices and quantities exist at the line-item grain. To prevent fan-out, I separated order-level KPIs (like AOV and delivery durations) by querying the `orders` table directly, while dish-level metrics (such as veg vs. non-veg share) were calculated by joining `order_items` with `menu_items`."*

---

## 3. Power BI & DAX Questions & Scripted Answers

### Q4: *"Why did you use a Star Schema in Power BI rather than a single flat table?"*
* **Answer:** *"A Star Schema is Microsoft's recommended architecture for Power BI. It separates business events (`fact_orders`, `fact_order_items`) from business context (`dim_users`, `dim_restaurants`, `dim_delivery_partners`, `dim_menu_items`). It optimizes memory usage through VertiPaq compression, eliminates data redundancy, and ensures DAX filters propagate cleanly without bidirectional ambiguity."*

### Q5: *"Can you explain one complex DAX measure you wrote?"*
* **Answer:** *"For measuring customer retention, I wrote `[Swiggy One GMV Share %]`. It calculates the proportion of total delivered GMV coming from subscribers using `VAR OneGMV = CALCULATE([Total GMV], 'users'[is_swiggy_one] = 1)` and `DIVIDE(OneGMV, [Total GMV], 0)`. I also wrote `[GMV MoM Growth %]` using `PREVIOUSMONTH('orders'[order_date])` to benchmark growth rates."*

---

## 4. Business & Commercial Understanding Questions

### Q6: *"Does Swiggy lose money by offering Free Delivery to Swiggy One members?"*
* **Answer:** *"On an individual order basis, Swiggy absorbs the ₹35–₹50 delivery fee. However, at a customer lifetime level, Swiggy One members order 2.6x more frequently (18.4 orders vs 7.1 orders/year) and have a 24% higher basket size. Swiggy earns a 21% commission on food sales from restaurants. The higher order volume generates substantially more gross commission profit than the cost of subsidized delivery, making the program net profitable by ~₹1,850 per subscriber per year."*

### Q7: *"What would you do with restaurants having high order volume but ratings below 4.0?"*
* **Answer:** *"In Query 12 of my SQL analysis, I identified 7 restaurants with over 75 orders but ratings under 4.0. These restaurants generate significant commission for Swiggy but risk customer churn due to poor food quality or slow preparation times. My recommendation is to audit their kitchen prep times, delay delivery rider dispatch until the food is actually ready (reducing rider wait time), and set quality improvement SLAs before featuring them in promotional carousels."*
