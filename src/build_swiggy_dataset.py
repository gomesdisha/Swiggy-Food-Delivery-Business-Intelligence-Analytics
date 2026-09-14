"""
Swiggy Food Delivery & Business Intelligence Analytics
Dataset Builder using Actual Web-Scraped Swiggy Data

1. Fetches real scraped Swiggy restaurant data from GitHub (covering Bangalore, Mumbai, Delhi, Hyderabad, Pune, Kolkata, Chennai).
2. Fetches real scraped Swiggy menu items with authentic prices and dish names.
3. Generates realistic user base, delivery partners, and transaction order history linked directly to real restaurants and real dishes.
"""

import os
import random
import datetime
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

print("=" * 60)
print("Step 1: Downloading & Processing Real Scraped Swiggy Data...")
print("=" * 60)

# URLs for real scraped Swiggy datasets
RESTAURANTS_URL = "https://raw.githubusercontent.com/shashanksingh1717/Swiggy-database/main/database.csv"
MENU_URL = "https://raw.githubusercontent.com/SelvaJenner/SQL_Swiggy-Restaurant-Analysis-and-Insights/main/Swiggy.csv"

# Load restaurants
print("Loading real Swiggy restaurants...")
raw_rests = pd.read_csv(RESTAURANTS_URL)
# Target top metro cities
TARGET_CITIES = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Kolkata", "Chennai"]
filtered_rests = raw_rests[raw_rests["city"].isin(TARGET_CITIES)].copy()

# Clean cost column (remove non-numeric chars if any)
filtered_rests["cost"] = pd.to_numeric(filtered_rests["cost"].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(400)
# Clean rating
filtered_rests["rating"] = pd.to_numeric(filtered_rests["rating"], errors="coerce").fillna(4.1)
# Drop duplicates by name and city
filtered_rests = filtered_rests.drop_duplicates(subset=["name", "city"])

# Sample top 20-30 iconic / high-rated restaurants per city (total ~150 restaurants)
city_samples = []
for c in TARGET_CITIES:
    c_df = filtered_rests[filtered_rests["city"] == c]
    # Sort by rating and pick top 25
    sample = c_df.sort_values(by="rating", ascending=False).head(25)
    city_samples.append(sample)

curated_rests = pd.concat(city_samples, ignore_index=True)
curated_rests["restaurant_id"] = range(101, 101 + len(curated_rests))

restaurants_final = curated_rests[[
    "restaurant_id", "name", "city", "cuisine", "rating", "rating_count", "cost", "link"
]].rename(columns={
    "name": "restaurant_name",
    "cost": "cost_for_two",
    "link": "swiggy_url"
})

restaurants_csv_path = os.path.join(DATA_DIR, "restaurants.csv")
restaurants_final.to_csv(restaurants_csv_path, index=False)
print(f"-> Saved {len(restaurants_final)} real restaurants to {restaurants_csv_path}")

# Load real menu items
print("\nLoading real scraped Swiggy menu items...")
raw_menu = pd.read_csv(MENU_URL, usecols=["menu_category", "item", "price", "veg_or_non-veg"])
raw_menu = raw_menu.dropna().drop_duplicates(subset=["item"])
# Clean price
raw_menu["price"] = pd.to_numeric(raw_menu["price"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
raw_menu = raw_menu[(raw_menu["price"] >= 25) & (raw_menu["price"] <= 900)]
raw_menu = raw_menu.rename(columns={
    "item": "item_name",
    "veg_or_non-veg": "veg_or_non_veg"
})

# Standardize veg tag
raw_menu["veg_or_non_veg"] = raw_menu["veg_or_non_veg"].apply(lambda x: "Non-veg" if "non" in str(x).lower() else "Veg")

# Sample ~1000 authentic menu items
menu_final = raw_menu.sample(n=min(1200, len(raw_menu)), random_state=42).copy()
menu_final["item_id"] = range(1, 1 + len(menu_final))
menu_final = menu_final[["item_id", "item_name", "menu_category", "price", "veg_or_non_veg"]]

menu_csv_path = os.path.join(DATA_DIR, "menu_items.csv")
menu_final.to_csv(menu_csv_path, index=False)
print(f"-> Saved {len(menu_final)} real menu items to {menu_csv_path}")

print("\n" + "=" * 60)
print("Step 2: Synthesizing Realistic Users & Delivery Partners...")
print("=" * 60)

FIRST_NAMES_M = ["Rahul", "Amit", "Rohan", "Aditya", "Vikram", "Kunal", "Abhishek", "Suresh", "Arjun", "Karthik", "Deepak", "Nikhil", "Pranav", "Varun", "Manish", "Gaurav", "Siddharth", "Vishal", "Anand", "Rakesh", "Tanmay", "Ayush", "Harsh", "Mayank"]
FIRST_NAMES_F = ["Priya", "Ananya", "Sneha", "Pooja", "Neha", "Divya", "Ritu", "Swati", "Aishwarya", "Shruti", "Tanvi", "Megha", "Shreya", "Kavya", "Deepika", "Aditi", "Pallavi", "Simran", "Nandini", "Anushka", "Isha", "Rhea", "Komal", "Bhavna"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Gupta", "Iyer", "Reddy", "Rao", "Nair", "Mehta", "Joshi", "Singh", "Das", "Bose", "Kulkarni", "Deshmukh", "Chopra", "Malhotra", "Mukherjee", "Sen", "Bhat", "Nambiar", "Pillai", "Choudhury"]

# Users (1,000 customers)
USERS_COUNT = 1000
users_data = []
start_signup = datetime.date(2023, 1, 1)
end_signup = datetime.date(2024, 6, 30)
signup_days_range = (end_signup - start_signup).days

for u_id in range(1, USERS_COUNT + 1):
    gender = random.choice(["Male", "Female"])
    first_name = random.choice(FIRST_NAMES_M) if gender == "Male" else random.choice(FIRST_NAMES_F)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    city = random.choice(TARGET_CITIES)
    age = random.randint(19, 52)
    signup_days = random.randint(0, signup_days_range)
    signup_date = start_signup + datetime.timedelta(days=signup_days)
    is_swiggy_one = 1 if random.random() < 0.36 else 0
    
    users_data.append({
        "user_id": 1000 + u_id,
        "name": name,
        "gender": gender,
        "age": age,
        "city": city,
        "signup_date": signup_date.isoformat(),
        "is_swiggy_one": is_swiggy_one
    })

users_df = pd.DataFrame(users_data)
users_csv_path = os.path.join(DATA_DIR, "users.csv")
users_df.to_csv(users_csv_path, index=False)
print(f"-> Saved {len(users_df)} users to {users_csv_path}")

# Delivery Partners (120 riders)
RIDERS_COUNT = 120
riders_data = []
for r_id in range(1, RIDERS_COUNT + 1):
    first_name = random.choice(FIRST_NAMES_M)
    last_name = random.choice(LAST_NAMES)
    rider_name = f"{first_name} {last_name}"
    city = random.choice(TARGET_CITIES)
    vehicle_type = random.choices(["Motorcycle", "Scooter", "Electric Vehicle (EV)"], weights=[0.55, 0.30, 0.15])[0]
    rating = round(random.uniform(4.0, 4.95), 1)
    
    riders_data.append({
        "partner_id": 500 + r_id,
        "partner_name": rider_name,
        "city": city,
        "vehicle_type": vehicle_type,
        "rating": rating
    })

riders_df = pd.DataFrame(riders_data)
riders_csv_path = os.path.join(DATA_DIR, "delivery_partners.csv")
riders_df.to_csv(riders_csv_path, index=False)
print(f"-> Saved {len(riders_df)} delivery partners to {riders_csv_path}")

print("\n" + "=" * 60)
print("Step 3: Simulating Orders & Order Items from Real Menus...")
print("=" * 60)

# Pre-map restaurants and riders by city
rests_by_city = {c: restaurants_final[restaurants_final["city"] == c].to_dict("records") for c in TARGET_CITIES}
riders_by_city = {c: riders_df[riders_df["city"] == c]["partner_id"].tolist() for c in TARGET_CITIES}
users_list = users_df.to_dict("records")
menu_items_list = menu_final.to_dict("records")

# Categorize menu items for realistic basket selection
mains = [item for item in menu_items_list if any(w in str(item["menu_category"]).lower() for w in ["main", "rice", "biryani", "noodles", "curry", "thali"])]
starters_breads = [item for item in menu_items_list if any(w in str(item["menu_category"]).lower() for w in ["starter", "bread", "roti", "naan", "paratha", "snack", "chaat", "accompaniment"])]
desserts_drinks = [item for item in menu_items_list if any(w in str(item["menu_category"]).lower() for w in ["dessert", "sweet", "beverage", "drink", "shake", "ice cream"])]

if not mains: mains = menu_items_list[:400]
if not starters_breads: starters_breads = menu_items_list[400:800]
if not desserts_drinks: desserts_drinks = menu_items_list[800:]

ORDERS_COUNT = 15000
orders_data = []
order_items_data = []

start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 12, 31)
date_range_days = (end_date - start_date).days

# Monthly seasonality weights (IPL peak, Monsoon delivery surge, Festive peak)
SEASONALITY_WEIGHTS = {
    1: 0.95, 2: 0.92, 3: 0.98,
    4: 1.14, 5: 1.18, # IPL Season
    6: 0.96, 7: 0.95, 8: 0.94, # Monsoon
    9: 1.02, 10: 1.20, 11: 1.22, # Diwali / Festive
    12: 1.16 # New Year
}

order_item_pk = 1

for o_idx in range(1, ORDERS_COUNT + 1):
    order_id = 200000 + o_idx
    
    # Select user
    user = random.choice(users_list)
    user_city = user["city"]
    is_one = user["is_swiggy_one"]
    
    # Select restaurant in the same city
    possible_rests = rests_by_city[user_city]
    restaurant = random.choice(possible_rests)
    r_id = restaurant["restaurant_id"]
    
    # Select rider in the same city
    r_riders = riders_by_city[user_city]
    rider_id = random.choice(r_riders) if r_riders else None
    
    # Date generation with seasonality
    while True:
        d_offset = random.randint(0, date_range_days)
        ord_date = start_date + datetime.timedelta(days=d_offset)
        m_weight = SEASONALITY_WEIGHTS[ord_date.month]
        if random.random() < (m_weight / 1.25):
            break
            
    # Order time distribution (Lunch 35%, Dinner 48%, Evening/Late 17%)
    slot_rand = random.random()
    if slot_rand < 0.35:
        hour = random.randint(12, 14)
    elif slot_rand < 0.83:
        hour = random.randint(19, 22)
    else:
        hour = random.choice([15, 16, 17, 18, 23, 0])
    minute = random.randint(0, 59)
    order_time = f"{hour:02d}:{minute:02d}:00"
    
    # Basket items selection (1 Main + optional starter/bread + optional dessert/drink)
    basket = [random.choice(mains)]
    if random.random() < 0.65:
        basket.append(random.choice(starters_breads))
    if random.random() < 0.35:
        basket.append(random.choice(desserts_drinks))
    if random.random() < 0.15:
        basket.append(random.choice(starters_breads))
        
    gross_items_amount = 0
    for item in basket:
        qty = random.choices([1, 2, 3], weights=[0.82, 0.15, 0.03])[0]
        item_price = int(item["price"])
        line_total = item_price * qty
        gross_items_amount += line_total
        
        order_items_data.append({
            "order_item_id": order_item_pk,
            "order_id": order_id,
            "item_id": item["item_id"],
            "item_name": item["item_name"],
            "price": item_price,
            "quantity": qty,
            "line_total": line_total
        })
        order_item_pk += 1
        
    # Delivery fee logic: Swiggy One gets Free Delivery on orders >= 149
    if is_one and gross_items_amount >= 149:
        delivery_fee = 0
    else:
        delivery_fee = random.choice([30, 35, 45, 50])
        
    # Discounts: Swiggy One gets special member discount (12-20%), regular gets 0-10%
    if is_one:
        discount_amount = int(min(gross_items_amount * random.uniform(0.12, 0.22), 120))
    else:
        discount_amount = int(min(gross_items_amount * random.uniform(0.00, 0.12), 60)) if random.random() < 0.50 else 0
        
    total_amount = max(gross_items_amount - discount_amount + delivery_fee, 50)
    
    # Order status: 94.5% Delivered, 5.5% Cancelled
    order_status = "Delivered" if random.random() < 0.945 else "Cancelled"
    
    # Delivery duration (mins)
    base_mins = random.gauss(31, 6)
    if ord_date.month in [7, 8]:
        base_mins += 6 # Monsoon delay
    if hour in [19, 20, 21]:
        base_mins += 4 # Dinner peak rush
    delivery_time_mins = int(max(min(base_mins, 75), 18)) if order_status == "Delivered" else None
    
    # Payment method (UPI dominant in India)
    payment_method = random.choices(
        ["UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"],
        weights=[0.63, 0.19, 0.08, 0.07, 0.03]
    )[0]
    
    orders_data.append({
        "order_id": order_id,
        "user_id": user["user_id"],
        "restaurant_id": r_id,
        "partner_id": rider_id,
        "order_date": ord_date.isoformat(),
        "order_time": order_time,
        "order_status": order_status,
        "total_amount": total_amount,
        "discount_amount": discount_amount,
        "delivery_fee": delivery_fee,
        "delivery_time_mins": delivery_time_mins,
        "payment_method": payment_method
    })

orders_df = pd.DataFrame(orders_data)
orders_csv_path = os.path.join(DATA_DIR, "orders.csv")
orders_df.to_csv(orders_csv_path, index=False)
print(f"-> Saved {len(orders_df)} orders to {orders_csv_path}")

order_items_df = pd.DataFrame(order_items_data)
order_items_csv_path = os.path.join(DATA_DIR, "order_items.csv")
order_items_df.to_csv(order_items_csv_path, index=False)
print(f"-> Saved {len(order_items_df)} order items to {order_items_csv_path}")

print("\n" + "=" * 60)
print("SUCCESS: 5 Relational Tables Generated Cleanly with Real Scraped Swiggy Data!")
print("=" * 60)
