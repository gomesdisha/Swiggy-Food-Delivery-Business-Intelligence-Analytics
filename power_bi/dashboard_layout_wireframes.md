# Power BI Dashboard Wireframe & Visual Blueprint — Swiggy BI

This guide outlines the layout, visual components, color codes, and user interactions for building the 3-page interactive Power BI report.

---

## Global Design System

* **Canvas Size:** 16:9 widescreen (1280 × 720 px or 1920 × 1080 px)
* **Background:** Light off-white `#F9FAFB`
* **Card Fill:** Pure white `#FFFFFF` with 2px border radius
* **Primary Brand Accent:** Swiggy Orange (`#FC8019`)
* **Secondary Brand Accent:** Dark Navy (`#1F2937`)
* **Success Color:** Mint Green (`#10B981`)
* **Alert / Late Color:** Coral Red (`#EF4444`)
* **Typography:** Segoe UI or DIN (consistent bold headers and clear metric callouts)

---

## Page 1: Executive Performance Overview

### Purpose
High-level C-suite dashboard displaying revenue scale, volume trends, city ranking, and payment channel share.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [LOGO] SWIGGY EXECUTIVE BUSINESS INTELLIGENCE                [Date Slicer: 2024] [City Slicer]   │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬──────────────────┤
│ TOTAL GMV (SALES) │ TOTAL ORDERS      │ AVG ORDER VALUE   │ ACTIVE RESTAURANTS│ CANCELLATION RATE│
│    ₹ 6.42 Cr      │      14,175       │       ₹ 453       │        175        │      5.5%        │
├───────────────────┴───────────────────┴───────────────────┴───────────────────┴──────────────────┤
│ [VISUAL 1: Area / Column Combo Chart]                     │ [VISUAL 2: Bar Chart]                │
│ Monthly GMV Trend & MoM Growth %                          │ GMV by City (Top Metro Breakdown)    │
│ • X-Axis: Month (Jan - Dec)                               │ • Y-Axis: City (Bengaluru, Mumbai,   │
│ • Column: Total GMV (Orange)                              │           Delhi, Hyderabad, Pune...) │
│ • Line: MoM Growth % (Navy)                               │ • X-Axis: Total GMV                  │
├───────────────────────────────────────────────────────────┼──────────────────────────────────────┤
│ [VISUAL 3: Clustered Bar Chart]                           │ [VISUAL 4: Donut Chart]              │
│ Top Cuisines by Revenue & Orders                          │ Payment Method Share                 │
│ • Y-Axis: Cuisine (Biryani, North Indian, South Indian...)│ • Values: Total Orders               │
│ • X-Axis: Total GMV                                       │ • Legend: UPI (63%), Credit Card,    │
│ • Tooltip: AOV & Total Orders                             │           Debit Card, COD            │
└───────────────────────────────────────────────────────────┴──────────────────────────────────────┘
```

### Visual Specifications
1. **Top KPI Bar (5 Card Visuals):**
   - Card 1: `[Total GMV]`
   - Card 2: `[Total Orders]`
   - Card 3: `[Average Order Value]`
   - Card 4: `[Active Restaurants]`
   - Card 5: `[Cancellation Rate %]`
2. **Monthly Trend (Line and Clustered Column Chart):**
   - Shared Axis: `orders[order_date]` (Month)
   - Column Values: `[Total GMV]`
   - Line Values: `[GMV MoM Growth %]`
3. **City Revenue (Horizontal Bar Chart):**
   - Y-Axis: `users[city]`
   - X-Axis: `[Total GMV]`
   - Data labels enabled in Currency format.
4. **Payment Split (Donut Chart):**
   - Legend: `orders[payment_method]`
   - Values: `[Total Orders]`

---

## Page 2: Swiggy One & Customer Loyalty

### Purpose
Demonstrate the commercial impact of the **Swiggy One** membership program on customer order frequency, basket size, and customer retention.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [LOGO] SWIGGY ONE MEMBERSHIP & CUSTOMER RETENTION             [City Filter] [Gender Filter]      │
├───────────────────┬───────────────────┬───────────────────┬──────────────────────────────────────┤
│ SWIGGY ONE SHARE  │ MEMBER AOV LIFT   │ ORDERS / MEMBER   │ NON-MEMBER ORDERS                    │
│      58.4%        │     + 24.2%       │   18.4 Orders/Yr  │     7.1 Orders/Yr                    │
├───────────────────┴───────────────────┴───────────────────┴──────────────────────────────────────┤
│ [VISUAL 1: 100% Stacked Bar Chart]                        │ [VISUAL 2: Grouped Bar Chart]        │
│ Swiggy One vs. Regular Orders across Cities               │ Average Spend per User: One vs Non-One│
│ • Y-Axis: City                                            │ • Category: City                     │
│ • X-Axis: % Share of Orders                               │ • Legend: Swiggy One vs Regular      │
│ • Legend: Swiggy One (Orange) vs Regular (Gray)           │                                      │
├───────────────────────────────────────────────────────────┼──────────────────────────────────────┤
│ [VISUAL 3: Treemap / Matrix]                              │ [VISUAL 4: Scatter Plot]             │
│ Customer Frequency Segmentation                           │ Customer Lifetime Value vs Frequency │
│ • Segments: Power Users (25+), Frequent (12-24),          │ • X-Axis: Total Orders Placed        │
│   Regular (5-11), Occasional (1-4)                        │ • Y-Axis: Total Spend (₹)            │
│ • Size: Total Revenue                                     │ • Legend: Swiggy One (Yes / No)      │
└───────────────────────────────────────────────────────────┴──────────────────────────────────────┘
```

### Visual Specifications
1. **KPI Header Cards:**
   - Card 1: `[Swiggy One Order Share %]`
   - Card 2: `[Member AOV Lift %]`
   - Card 3: `[Swiggy One Orders]`
   - Card 4: `[Active Customers]`
2. **City Adoption (100% Stacked Bar Chart):**
   - Y-Axis: `users[city]`
   - X-Axis: `[Swiggy One Orders]`, `[Regular Orders]`
3. **Customer Segmentation Matrix:**
   - Rows: RFM Frequency Tiers
   - Values: Count of Users, Total GMV, Average Spend per User

---

## Page 3: Delivery Logistics & SLA Control Tower

### Purpose
Operational intelligence for city logistics managers to monitor delivery speed, peak traffic delays, and delivery partner efficiency.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [LOGO] DELIVERY LOGISTICS & FLEET SLA CONTROL TOWER          [City Slicer] [Vehicle Slicer]      │
├───────────────────┬───────────────────┬───────────────────┬──────────────────────────────────────┤
│ AVG DELIVERY TIME │ ON-TIME RATE %    │ SLA BREACH RATE % │ ACTIVE FLEET RIDERS                  │
│     32.4 mins     │      78.6%        │      12.1%        │        120 Riders                    │
├───────────────────┴───────────────────┴───────────────────┴──────────────────────────────────────┤
│ [VISUAL 1: Heatmap / Matrix Table]                        │ [VISUAL 2: Bar Chart]                │
│ Delivery Duration by City & Time Slot                     │ On-Time Delivery Rate by City        │
│ • Rows: City                                              │ • Y-Axis: City                       │
│ • Columns: Breakfast, Lunch, Evening, Dinner, Late Night  │ • X-Axis: [On-Time Delivery Rate %]  │
│ • Values: [Average Delivery Time] (Color scale)           │ • Target Line: 85% Benchmark         │
├───────────────────────────────────────────────────────────┼──────────────────────────────────────┤
│ [VISUAL 3: Clustered Column Chart]                        │ [VISUAL 4: Table with Data Bars]     │
│ Delivery Duration: Electric Vehicles vs. Motorcycles      │ Top Delivery Partners Scorecard      │
│ • X-Axis: City                                            │ • Columns: Rider Name, City, Vehicle,│
│ • Columns: EV Delivery Mins vs Petrol Motorcycle Mins     │   Deliveries, Rating, On-Time %      │
└───────────────────────────────────────────────────────────┴──────────────────────────────────────┘
```

### Visual Specifications
1. **Key Operational KPIs:**
   - Card 1: `[Average Delivery Time]`
   - Card 2: `[On-Time Delivery Rate %]`
   - Card 3: `[SLA Breach Rate %]`
   - Card 4: `[Active Fleet Riders]`
2. **Delivery Heatmap (Matrix):**
   - Rows: `users[city]`
   - Columns: Meal Slot (Lunch, Dinner, Late Night)
   - Values: `[Average Delivery Time]` with conditional background color formatting (Green $\rightarrow$ Red).
3. **Fleet Efficiency Table:**
   - Columns: `partner_name`, `city`, `vehicle_type`, `total_deliveries`, `rating`, `on_time_rate_pct`.
