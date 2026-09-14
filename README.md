# 🛵 Swiggy Food Delivery & Marketplace Business Intelligence Analytics

[![Database: MySQL](https://img.shields.io/badge/Database-MySQL_8.0-00758F?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![BI Tool: Power BI](https://img.shields.io/badge/BI_Tool-Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Modeling: Excel](https://img.shields.io/badge/Modeling-Microsoft_Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/en-us/microsoft-365/excel)
[![ETL: Python](https://img.shields.io/badge/Pipeline-Python_3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

An end-to-end Data Analytics and Business Intelligence project analyzing Swiggy's food delivery transactions across 7 major Indian metro cities (**Bangalore, Mumbai, Delhi, Hyderabad, Pune, Kolkata, and Chennai**). 

The project utilizes **MySQL**, **Power BI**, and **Excel** to evaluate marketplace revenue, customer loyalty (**Swiggy One** membership ROI), restaurant revenue rankings, and delivery SLA efficiency across 15,000 orders, 175 real scraped restaurants, and 1,200 menu items.

---

## 📌 Executive Summary & Key Results

| Business Metric | Value | Key Business Takeaway |
| :--- | :--- | :--- |
| **Gross Merchandise Value (GMV)** | **₹6.42 Crore** | Total marketplace food sales across FY2024. |
| **Total Delivered Orders** | **14,175** | Across 1,000 active customers and 175 restaurants. |
| **Average Order Value (AOV)** | **₹453** | Highest in Delhi NCR (₹512) due to family dinner orders. |
| **Swiggy One Order Share** | **58.4%** | Members order **2.6x more frequently** than non-members. |
| **On-Time Delivery Rate** | **78.6%** | Delivered within 35 mins; 12.1% delayed during monsoon/dinner peaks. |
| **Dominant Payment Channel** | **UPI (63%)** | Cash on Delivery (COD) represents 7% of orders but **44% of cancellations**. |

---

## 🏗️ System Architecture

```
                          ┌──────────────────────────────────────────────┐
                          │  REAL SCRAPED SWIGGY DATASETS (GitHub/Web)   │
                          │  • 175 Iconic Restaurants across 7 Cities    │
                          │  • 1,200 Real Menu Items & Actual Prices     │
                          └──────────────────────┬───────────────────────┘
                                                 │
                                                 ▼
                          ┌──────────────────────────────────────────────┐
                          │  1. DATASET BUILDER & ETL (Python)           │
                          │  • Synthesizes realistic customer profiles   │
                          │  • Generates 15k orders with seasonality     │
                          │  • Exports 6 clean relational CSV tables     │
                          └──────────────────────┬───────────────────────┘
                                                 │
                                                 ▼
                          ┌──────────────────────────────────────────────┐
                          │  2. MySQL 8.0 DATABASE (`swiggy_db`)         │
                          │  • Star Schema DDL with PK/FK constraints    │
                          │  • 15 Production Business Analysis Queries   │
                          │  • Window Functions: DENSE_RANK, LAG, NTILE  │
                          └──────────────┬───────────────────────────────┘
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
          ┌─────────────────────────────┐ ┌─────────────────────────────┐
          │  3. POWER BI DASHBOARD      │ │  4. EXCEL FINANCIAL MODEL   │
          │  • Executive Overview       │ │  • Monthly Business Review  │
          │  • Swiggy One Retention     │ │  • Take-Rate & Unit P&L     │
          │  • Delivery Logistics Tower │ │  • Dynamic Formulas         │
          │  • 22 Custom DAX Measures   │ │    (SUMIFS, AVERAGEIFS)     │
          └─────────────────────────────┘ └─────────────────────────────┘
```

---

## 🗄️ Relational Database Schema (`swiggy_db`)

The database is organized into 6 normalized relational tables:
1. **`users`** (`user_id`, `name`, `gender`, `age`, `city`, `signup_date`, `is_swiggy_one`)
2. **`restaurants`** (`restaurant_id`, `restaurant_name`, `city`, `cuisine`, `rating`, `rating_count`, `cost_for_two`, `swiggy_url`)
3. **`menu_items`** (`item_id`, `item_name`, `menu_category`, `price`, `veg_or_non_veg`)
4. **`delivery_partners`** (`partner_id`, `partner_name`, `city`, `vehicle_type`, `rating`)
5. **`orders`** (`order_id`, `user_id`, `restaurant_id`, `partner_id`, `order_date`, `order_time`, `order_status`, `total_amount`, `discount_amount`, `delivery_fee`, `delivery_time_mins`, `payment_method`)
6. **`order_items`** (`order_item_id`, `order_id`, `item_id`, `item_name`, `price`, `quantity`, `line_total`)

👉 *Full schema specifications available in [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md).*

---

## 💡 Top SQL Business Queries & Technical Highlights

All 15 SQL queries are located in [`sql/03_swiggy_business_analysis.sql`](sql/03_swiggy_business_analysis.sql). Here are 3 signature queries:

### 1. Top 3 Restaurants by Total Revenue in Each City (`DENSE_RANK`)
```sql
WITH restaurant_city_sales AS (
    SELECT 
        r.city,
        r.restaurant_name,
        r.cuisine,
        r.rating,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_revenue,
        DENSE_RANK() OVER (PARTITION BY r.city ORDER BY SUM(o.total_amount) DESC) AS city_rank
    FROM restaurants r
    INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
    WHERE o.order_status = 'Delivered'
    GROUP BY r.city, r.restaurant_name, r.cuisine, r.rating
)
SELECT city, city_rank, restaurant_name, cuisine, rating, total_revenue
FROM restaurant_city_sales
WHERE city_rank <= 3
ORDER BY city, city_rank;
```

### 2. Month-over-Month (MoM) GMV Growth (`LAG`)
```sql
WITH monthly_metrics AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        SUM(total_amount) AS total_gmv
    FROM orders
    WHERE order_status = 'Delivered'
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    order_month,
    total_gmv,
    LAG(total_gmv, 1) OVER (ORDER BY order_month) AS prev_month_gmv,
    ROUND((total_gmv - LAG(total_gmv, 1) OVER (ORDER BY order_month)) / 
          LAG(total_gmv, 1) OVER (ORDER BY order_month) * 100, 2) AS mom_growth_pct
FROM monthly_metrics;
```

### 3. High-Volume / Low-Rating Quality Risk Alert
```sql
SELECT 
    r.restaurant_name,
    r.city,
    r.cuisine,
    r.rating,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_revenue
FROM restaurants r
INNER JOIN orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_name, r.city, r.cuisine, r.rating
HAVING r.rating < 4.0 AND total_orders >= 75
ORDER BY total_orders DESC;
```

---

## 📊 Power BI Dashboard Blueprint

The Power BI report contains 3 dedicated executive pages:
* **Page 1: Executive Performance Overview:** Top KPI cards, Monthly GMV vs. MoM growth line/bar combo, City revenue breakdown, and Payment channel donut.
* **Page 2: Swiggy One & Customer Loyalty:** Member vs. Non-Member unit economics, Frequency tier segmentation, and Customer Lifetime Value (LTV) scatter plots.
* **Page 3: Delivery Logistics & SLA Control Tower:** Average delivery time heatmap across meal slots, On-Time delivery rate by city, and EV vs. Motorcycle fleet benchmarking.

👉 *Explore the [DAX Measures Library](power_bi/dax_measures_library.md) and [Dashboard Wireframes](power_bi/dashboard_layout_wireframes.md).*

---

## 📗 Excel Monthly Business Review (MBR) & Unit Economics

Located in [`excel/swiggy_business_performance_review.xlsx`](excel/swiggy_business_performance_review.xlsx):
* **Tab 1: Executive Summary:** KPI cards and city-wise performance metrics.
* **Tab 2: Monthly Business Review (MBR):** Dynamic month-by-month financial statement with `SUMIFS`, `AVERAGEIFS`, and MoM % formulas.
* **Tab 3: Commission & Take-Rate P&L:** Unit economics model analyzing restaurant commission (21%), customer delivery fees, rider payouts, and net contribution margin.

---

## 🚀 How to Run this Project Locally

### 1. Clone the Repository
```bash
git clone https://github.com/gomesdisha/Swiggy-Food-Delivery-Business-Intelligence-Analytics.git
cd Swiggy-Food-Delivery-Business-Intelligence-Analytics
```

### 2. Set Up MySQL Database
1. Open **MySQL Workbench**.
2. Run `sql/01_swiggy_schema.sql` to create `swiggy_db` and tables.
3. Import the CSV files from `data/` using the **Table Data Import Wizard** (see `sql/02_load_data_mysql.sql`).
4. Execute `sql/03_swiggy_business_analysis.sql` to view all analytical results!

### 3. Open in Power BI Desktop
1. Launch Power BI Desktop.
2. Connect to the clean CSV files in `data/` (or connect directly to your local MySQL database).
3. Verify relationships match the Star Schema in `power_bi/power_bi_data_model_guide.md`.
4. Copy-paste DAX measures from `power_bi/dax_measures_library.md`.

---

## 📁 Repository Structure

```
Swiggy-Food-Delivery-Business-Intelligence-Analytics/
├── data/                                 # Clean relational CSV datasets
│   ├── users.csv
│   ├── restaurants.csv
│   ├── menu_items.csv
│   ├── delivery_partners.csv
│   ├── orders.csv
│   └── order_items.csv
├── sql/                                  # Production SQL scripts
│   ├── 01_swiggy_schema.sql             # Table DDL & indexes
│   ├── 02_load_data_mysql.sql           # Data ingestion scripts
│   └── 03_swiggy_business_analysis.sql  # 15 Core Business Queries
├── power_bi/                             # Power BI design assets
│   ├── dax_measures_library.md          # 22 Production DAX measures
│   ├── power_bi_data_model_guide.md     # Star schema modeling guide
│   └── dashboard_layout_wireframes.md   # Visual blueprints & layouts
├── excel/                                # Excel financial model
│   └── swiggy_business_performance_review.xlsx
├── src/                                  # Data generation & automation scripts
│   ├── build_swiggy_dataset.py          # Scraped data ingestion & order synthesis
│   └── build_excel_model.py             # OpenPyXL automated workbook builder
├── docs/                                 # Project documentation
│   ├── DATA_DICTIONARY.md               # Table & column descriptions
│   ├── EXECUTIVE_INSIGHTS_REPORT.md     # Business insights & strategy
│   └── INTERVIEW_QA_GUIDE.md            # Scripted interview talking points
└── README.md                            # Flagship project documentation
```

---

## 👤 Author
* **Disha Gomes** — [GitHub](https://github.com/gomesdisha)
