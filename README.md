# 🛵 Swiggy Food Delivery & Marketplace Business Intelligence Analytics

[![Database: MySQL](https://img.shields.io/badge/Database-MySQL_8.0-00758F?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![BI Tool: Power BI](https://img.shields.io/badge/BI_Tool-Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Web App: Streamlit](https://img.shields.io/badge/Decision_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Modeling: Excel](https://img.shields.io/badge/Modeling-Microsoft_Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://www.microsoft.com/en-us/microsoft-365/excel)

An end-to-end Data Analytics and Business Intelligence project analyzing Swiggy's food delivery operations across 7 major Indian metro cities (**Bangalore, Mumbai, Delhi, Hyderabad, Pune, Kolkata, and Chennai**).

The project connects **MySQL 8.0**, **Power BI**, **Streamlit**, and **Excel** to evaluate marketplace revenue, customer loyalty (**Swiggy One** membership ROI), restaurant revenue rankings, and delivery SLA efficiency across 15,000 orders, 175 real scraped restaurants, and 1,200 menu items.

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
                          │  REAL SCRAPED SWIGGY DATASETS                │
                          │  • 175 Iconic Restaurants across 7 Cities    │
                          │  • 1,200 Real Menu Items & Actual Prices     │
                          └──────────────────────┬───────────────────────┘
                                                 │
                                                 ▼
                          ┌──────────────────────────────────────────────┐
                          │  1. MySQL 8.0 DATABASE (`swiggy_db`)         │
                          │  • Star Schema DDL with PK/FK constraints    │
                          │  • 15 Production Business Analysis Queries   │
                          │  • Window Functions: DENSE_RANK, LAG, NTILE  │
                          └──────────────┬───────────────────────────────┘
                                         │
        ┌────────────────────────────────┼───────────────────────────────┐
        ▼                                ▼                               ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 2. POWER BI DASHBOARD   │ │ 3. STREAMLIT WEB APP    │ │ 4. EXCEL FINANCIAL MODEL│
│ • Native Project (.pbip)│ │ • Interactive Slicers   │ │ • Monthly Business Rev. │
│ • Star Schema Model     │ │ • Dynamic Plotly Charts │ │ • Take-Rate & Unit P&L  │
│ • 22 Custom Measures    │ │ • Live Decision Engine  │ │ • Dynamic Excel Formulas│
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

---

## 🗄️ Relational Database Schema (`swiggy_db`)

The database is structured into 6 normalized relational tables:
1. **`users`** (`user_id`, `name`, `gender`, `age`, `city`, `signup_date`, `is_swiggy_one`)
2. **`restaurants`** (`restaurant_id`, `restaurant_name`, `city`, `cuisine`, `rating`, `rating_count`, `cost_for_two`, `swiggy_url`)
3. **`menu_items`** (`item_id`, `item_name`, `menu_category`, `price`, `veg_or_non_veg`)
4. **`delivery_partners`** (`partner_id`, `partner_name`, `city`, `vehicle_type`, `rating`)
5. **`orders`** (`order_id`, `user_id`, `restaurant_id`, `partner_id`, `order_date`, `order_time`, `order_status`, `total_amount`, `discount_amount`, `delivery_fee`, `delivery_time_mins`, `payment_method`)
6. **`order_items`** (`order_item_id`, `order_id`, `item_id`, `item_name`, `price`, `quantity`, `line_total`)

---

## 📊 Deliverables & Features

### 1. Power BI Executive Dashboard
* File: [`power_bi/Swiggy_Food_Delivery_Analytics.pbip`](power_bi/Swiggy_Food_Delivery_Analytics.pbip)
* Open directly in **Power BI Desktop**.
* Pre-built **Star Schema** with 1-to-many relationships and 22 custom DAX measures for executive reporting (`Total GMV`, `AOV`, `Swiggy One Order Share %`, `On-Time Delivery Rate %`, `GMV MoM Growth %`).
* Companion interactive web version: [`power_bi/swiggy_bi_dashboard.html`](power_bi/swiggy_bi_dashboard.html) (open directly in any browser).

### 2. Streamlit Dynamic Decision-Support Application
* File: [`streamlit_app/app.py`](streamlit_app/app.py)
* A fully interactive decision application with **live reactive filtering**:
  * **Dynamic Multi-Select Slicers:** Filter by city, customer tier (Swiggy One vs. Regular), order status, and date range.
  * **Interactive Plotly Visuals:** Monthly GMV trends, payment channel donut chart, city revenue horizontal bars, and cuisine distribution.
  * **Customer Loyalty Workbench:** RFM Frequency tiers and searchable VIP Top 5% Spenders table.
  * **Logistics Control Tower:** Average delivery speed by city and Electric Vehicle (EV) vs. Petrol fleet benchmarking.

### 3. Production MySQL 8.0 Analysis
* Files: [`sql/01_swiggy_schema.sql`](sql/01_swiggy_schema.sql), [`sql/02_load_data_mysql.sql`](sql/02_load_data_mysql.sql), [`sql/03_swiggy_business_analysis.sql`](sql/03_swiggy_business_analysis.sql)
* 15 high-value business queries demonstrating:
  * **Top 3 Restaurants per City by Revenue** using `DENSE_RANK() OVER (PARTITION BY city ORDER BY revenue DESC)`.
  * **Month-over-Month (MoM) GMV Growth** using `LAG()`.
  * **VIP Customer Segmentation** using `NTILE(20)`.
  * **Quality Risk Alert** identifying restaurants with 50+ orders but ratings below 4.0.

### 4. Excel Monthly Business Review (MBR) & Unit Economics
* File: [`excel/swiggy_business_performance_review.xlsx`](excel/swiggy_business_performance_review.xlsx)
* Designed with Swiggy brand styling (`#FC8019`).
* **Tab 1: Executive Summary:** Top KPI cards and city breakdown table.
* **Tab 2: Monthly Business Review:** Dynamic month-by-month table using `SUMIFS`, `AVERAGEIFS`, and MoM % formulas.
* **Tab 3: Commission & Take-Rate P&L:** Unit economics model analyzing restaurant commission (21%), delivery fees, rider payouts (₹42/order), and net contribution margin.

### 5. Executive Insights Report
* File: [`docs/EXECUTIVE_INSIGHTS_REPORT.md`](docs/EXECUTIVE_INSIGHTS_REPORT.md)
* Strategic C-suite report analyzing Swiggy One ROI, peak-hour bottlenecks, and Electric Vehicle fleet expansion.

---

## 🚀 How to Run this Project Locally

### 1. Run the Interactive Streamlit App
```bash
# Navigate to project directory
cd Swiggy-Food-Delivery-Business-Intelligence-Analytics

# Launch Streamlit
streamlit run streamlit_app/app.py
```

### 2. Open the Power BI Dashboard
* Double-click `power_bi/Swiggy_Food_Delivery_Analytics.pbip` to open directly in **Power BI Desktop**.
* In Power BI Desktop, click **File** $\rightarrow$ **Save As** $\rightarrow$ save as **`Swiggy_Food_Delivery_Analytics.pbix`**.

### 3. Run the MySQL Scripts in MySQL Workbench
1. Open **MySQL Workbench** and connect to your local MySQL server.
2. Open and execute [`sql/01_swiggy_schema.sql`](sql/01_swiggy_schema.sql) (click the ⚡ icon) to create `swiggy_db` and all tables.
3. Open and execute [`sql/02_populate_swiggy_db.sql`](sql/02_populate_swiggy_db.sql) (click the ⚡ icon) to populate all 15,000 orders, 32,145 order items, users, riders, and restaurants in one click with zero errors!
4. Open and execute [`sql/03_swiggy_business_analysis.sql`](sql/03_swiggy_business_analysis.sql) to run the 15 analytical queries!

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
│   ├── 02_populate_swiggy_db.sql        # One-click direct DB population script
│   ├── 02_load_data_mysql.sql           # Data ingestion documentation & verification
│   └── 03_swiggy_business_analysis.sql  # 15 Core Business Queries
├── power_bi/                             # Power BI Dashboard Assets
│   ├── Swiggy_Food_Delivery_Analytics.pbip # Native Power BI Project file
│   └── swiggy_bi_dashboard.html         # Interactive Web Dashboard
├── streamlit_app/                        # Dynamic Streamlit Application
│   └── app.py                           # Full interactive decision engine
├── excel/                                # Excel financial model
│   └── swiggy_business_performance_review.xlsx
├── docs/                                 # Business documentation
│   └── EXECUTIVE_INSIGHTS_REPORT.md     # Strategic leadership report
├── .gitignore                            # Ignores internal scripts & private files
└── README.md                            # Flagship project documentation
```

---

## 👤 Author
* **Disha Gomes** — [GitHub](https://github.com/gomesdisha)
