import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS Styling (Swiggy Theme)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy Food Delivery — Executive Business Intelligence",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #F8FAFC;
    }
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #FC8019;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #1E293B;
        margin: 4px 0;
    }
    .metric-delta {
        font-size: 11px;
        color: #10B981;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #475569;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        color: #FC8019 !important;
        border-bottom-color: #FC8019 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Preparation
# -----------------------------------------------------------------------------
@st.cache_data
def load_swiggy_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    users = pd.read_csv(os.path.join(data_dir, "users.csv"))
    rests = pd.read_csv(os.path.join(data_dir, "restaurants.csv"))
    riders = pd.read_csv(os.path.join(data_dir, "delivery_partners.csv"))
    
    # Pre-process dates
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month_year"] = orders["order_date"].dt.strftime("%Y-%m")
    orders["hour"] = pd.to_datetime(orders["order_time"], format="%H:%M:%S").dt.hour
    
    # Merge context
    df = orders.merge(users[["user_id", "name", "city", "gender", "age", "is_swiggy_one"]], on="user_id", how="left")
    df = df.merge(rests[["restaurant_id", "restaurant_name", "cuisine", "rating", "cost_for_two"]], on="restaurant_id", how="left")
    df = df.merge(riders[["partner_id", "partner_name", "vehicle_type", "rating"]], on="partner_id", how="left", suffixes=("_rest", "_rider"))
    
    return df

df_raw = load_swiggy_data()

# -----------------------------------------------------------------------------
# 3. Interactive Sidebar Slicers & Filters
# -----------------------------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=160)
st.sidebar.markdown("### 🎛️ Interactive Filters")

# City Slicer
all_cities = sorted(df_raw["city"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("Select Cities", options=all_cities, default=all_cities)

# Swiggy One Membership Slicer
membership_opt = st.sidebar.radio("Customer Membership", options=["All Customers", "Swiggy One Only", "Regular Users Only"])

# Order Status Slicer
status_opt = st.sidebar.selectbox("Order Status", options=["Delivered Orders Only", "All Orders (Delivered + Cancelled)", "Cancelled Only"])

# Date Range Slicer
min_date = df_raw["order_date"].min().date()
max_date = df_raw["order_date"].max().date()
date_range = st.sidebar.date_input("Date Range (FY 2024)", value=[min_date, max_date], min_value=min_date, max_value=max_date)

# Apply Filters Dynamically
df_filtered = df_raw.copy()

if selected_cities:
    df_filtered = df_filtered[df_filtered["city"].isin(selected_cities)]

if membership_opt == "Swiggy One Only":
    df_filtered = df_filtered[df_filtered["is_swiggy_one"] == 1]
elif membership_opt == "Regular Users Only":
    df_filtered = df_filtered[df_filtered["is_swiggy_one"] == 0]

if status_opt == "Delivered Orders Only":
    df_filtered = df_filtered[df_filtered["order_status"] == "Delivered"]
elif status_opt == "Cancelled Only":
    df_filtered = df_filtered[df_filtered["order_status"] == "Cancelled"]

if len(date_range) == 2:
    start_d, end_d = date_range
    df_filtered = df_filtered[(df_filtered["order_date"].dt.date >= start_d) & (df_filtered["order_date"].dt.date <= end_d)]

st.sidebar.markdown("---")
st.sidebar.info(f"**Showing:** {len(df_filtered):,} of {len(df_raw):,} orders\n\n**Connected DB:** MySQL 8.0 (`swiggy_db`)")

# -----------------------------------------------------------------------------
# 4. Header & Dynamic KPI Metrics Bar
# -----------------------------------------------------------------------------
st.title("🛵 Swiggy Food Delivery & Business Intelligence")
st.caption("Live Executive Decision-Support System & Marketplace Analytics (FY 2024)")

# Calculate Real-Time Dynamic KPIs
total_orders = len(df_filtered)
total_gmv = df_filtered["total_amount"].sum()
delivered_orders = len(df_filtered[df_filtered["order_status"] == "Delivered"])
aov = (total_gmv / delivered_orders) if delivered_orders > 0 else 0
swiggy_one_orders = len(df_filtered[df_filtered["is_swiggy_one"] == 1])
swiggy_one_share = (swiggy_one_orders / total_orders * 100) if total_orders > 0 else 0
cancelled_count = len(df_filtered[df_filtered["order_status"] == "Cancelled"])
cancel_rate = (cancelled_count / total_orders * 100) if total_orders > 0 else 0
avg_deliv_time = df_filtered[df_filtered["order_status"] == "Delivered"]["delivery_time_mins"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total GMV (Sales)</div>
        <div class="metric-value">₹ {total_gmv/1e5:,.1f} L</div>
        <div class="metric-delta">₹ {total_gmv:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Delivered Orders</div>
        <div class="metric-value">{delivered_orders:,}</div>
        <div class="metric-delta">{(delivered_orders/total_orders*100 if total_orders else 0):.1f}% Fulfilled</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Order Value</div>
        <div class="metric-value">₹ {aov:.1f}</div>
        <div class="metric-delta">Per Delivered Order</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Swiggy One Share</div>
        <div class="metric-value">{swiggy_one_share:.1f}%</div>
        <div class="metric-delta">{swiggy_one_orders:,} Member Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Delivery Speed</div>
        <div class="metric-value">{avg_deliv_time:.1f} min</div>
        <div class="metric-delta">Target: ≤ 35 min</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Multi-Tab Visual Storytelling
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Revenue Pulse", 
    "👑 Swiggy One & Customer Loyalty", 
    "⏱️ Delivery Operations & Fleet SLAs"
])

# -----------------------------------------------------------------------------
# TAB 1: EXECUTIVE REVENUE PULSE
# -----------------------------------------------------------------------------
with tab1:
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("Monthly Revenue (GMV) Trend & Seasonality")
        monthly_df = df_filtered[df_filtered["order_status"] == "Delivered"].groupby("month_year").agg(
            GMV=("total_amount", "sum"),
            Orders=("order_id", "count")
        ).reset_index()
        
        if not monthly_df.empty:
            monthly_df["GMV_Lakhs"] = monthly_df["GMV"] / 1e5
            fig_monthly = px.bar(
                monthly_df, 
                x="month_year", 
                y="GMV_Lakhs",
                title="Gross Merchandise Value (₹ in Lakhs) by Month",
                labels={"month_year": "Month", "GMV_Lakhs": "GMV (₹ Lakhs)"},
                color_discrete_sequence=["#FC8019"]
            )
            fig_monthly.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.warning("No data matching current filters.")

    with col_chart2:
        st.subheader("Payment Gateway Channel Distribution")
        pay_df = df_filtered.groupby("payment_method").agg(
            Orders=("order_id", "count")
        ).reset_index()
        
        if not pay_df.empty:
            fig_pay = px.pie(
                pay_df, 
                names="payment_method", 
                values="Orders", 
                hole=0.45,
                color_discrete_sequence=["#FC8019", "#1F2937", "#3B82F6", "#EF4444", "#10B981"]
            )
            fig_pay.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_pay, use_container_width=True)

    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.subheader("City Revenue Performance (₹ Lakhs)")
        city_df = df_filtered[df_filtered["order_status"] == "Delivered"].groupby("city").agg(
            GMV=("total_amount", "sum")
        ).reset_index().sort_values(by="GMV", ascending=True)
        
        if not city_df.empty:
            city_df["GMV_Lakhs"] = city_df["GMV"] / 1e5
            fig_city = px.bar(
                city_df, 
                x="GMV_Lakhs", 
                y="city", 
                orientation="h",
                color_discrete_sequence=["#1F2937"],
                labels={"city": "City", "GMV_Lakhs": "GMV (₹ Lakhs)"}
            )
            fig_city.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_city, use_container_width=True)

    with col_chart4:
        st.subheader("Top Cuisines by Order Volume")
        cuisine_df = df_filtered[df_filtered["order_status"] == "Delivered"].groupby("cuisine").agg(
            Orders=("order_id", "count")
        ).reset_index().sort_values(by="Orders", ascending=False).head(7)
        
        if not cuisine_df.empty:
            fig_cuisine = px.bar(
                cuisine_df, 
                x="cuisine", 
                y="Orders", 
                color_discrete_sequence=["#FC8019"],
                labels={"cuisine": "Cuisine", "Orders": "Total Delivered Orders"}
            )
            fig_cuisine.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_cuisine, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: SWIGGY ONE & CUSTOMER LOYALTY
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Swiggy One vs. Regular Customers: Commercial Unit Economics")
    
    delivered_df = df_filtered[df_filtered["order_status"] == "Delivered"]
    comp_df = delivered_df.groupby("is_swiggy_one").agg(
        Customers=("user_id", "nunique"),
        Total_Orders=("order_id", "count"),
        Total_GMV=("total_amount", "sum"),
        AOV=("total_amount", "mean"),
        Avg_Discount=("discount_amount", "mean"),
        Avg_Delivery_Fee=("delivery_fee", "mean")
    ).reset_index()
    
    comp_df["Tier"] = comp_df["is_swiggy_one"].map({1: "Swiggy One Member", 0: "Regular Customer"})
    comp_df["Orders_Per_User"] = comp_df["Total_Orders"] / comp_df["Customers"]
    
    st.dataframe(
        comp_df[["Tier", "Customers", "Total_Orders", "Orders_Per_User", "Total_GMV", "AOV", "Avg_Discount", "Avg_Delivery_Fee"]].style.format({
            "Customers": "{:,}",
            "Total_Orders": "{:,}",
            "Orders_Per_User": "{:.1f}",
            "Total_GMV": "₹ {:,.0f}",
            "AOV": "₹ {:.1f}",
            "Avg_Discount": "₹ {:.1f}",
            "Avg_Delivery_Fee": "₹ {:.1f}"
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    col_rfm1, col_rfm2 = st.columns([1, 2])
    
    with col_rfm1:
        st.subheader("Customer Frequency Tiers")
        user_orders = delivered_df.groupby(["user_id", "is_swiggy_one"]).agg(
            orders=("order_id", "count"),
            spend=("total_amount", "sum")
        ).reset_index()
        
        def assign_tier(c):
            if c >= 25: return "Power User (25+)"
            elif c >= 12: return "Frequent Eater (12-24)"
            elif c >= 5: return "Regular (5-11)"
            else: return "Occasional (1-4)"
            
        user_orders["Frequency_Tier"] = user_orders["orders"].apply(assign_tier)
        rfm_summary = user_orders.groupby("Frequency_Tier")["spend"].sum().reset_index()
        
        fig_rfm = px.pie(
            rfm_summary, 
            names="Frequency_Tier", 
            values="spend", 
            color_discrete_sequence=["#FC8019", "#FB923C", "#FDBA74", "#FED7AA"]
        )
        fig_rfm.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_rfm, use_container_width=True)
        
    with col_rfm2:
        st.subheader("VIP Customer Cohort (Top Spenders)")
        top_users = delivered_df.groupby(["user_id", "name", "city", "is_swiggy_one"]).agg(
            Total_Orders=("order_id", "count"),
            Total_Spend=("total_amount", "sum"),
            Avg_Spend=("total_amount", "mean")
        ).reset_index().sort_values(by="Total_Spend", ascending=False).head(10)
        
        top_users["Swiggy_One"] = top_users["is_swiggy_one"].map({1: "Yes", 0: "No"})
        
        st.dataframe(
            top_users[["user_id", "name", "city", "Swiggy_One", "Total_Orders", "Total_Spend", "Avg_Spend"]].style.format({
                "Total_Orders": "{:,}",
                "Total_Spend": "₹ {:,.0f}",
                "Avg_Spend": "₹ {:.1f}"
            }),
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# TAB 3: DELIVERY OPERATIONS & FLEET SLAS
# -----------------------------------------------------------------------------
with tab3:
    col_deliv1, col_deliv2 = st.columns(2)
    
    with col_deliv1:
        st.subheader("Average Delivery Time by City (Minutes)")
        city_speed = delivered_df.groupby("city")["delivery_time_mins"].mean().reset_index().sort_values(by="delivery_time_mins", ascending=False)
        fig_speed = px.bar(
            city_speed, 
            x="city", 
            y="delivery_time_mins", 
            labels={"delivery_time_mins": "Avg Minutes", "city": "City"},
            color_discrete_sequence=["#3B82F6"]
        )
        fig_speed.add_hline(y=35, line_dash="dash", line_color="#EF4444", annotation_text="35-Min SLA Target")
        fig_speed.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_speed, use_container_width=True)
        
    with col_deliv2:
        st.subheader("Electric Vehicles (EV) vs. Petrol Fleet Comparison")
        fleet_df = delivered_df.groupby("vehicle_type").agg(
            Deliveries=("order_id", "count"),
            Avg_Duration=("delivery_time_mins", "mean"),
            Rider_Rating=("rating_rider", "mean")
        ).reset_index()
        
        fig_fleet = px.bar(
            fleet_df, 
            x="vehicle_type", 
            y="Avg_Duration", 
            color="vehicle_type",
            color_discrete_map={"Electric Vehicle (EV)": "#10B981", "Motorcycle": "#1F2937", "Scooter": "#FC8019"},
            labels={"Avg_Duration": "Avg Delivery (Mins)"}
        )
        fig_fleet.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
        st.plotly_chart(fig_fleet, use_container_width=True)

    st.markdown("---")
    st.subheader("⚠️ Quality Risk Monitoring: High Volume / Rating < 4.0 Restaurants")
    
    rest_risk = delivered_df.groupby(["restaurant_name", "city", "cuisine", "rating_rest"]).agg(
        Orders_Fulfilled=("order_id", "count"),
        Total_GMV=("total_amount", "sum"),
        Avg_Delivery=("delivery_time_mins", "mean")
    ).reset_index()
    
    risk_alert = rest_risk[(rest_risk["Orders_Fulfilled"] >= 50) & (rest_risk["rating_rest"] < 4.0)].sort_values(by="Orders_Fulfilled", ascending=False)
    
    if not risk_alert.empty:
        st.dataframe(
            risk_alert.style.format({
                "rating_rest": "{:.1f} ★",
                "Orders_Fulfilled": "{:,}",
                "Total_GMV": "₹ {:,.0f}",
                "Avg_Delivery": "{:.1f} min"
            }),
            use_container_width=True
        )
    else:
        st.success("No high-volume restaurants with sub-4.0 ratings detected under current filter selection.")
