# Power BI Data Modeling & Integration Guide — Swiggy BI

This guide explains how to connect Power BI Desktop to your Swiggy dataset, configure the **Star Schema data model**, and manage relationships.

---

## 1. Connecting Data to Power BI Desktop

You can load the data into Power BI through either of two paths:

### Path A: Direct Import via Clean CSVs (Fastest & Most Reliable)
1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV**.
3. Select and load each CSV from your project `data/` folder:
   - `users.csv`
   - `restaurants.csv`
   - `menu_items.csv`
   - `delivery_partners.csv`
   - `orders.csv`
   - `order_items.csv`
4. In Power Query, verify data types:
   - `order_date` $\rightarrow$ Date
   - `total_amount`, `price`, `line_total`, `cost_for_two` $\rightarrow$ Fixed Decimal Number (Currency)
   - `is_swiggy_one` $\rightarrow$ True/False or Whole Number (0 or 1)
   - `delivery_time_mins` $\rightarrow$ Whole Number
5. Click **Close & Apply**.

### Path B: Connecting Directly to MySQL Database
1. In Power BI Desktop, click **Get Data** $\rightarrow$ **Database** $\rightarrow$ **MySQL database**.
2. Server: `localhost:3306` (or `127.0.0.1:3306`).
3. Database: `swiggy_db`.
4. Enter your MySQL username (`root`) and password.
5. Select all tables and click **Load**.

---

## 2. Star Schema Architecture

Power BI performs fastest and produces the cleanest DAX calculations when structured in a **Star Schema** (Fact tables in the center, surrounded by Dimension tables).

```
          ┌───────────────────────────┐       ┌───────────────────────────┐
          │      dim_restaurants      │       │         dim_users         │
          │ • restaurant_id (PK)      │       │ • user_id (PK)            │
          │ • restaurant_name         │       │ • name, city, gender, age │
          │ • city, cuisine, rating   │       │ • is_swiggy_one           │
          └─────────────┬─────────────┘       └─────────────┬─────────────┘
                        │ 1                                 │ 1
                        │                                   │
                        │ *                                 │ *
          ┌─────────────▼───────────────────────────────────▼─────────────┐
          │                         fact_orders                           │
          │ • order_id (PK)                                               │
          │ • user_id (FK) ───────────┐                                   │
          │ • restaurant_id (FK)      │                                   │
          │ • partner_id (FK)         │                                   │
          │ • order_date, order_time  │                                   │
          │ • total_amount, discount  │                                   │
          │ • delivery_time_mins      │                                   │
          └───────▲─────────────────▲─┴───────────────────┬───────────────┘
                  │ *               │ *                   │ 1
                  │                 │                     │
                  │ 1               │ 1                   │ *
   ┌──────────────┴──────────┐      │       ┌─────────────▼─────────────┐
   │  dim_delivery_partners  │      │       │     fact_order_items      │
   │ • partner_id (PK)       │      │       │ • order_item_id (PK)      │
   │ • partner_name, city    │      │       │ • order_id (FK)           │
   │ • vehicle_type, rating  │      │       │ • item_id (FK) ────────┐  │
   └─────────────────────────┘      │       │ • price, quantity      │  │
                                    │       └────────────────────────┼──┘
                        ┌───────────┴───────────┐                    │ *
                        │       dim_date        │                    │
                        │ • Date (PK)           │                    │ 1
                        │ • Year, Month, Day    │       ┌────────────▼────────────┐
                        │ • Quarter, DayOfWeek  │       │     dim_menu_items      │
                        └───────────────────────┘       │ • item_id (PK)          │
                                                        │ • item_name, category   │
                                                        │ • veg_or_non_veg        │
                                                        └─────────────────────────┘
```

---

## 3. Relationship Settings in Model View

In Power BI **Model View**, set up the following relationships:

| From Table (Foreign Key) | To Table (Primary Key) | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- |
| `orders[user_id]` | `users[user_id]` | Many to One (*:1) | Single |
| `orders[restaurant_id]` | `restaurants[restaurant_id]` | Many to One (*:1) | Single |
| `orders[partner_id]` | `delivery_partners[partner_id]` | Many to One (*:1) | Single |
| `order_items[order_id]` | `orders[order_id]` | Many to One (*:1) | Single |
| `order_items[item_id]` | `menu_items[item_id]` | Many to One (*:1) | Single |

---

## 4. Best Practices for High Performance
1. **Hide Foreign Key Columns:** Hide IDs like `orders[user_id]` and `orders[restaurant_id]` from report view so users slice exclusively using dimension tables.
2. **Format Measures Explicitly:** Set `Total GMV` to Indian Currency or Currency (`₹ #,##0`), percentages to `0.0%`, and delivery minutes to whole numbers.
3. **Use Explicit Measures:** Never drag numeric columns directly onto charts; always use the pre-built DAX measures from `dax_measures_library.md`.
