# Swiggy Food Delivery & Marketplace Analytics — Executive Insights Report

**Prepared for:** Swiggy Business Operations & Product Leadership  
**Author:** Disha Gomes  
**Period Analyzed:** Full Year 2024 (15,000 Orders across 7 Indian Metro Cities)  
**Database:** MySQL 8.0 (`swiggy_db`)

---

## 1. Executive Summary

This report analyzes Swiggy's food delivery operations across 7 major metro cities (**Bangalore, Mumbai, Delhi, Hyderabad, Pune, Kolkata, and Chennai**). The objective is to evaluate revenue drivers, assess the return on investment of the **Swiggy One** membership program, benchmark city logistics SLAs, and uncover high-impact operational optimizations.

### Key Performance Highlights:
* **Total Gross Merchandise Value (GMV):** ₹6.42 Crore across 14,175 successfully delivered orders.
* **Average Order Value (AOV):** ₹453 per delivered order.
* **Swiggy One Dominance:** Swiggy One subscribers account for **36% of the customer base**, but generate **58.4% of total order volume** and **61.2% of annual GMV**.
* **On-Time Delivery Performance:** 78.6% of orders were delivered within the 35-minute target; 12.1% suffered from severe delays (>40 mins).
* **Payment Modernization:** UPI accounts for **63% of transactions**, while Cash on Delivery (COD) accounts for only 7% of orders but represents **44% of total cancellations**.

---

## 2. Core Business Findings

### Finding 1: Swiggy One is the Primary Engine of Customer Lifetime Value (LTV)
* **Frequency Lift:** Swiggy One members place an average of **18.4 orders per year**, compared to just **7.1 orders per year** for non-members (a **2.6x frequency lift**).
* **Basket Size Expansion:** Members have an Average Order Value of **₹488**, compared to **₹393** for regular users (+24.2% higher ticket size).
* **Unit Economics Assessment:** While Swiggy absorbs ₹35–₹50 in delivery fees on member orders, the increased order volume and 21% restaurant commission generate **+₹1,850 in net incremental annual contribution margin per subscriber**.

### Finding 2: City-Level Revenue & AOV Nuances
* **Bangalore & Mumbai** are the highest volume markets, contributing **42% of total marketplace GMV**.
* **Delhi NCR** exhibits the highest AOV (**₹512**), driven by large evening dinner family orders (North Indian / Mughlai platters and tandoori breads).
* **Hyderabad** demonstrates the strongest single-cuisine concentration: Biryani accounts for **68% of all food orders** in the city.

### Finding 3: Peak Hour Ordering Bottlenecks
* The ordering window follows an extreme bimodal distribution:
  * **Lunch Peak (12:00 PM – 3:00 PM):** 35% of daily volume.
  * **Dinner Peak (7:00 PM – 10:30 PM):** 48% of daily volume.
* Dinner peak orders experience an average delivery time of **35.8 minutes**, compared to **29.4 minutes** during afternoon hours, resulting from restaurant kitchen backlogs and peak city traffic.

### Finding 4: Electric Vehicle (EV) Delivery Fleet Viability
* Analysis of 120 delivery partners indicates that **Electric Vehicles (EVs)** achieve an average delivery time of **32.8 minutes**, compared to **32.1 minutes** for petrol motorcycles.
* Rider customer satisfaction ratings for EV riders (**4.62 / 5.0**) are on par with traditional motorbikes, validating Swiggy's transition toward 100% green fleet electrification without sacrificing speed.

### Finding 5: Quality Risk in High-Volume Restaurant Partners
* 7 restaurants across Bangalore, Mumbai, and Delhi were identified with high order volume (>75 orders) but sub-par customer ratings (<3.9).
* Analysis indicates these partners frequently delay order prep times by +12 minutes, directly driving customer delivery dissatisfaction.

---

## 3. Strategic Recommendations for Swiggy Leadership

| Area | Recommended Business Action | Projected Financial / Operational Impact |
| :--- | :--- | :--- |
| **Swiggy One Conversion** | Deploy targeted in-app nudges to users who place 3+ orders/month without Swiggy One, offering a 1-month discounted trial at ₹99. | +18% increase in Swiggy One conversion, boosting annual GMV by ~₹45 Lakhs. |
| **COD Surcharge / Disincentive** | Implement a nominal ₹10 convenience fee on Cash on Delivery (COD) orders or provide instant ₹15 cashback on UPI payments. | Reduce order cancellation rate from 5.5% to <2.5%, saving ~₹18 Lakhs in reverse logistics waste. |
| **Kitchen Prep SLA Monitoring** | Integrate a dynamic "Kitchen Delay Warning" for restaurants with ratings below 4.0 that delays rider dispatch by 6 minutes. | Reduce delivery partner idle waiting time by 15%, improving fleet utilization during dinner peaks. |
| **EV Fleet Incentives** | Offer delivery partners a ₹3/order green bonus for deliveries completed on Electric Vehicles. | Accelerate EV adoption from 15% to 40% within 12 months, cutting courier carbon footprint and fuel vulnerability. |
