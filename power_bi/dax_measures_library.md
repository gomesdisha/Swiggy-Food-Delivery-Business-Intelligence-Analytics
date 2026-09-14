# Power BI DAX Measures Library — Swiggy Business Intelligence

This document contains production-ready **DAX (Data Analysis Expressions)** measures organized into functional folders. You can copy and paste these directly into Power BI Desktop.

---

## Metric Folder: 1. Core Financials & Revenue

### 1. Total Delivered Orders
```dax
Total Orders = 
CALCULATE(
    COUNTROWS('orders'),
    'orders'[order_status] = "Delivered"
)
```

### 2. Gross Merchandise Value (GMV)
```dax
Total GMV = 
CALCULATE(
    SUM('orders'[total_amount]),
    'orders'[order_status] = "Delivered"
)
```

### 3. Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE(
    [Total GMV],
    [Total Orders],
    0
)
```

### 4. Total Discounts Funded
```dax
Total Discounts = 
CALCULATE(
    SUM('orders'[discount_amount]),
    'orders'[order_status] = "Delivered"
)
```

### 5. Delivery Fee Revenue
```dax
Total Delivery Fees = 
CALCULATE(
    SUM('orders'[delivery_fee]),
    'orders'[order_status] = "Delivered"
)
```

### 6. Swiggy Estimated Commission (Take-Rate ~21%)
```dax
Swiggy Commission Revenue = 
[Total GMV] * 0.21
```

---

## Metric Folder: 2. Time Intelligence (MoM & YoY Growth)

### 7. Previous Month GMV
```dax
Previous Month GMV = 
CALCULATE(
    [Total GMV],
    PREVIOUSMONTH('orders'[order_date])
)
```

### 8. Month-over-Month (MoM) GMV Growth %
```dax
GMV MoM Growth % = 
VAR PrevGMV = [Previous Month GMV]
RETURN
    IF(
        ISBLANK(PrevGMV),
        BLANK(),
        DIVIDE([Total GMV] - PrevGMV, PrevGMV, 0)
    )
```

### 9. Year-to-Date (YTD) GMV
```dax
YTD GMV = 
TOTALYTD(
    [Total GMV],
    'orders'[order_date]
)
```

---

## Metric Folder: 3. Swiggy One & Customer Loyalty

### 10. Swiggy One Orders
```dax
Swiggy One Orders = 
CALCULATE(
    [Total Orders],
    'users'[is_swiggy_one] = 1
)
```

### 11. Regular User Orders
```dax
Regular Orders = 
CALCULATE(
    [Total Orders],
    'users'[is_swiggy_one] = 0
)
```

### 12. Swiggy One Order Share %
```dax
Swiggy One Order Share % = 
DIVIDE(
    [Swiggy One Orders],
    [Total Orders],
    0
)
```

### 13. Swiggy One GMV Share %
```dax
Swiggy One GMV Share % = 
VAR OneGMV = CALCULATE([Total GMV], 'users'[is_swiggy_one] = 1)
RETURN
    DIVIDE(OneGMV, [Total GMV], 0)
```

### 14. Active Ordering Customers
```dax
Active Customers = 
CALCULATE(
    DISTINCTCOUNT('orders'[user_id]),
    'orders'[order_status] = "Delivered"
)
```

---

## Metric Folder: 4. Delivery Logistics & SLA Performance

### 15. Average Delivery Duration (Minutes)
```dax
Average Delivery Time = 
CALCULATE(
    AVERAGE('orders'[delivery_time_mins]),
    'orders'[order_status] = "Delivered"
)
```

### 16. On-Time Deliveries (≤ 35 Minutes)
```dax
On-Time Deliveries = 
CALCULATE(
    [Total Orders],
    'orders'[delivery_time_mins] <= 35
)
```

### 17. On-Time Delivery Rate %
```dax
On-Time Delivery Rate % = 
DIVIDE(
    [On-Time Deliveries],
    [Total Orders],
    0
)
```

### 18. Delayed Orders (> 40 Minutes SLA Breach)
```dax
Delayed Orders = 
CALCULATE(
    [Total Orders],
    'orders'[delivery_time_mins] > 40
)
```

### 19. SLA Breach Rate %
```dax
SLA Breach Rate % = 
DIVIDE(
    [Delayed Orders],
    [Total Orders],
    0
)
```

---

## Metric Folder: 5. Operational & Cancellation Diagnostics

### 20. Total Cancelled Orders
```dax
Cancelled Orders = 
CALCULATE(
    COUNTROWS('orders'),
    'orders'[order_status] = "Cancelled"
)
```

### 21. Order Cancellation Rate %
```dax
Cancellation Rate % = 
DIVIDE(
    [Cancelled Orders],
    COUNTROWS('orders'),
    0
)
```

### 22. Lost Revenue from Cancellations
```dax
Lost Cancellation GMV = 
CALCULATE(
    SUM('orders'[total_amount]),
    'orders'[order_status] = "Cancelled"
)
```
