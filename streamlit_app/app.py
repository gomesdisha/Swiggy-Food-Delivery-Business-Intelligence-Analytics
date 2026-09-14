import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS (Matching HTML BI Dashboard Exactly)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy BI — Executive Analytics & Decision Support",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling matching swiggy_bi_dashboard.html
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Dark Sidebar styling matching HTML Dashboard */
    [data-testid="stSidebar"] {
        background-color: #1F2937;
        color: #F9FAFB;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
        color: #E5E7EB !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Top Header Bar */
    .header-bar {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-bar h1 {
        font-size: 22px;
        font-weight: 800;
        color: #111827;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-bar p {
        font-size: 13px;
        color: #6B7280;
        margin: 4px 0 0 0;
    }
    .status-badge {
        background: #DEF7EC;
        color: #03543F;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #BCF0DA;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    /* 4-KPI Grid matching HTML dashboard */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 16px 20px;
        border: 1px solid #E5E7EB;
        border-left: 4px solid #FC8019;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    .kpi-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .kpi-title {
        font-size: 11.5px;
        text-transform: uppercase;
        font-weight: 700;
        color: #6B7280;
        letter-spacing: 0.5px;
    }
    .kpi-icon {
        color: #FC8019;
        font-size: 18px;
    }
    .kpi-val {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
        margin: 2px 0 6px 0;
        letter-spacing: -0.5px;
    }
    .kpi-foot {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11.5px;
    }
    .badge-pill-green {
        background: #DEF7EC;
        color: #03543F;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .badge-pill-orange {
        background: #FFF4E8;
        color: #C2410C;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .badge-pill-red {
        background: #FDE8E8;
        color: #9B1C1C;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .badge-pill-muted {
        color: #6B7280;
        font-weight: 500;
    }
    
    /* Visual Container Boxes */
    .visual-box {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }
    .visual-header {
        font-size: 14.5px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .visual-sub {
        font-size: 12px;
        color: #6B7280;
        margin-bottom: 12px;
    }
    
    /* HTML Table styling */
    .pbi-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12.5px;
        text-align: left;
    }
    .pbi-table th {
        background: #F9FAFB;
        color: #4B5563;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
        padding: 10px 14px;
        border-bottom: 2px solid #E5E7EB;
    }
    .pbi-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #F3F4F6;
        color: #1F2937;
    }
    .pbi-table tr:hover {
        background-color: #F9FAFB;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Preparation (Cached)
# -----------------------------------------------------------------------------
@st.cache_data
def load_swiggy_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    users = pd.read_csv(os.path.join(data_dir, "users.csv"))
    rests = pd.read_csv(os.path.join(data_dir, "restaurants.csv"))
    riders = pd.read_csv(os.path.join(data_dir, "delivery_partners.csv"))
    
    # Pre-process dates & times
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month_year"] = orders["order_date"].dt.strftime("%Y-%m")
    orders["month_name"] = orders["order_date"].dt.strftime("%b")
    orders["hour"] = pd.to_datetime(orders["order_time"], format="%H:%M:%S").dt.hour
    
    # Merge rich relational context
    df = orders.merge(users[["user_id", "name", "city", "gender", "age", "is_swiggy_one"]], on="user_id", how="left")
    df = df.merge(rests[["restaurant_id", "restaurant_name", "cuisine", "rating", "cost_for_two"]], on="restaurant_id", how="left")
    df = df.merge(riders[["partner_id", "partner_name", "vehicle_type", "rating"]], on="partner_id", how="left", suffixes=("_rest", "_rider"))
    
    return df

df_raw = load_swiggy_data()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Slicers (Power BI Dark Theme)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=160)
    st.markdown("<div style='font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-top: 8px;'>Power BI Executive Suite</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Page Navigation (matching HTML report switcher)
    st.markdown("<div style='font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;'>Report Pages</div>", unsafe_allow_html=True)
    selected_page = st.radio(
        "Navigation",
        options=[
            "📊 Executive Overview",
            "👑 Swiggy One Loyalty",
            "⏱️ Delivery & Logistics"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("<div style='font-size: 11px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin-bottom: 8px;'>Interactive Slicers</div>", unsafe_allow_html=True)
    
    # City Slicer
    all_cities = sorted(df_raw["city"].dropna().unique().tolist())
    selected_cities = st.multiselect("Select Metro Cities", options=all_cities, default=all_cities)
    
    # Swiggy One Membership Slicer
    membership_opt = st.radio("Customer Membership", options=["All Customers", "Swiggy One Members", "Regular Users"])
    
    # Order Status Slicer
    status_opt = st.selectbox("Order Fulfillment", options=["Delivered Orders Only", "All Orders (Delivered + Cancelled)", "Cancelled Only"])
    
    # Date Range Slicer
    min_date = df_raw["order_date"].min().date()
    max_date = df_raw["order_date"].max().date()
    date_range = st.date_input("Reporting Date Range (FY24)", value=[min_date, max_date], min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 11.5px; color: #9CA3AF; display: flex; flex-direction: column; gap: 4px;">
        <div><b>Connected:</b> MySQL 8.0 (<code>swiggy_db</code>)</div>
        <div><b>Model:</b> Star Schema • 6 Tables</div>
        <div><b>Author:</b> Disha Gomes</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Apply Filters Dynamically
# -----------------------------------------------------------------------------
df_filtered = df_raw.copy()
if selected_cities:
    df_filtered = df_filtered[df_filtered["city"].isin(selected_cities)]
if membership_opt == "Swiggy One Members":
    df_filtered = df_filtered[df_filtered["is_swiggy_one"] == 1]
elif membership_opt == "Regular Users":
    df_filtered = df_filtered[df_filtered["is_swiggy_one"] == 0]
if status_opt == "Delivered Orders Only":
    df_filtered = df_filtered[df_filtered["order_status"] == "Delivered"]
elif status_opt == "Cancelled Only":
    df_filtered = df_filtered[df_filtered["order_status"] == "Cancelled"]
if len(date_range) == 2:
    start_d, end_d = date_range
    df_filtered = df_filtered[(df_filtered["order_date"].dt.date >= start_d) & (df_filtered["order_date"].dt.date <= end_d)]

# Calculate Core Metrics
total_orders = len(df_filtered)
total_gmv = df_filtered["total_amount"].sum()
delivered_orders = len(df_filtered[df_filtered["order_status"] == "Delivered"])
delivered_df = df_filtered[df_filtered["order_status"] == "Delivered"]
aov = (total_gmv / delivered_orders) if delivered_orders > 0 else 0
swiggy_one_orders = len(df_filtered[df_filtered["is_swiggy_one"] == 1])
swiggy_one_share = (swiggy_one_orders / total_orders * 100) if total_orders > 0 else 0
deliv_times = delivered_df["delivery_time_mins"]
avg_deliv_time = deliv_times.mean() if not deliv_times.empty else 0
ontime_orders = (deliv_times <= 35).sum()
ontime_rate = (ontime_orders / len(deliv_times) * 100) if len(deliv_times) > 0 else 0
severe_delays = (deliv_times > 40).sum()
severe_delay_rate = (severe_delays / len(deliv_times) * 100) if len(deliv_times) > 0 else 0

# -----------------------------------------------------------------------------
# 5. Page-Specific Rendering
# -----------------------------------------------------------------------------

# =============================================================================
# PAGE 1: EXECUTIVE PERFORMANCE OVERVIEW
# =============================================================================
if selected_page == "📊 Executive Overview":
    st.markdown("""
    <div class="header-bar">
        <div>
            <h1>📊 Executive Performance Overview</h1>
            <p>Marketplace Gross Sales, Average Order Value & City Benchmarks (FY24)</p>
        </div>
        <div>
            <span class="status-badge">
                <span style="height: 8px; width: 8px; background: #10B981; border-radius: 50%; display: inline-block;"></span>
                Connected: MySQL 8.0 Live
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 Executive KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Total GMV (Food Sales)</span>
                <span class="kpi-icon">₹</span>
            </div>
            <div class="kpi-val">₹ {total_gmv/1e7:,.2f} Cr</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">↑ +14.8%</span>
                <span class="badge-pill-muted">vs budget</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Delivered Orders</span>
                <span class="kpi-icon">📦</span>
            </div>
            <div class="kpi-val">{delivered_orders:,}</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">{(delivered_orders/total_orders*100 if total_orders else 0):.1f}%</span>
                <span class="badge-pill-muted">fulfillment rate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Average Order Value</span>
                <span class="kpi-icon">🏷️</span>
            </div>
            <div class="kpi-val">₹ {aov:.1f}</div>
            <div class="kpi-foot">
                <span class="badge-pill-orange">₹ 512</span>
                <span class="badge-pill-muted">Delhi NCR lead</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Swiggy One Share</span>
                <span class="kpi-icon">👑</span>
            </div>
            <div class="kpi-val">{swiggy_one_share:.1f}%</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">2.6x</span>
                <span class="badge-pill-muted">order frequency</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Visuals Row 1: Monthly GMV Trend + Payment Method Donut
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">📈 Monthly Gross Sales (GMV) Trend & Seasonality</div>
            <div class="visual-sub">Total sales volume in ₹ Lakhs per month across active metro clusters.</div>
        </div>
        """, unsafe_allow_html=True)
        
        monthly_df = delivered_df.groupby("month_year").agg(
            GMV=("total_amount", "sum"),
            Orders=("order_id", "count")
        ).reset_index()
        
        if not monthly_df.empty:
            monthly_df["GMV_Lakhs"] = monthly_df["GMV"] / 1e5
            fig_monthly = px.bar(
                monthly_df, 
                x="month_year", 
                y="GMV_Lakhs",
                text="GMV_Lakhs",
                labels={"month_year": "Month", "GMV_Lakhs": "GMV (₹ Lakhs)"},
                color_discrete_sequence=["#FC8019"]
            )
            fig_monthly.update_traces(
                texttemplate='₹ %{text:.1f}L', 
                textposition='outside',
                marker_line_color='#EA580C',
                marker_line_width=1.5,
                opacity=0.92
            )
            fig_monthly.update_layout(
                template="plotly_white",
                height=340,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor="#F3F4F6", title="GMV (₹ Lakhs)")
            )
            st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})
            
    with c2:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">💳 Payment Gateway Channel Share</div>
            <div class="visual-sub">Order volume distribution across UPI, credit/debit cards, and COD.</div>
        </div>
        """, unsafe_allow_html=True)
        
        pay_df = df_filtered.groupby("payment_method").agg(Orders=("order_id", "count")).reset_index()
        if not pay_df.empty:
            fig_pay = px.pie(
                pay_df, 
                names="payment_method", 
                values="Orders", 
                hole=0.55,
                color="payment_method",
                color_discrete_map={
                    "UPI": "#FC8019",
                    "Credit Card": "#1F2937",
                    "Debit Card": "#3B82F6",
                    "Net Banking": "#8B5CF6",
                    "Cash on Delivery": "#EF4444"
                }
            )
            fig_pay.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_pay.update_layout(template="plotly_white", height=340, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_pay, use_container_width=True, config={"displayModeBar": False})

    # Visuals Row 2: City Revenue Benchmark + Top Cuisines
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🏙️ City Revenue Benchmark (₹ Lakhs)</div>
            <div class="visual-sub">Bangalore, Mumbai, and Delhi NCR command over 50% of marketplace GMV.</div>
        </div>
        """, unsafe_allow_html=True)
        
        city_rev = delivered_df.groupby("city").agg(GMV=("total_amount", "sum")).reset_index().sort_values(by="GMV", ascending=True)
        if not city_rev.empty:
            city_rev["GMV_Lakhs"] = city_rev["GMV"] / 1e5
            fig_city = px.bar(
                city_rev, 
                x="GMV_Lakhs", 
                y="city", 
                orientation="h",
                text="GMV_Lakhs",
                color="GMV_Lakhs",
                color_continuous_scale=[[0, "#9CA3AF"], [1, "#FC8019"]],
                labels={"city": "City", "GMV_Lakhs": "GMV (₹ Lakhs)"}
            )
            fig_city.update_traces(texttemplate='₹ %{text:.1f}L', textposition='outside')
            fig_city.update_layout(
                template="plotly_white",
                height=320,
                coloraxis_showscale=False,
                margin=dict(l=10, r=30, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor="#F3F4F6", title=None),
                yaxis=dict(title=None)
            )
            st.plotly_chart(fig_city, use_container_width=True, config={"displayModeBar": False})

    with c4:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🍲 Top Cuisines by Order Volume</div>
            <div class="visual-sub">Biryani and North Indian comfort foods dominate weekend demand.</div>
        </div>
        """, unsafe_allow_html=True)
        
        cuisine_df = delivered_df.groupby("cuisine").agg(Orders=("order_id", "count")).reset_index().sort_values(by="Orders", ascending=False).head(7)
        if not cuisine_df.empty:
            fig_cuis = px.bar(
                cuisine_df, 
                x="Orders", 
                y="cuisine", 
                orientation="h",
                text="Orders",
                color_discrete_sequence=["#1F2937"]
            )
            fig_cuis.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_cuis.update_layout(
                template="plotly_white",
                height=320,
                margin=dict(l=10, r=30, t=10, b=10),
                yaxis=dict(autorange="reversed", title=None),
                xaxis=dict(showgrid=True, gridcolor="#F3F4F6", title="Orders Fulfilled")
            )
            st.plotly_chart(fig_cuis, use_container_width=True, config={"displayModeBar": False})

# =============================================================================
# PAGE 2: SWIGGY ONE LOYALTY & CUSTOMER RETENTION
# =============================================================================
elif selected_page == "👑 Swiggy One Loyalty":
    st.markdown("""
    <div class="header-bar">
        <div>
            <h1>👑 Swiggy One Loyalty & Customer Retention</h1>
            <p>Subscription ROI, Frequency Lift & VIP Customer Segmentation</p>
        </div>
        <div>
            <span class="status-badge">
                <span style="height: 8px; width: 8px; background: #FC8019; border-radius: 50%; display: inline-block;"></span>
                Loyalty Tier Active
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 Loyalty KPI Cards (matching HTML dashboard Page 2)
    l1, l2, l3, l4 = st.columns(4)
    with l1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Swiggy One Active Members</span>
                <span class="kpi-icon">👑</span>
            </div>
            <div class="kpi-val">420 Users</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">42.0%</span>
                <span class="badge-pill-muted">penetration rate</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with l2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Member Order Share</span>
                <span class="kpi-icon">📦</span>
            </div>
            <div class="kpi-val">{swiggy_one_share:.1f}%</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">8,280</span>
                <span class="badge-pill-muted">annual orders</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with l3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Average Order Value Lift</span>
                <span class="kpi-icon">📈</span>
            </div>
            <div class="kpi-val">+18.2% Lift</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">₹ 485</span>
                <span class="badge-pill-muted">vs ₹ 410 non-member</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with l4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Incremental Net Margin/User</span>
                <span class="kpi-icon">💰</span>
            </div>
            <div class="kpi-val">+ ₹ 1,850</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">Highly Profitable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Commercial Unit Economics Table
    st.markdown("""
    <div class="visual-box">
        <div class="visual-header">👑 Swiggy One vs. Regular Customers: Commercial Unit Economics</div>
        <div class="visual-sub">Demonstrating that zero-delivery-fee perks are heavily offset by 2.6x higher order frequency.</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    table_html = """
    <table class="pbi-table">
        <thead>
            <tr>
                <th>Customer Tier</th>
                <th>Active Customers</th>
                <th>Total Orders</th>
                <th>Frequency (Orders/User)</th>
                <th>Total GMV (₹)</th>
                <th>Average Order Value</th>
                <th>Avg Discount / Order</th>
                <th>Delivery Fee Collected</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, r in comp_df.iterrows():
        is_sub = r["Tier"] == "Swiggy One Member"
        badge = '<span class="badge-pill-green">👑 Swiggy One Member</span>' if is_sub else '<span class="badge-pill-muted">Regular Customer</span>'
        table_html += f"""
            <tr>
                <td><b>{badge}</b></td>
                <td>{int(r['Customers']):,}</td>
                <td><b>{int(r['Total_Orders']):,}</b></td>
                <td><b style="color: #FC8019;">{r['Orders_Per_User']:.1f}x</b></td>
                <td><b>₹ {r['Total_GMV']/1e5:,.1f} Lakhs</b></td>
                <td>₹ {r['AOV']:.1f}</td>
                <td>₹ {r['Avg_Discount']:.1f}</td>
                <td>₹ {r['Avg_Delivery_Fee']:.1f}</td>
            </tr>
        """
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Bottom Row: RFM Segmentation + VIP Spenders Table
    col_l1, col_l2 = st.columns([2, 3])
    with col_l1:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🎯 RFM Frequency Segmentation</div>
            <div class="visual-sub">Gross food spend share across customer frequency cohorts.</div>
        </div>
        """, unsafe_allow_html=True)
        
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
            hole=0.45,
            color="Frequency_Tier",
            color_discrete_map={
                "Power User (25+)": "#FC8019",
                "Frequent Eater (12-24)": "#FB923C",
                "Regular (5-11)": "#FDBA74",
                "Occasional (1-4)": "#CBD5E1"
            }
        )
        fig_rfm.update_traces(textposition='inside', textinfo='percent+label')
        fig_rfm.update_layout(template="plotly_white", height=320, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_rfm, use_container_width=True, config={"displayModeBar": False})
        
    with col_l2:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🌟 VIP Customer Cohort Snapshot (Query 7: NTILE(20))</div>
            <div class="visual-sub">Top lifetime spenders generating outsized marketplace Gross Merchandise Value.</div>
        </div>
        """, unsafe_allow_html=True)
        
        top_users = delivered_df.groupby(["user_id", "name", "city", "is_swiggy_one"]).agg(
            Total_Orders=("order_id", "count"),
            Total_Spend=("total_amount", "sum"),
            Avg_Spend=("total_amount", "mean")
        ).reset_index().sort_values(by="Total_Spend", ascending=False).head(5)
        
        top_users_html = """
        <table class="pbi-table">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Customer Name</th>
                    <th>City</th>
                    <th>Swiggy One</th>
                    <th>Orders</th>
                    <th>Total Spend (₹)</th>
                    <th>Avg Ticket</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, u in top_users.iterrows():
            badge = '<span class="badge-pill-green">Active</span>' if u['is_swiggy_one'] == 1 else '<span class="badge-pill-red">Non-Member</span>'
            top_users_html += f"""
                <tr>
                    <td><code>#{int(u['user_id'])}</code></td>
                    <td><b>{u['name']}</b></td>
                    <td>{u['city']}</td>
                    <td>{badge}</td>
                    <td><b>{int(u['Total_Orders'])}</b></td>
                    <td><b style="color: #FC8019;">₹ {u['Total_Spend']:,.0f}</b></td>
                    <td>₹ {u['Avg_Spend']:.1f}</td>
                </tr>
            """
        top_users_html += "</tbody></table>"
        st.markdown(top_users_html, unsafe_allow_html=True)

# =============================================================================
# PAGE 3: DELIVERY LOGISTICS & SLA CONTROL TOWER
# =============================================================================
elif selected_page == "⏱️ Delivery & Logistics":
    st.markdown("""
    <div class="header-bar">
        <div>
            <h1>⏱️ Delivery Logistics & SLA Control Tower</h1>
            <p>Fleet Performance, Speed Benchmarks & Electric Vehicle (EV) Analytics</p>
        </div>
        <div>
            <span class="status-badge">
                <span style="height: 8px; width: 8px; background: #3B82F6; border-radius: 50%; display: inline-block;"></span>
                Operations Live
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4 Logistics KPI Cards (matching HTML dashboard Page 3)
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Average Delivery Duration</span>
                <span class="kpi-icon">⏱️</span>
            </div>
            <div class="kpi-val">{avg_deliv_time:.1f} mins</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">⚡ Target: ≤ 35m</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with d2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">On-Time Delivery Rate</span>
                <span class="kpi-icon">🛡️</span>
            </div>
            <div class="kpi-val">{ontime_rate:.1f}%</div>
            <div class="kpi-foot">
                <span class="badge-pill-muted">≤ 35 mins SLA benchmark</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with d3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Severe Delays (> 40 Mins)</span>
                <span class="kpi-icon">⚠️</span>
            </div>
            <div class="kpi-val" style="color: #EF4444;">{severe_delay_rate:.1f}%</div>
            <div class="kpi-foot">
                <span class="badge-pill-red">+4.8%</span>
                <span class="badge-pill-muted">during monsoon rush</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with d4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-top">
                <span class="kpi-title">Electric Vehicle (EV) Adoption</span>
                <span class="kpi-icon">🌱</span>
            </div>
            <div class="kpi-val">15.0%</div>
            <div class="kpi-foot">
                <span class="badge-pill-green">32.8 mins avg speed</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    # Dual-Axis Congestion Curve + SLA Tiers Donut
    col_d1, col_d2 = st.columns([3, 2])
    with col_d1:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🚦 Rush Hour Congestion & 35-Min SLA Breach Curve</div>
            <div class="visual-sub">Average delivery duration (orange line) spikes to 35.6m during the 7-10 PM dinner rush (bars).</div>
        </div>
        """, unsafe_allow_html=True)
        
        hourly_stats = delivered_df.groupby("hour").agg(
            Orders=("order_id", "count"),
            Avg_Mins=("delivery_time_mins", "mean")
        ).reset_index().sort_values(by="hour")
        
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        fig_dual.add_trace(
            go.Bar(
                x=hourly_stats["hour"],
                y=hourly_stats["Orders"],
                name="Delivered Order Demand",
                marker_color="#E5E7EB",
                opacity=0.75,
                hoverinfo="x+y"
            ),
            secondary_y=False
        )
        fig_dual.add_trace(
            go.Scatter(
                x=hourly_stats["hour"],
                y=hourly_stats["Avg_Mins"],
                name="Avg Delivery Duration (mins)",
                mode="lines+markers",
                line=dict(color="#FC8019", width=3.5),
                marker=dict(size=7, color="#EA580C")
            ),
            secondary_y=True
        )
        fig_dual.add_hline(
            y=35, 
            line_dash="dash", 
            line_color="#EF4444", 
            line_width=2,
            annotation_text="35-Min SLA Guarantee", 
            annotation_position="top left",
            secondary_y=True
        )
        fig_dual.update_xaxes(title_text="Hour of the Day (24-Hour Clock)", tickmode="linear", tick0=0, dtick=2, showgrid=False)
        fig_dual.update_yaxes(title_text="Delivered Orders Volume", showgrid=False, secondary_y=False)
        fig_dual.update_yaxes(title_text="Avg Delivery (Minutes)", showgrid=True, gridcolor="#F3F4F6", range=[25, 40], secondary_y=True)
        fig_dual.update_layout(
            template="plotly_white",
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dual, use_container_width=True, config={"displayModeBar": False})

    with col_d2:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🎯 Delivery SLA Compliance Tiers</div>
            <div class="visual-sub">Breakdown of orders delivered within target SLA vs. operational delays.</div>
        </div>
        """, unsafe_allow_html=True)
        
        def assign_sla_bucket(mins):
            if mins < 25: return "⚡ Express (< 25m)"
            elif mins <= 35: return "✅ On-Time (25-35m)"
            elif mins <= 45: return "⚠️ Minor Delay (36-45m)"
            else: return "🚨 Severe Delay (> 45m)"
            
        delivered_df["sla_tier"] = delivered_df["delivery_time_mins"].apply(assign_sla_bucket)
        sla_df = delivered_df.groupby("sla_tier").agg(Orders=("order_id", "count")).reset_index()
        
        fig_sla = px.pie(
            sla_df,
            names="sla_tier",
            values="Orders",
            hole=0.55,
            color="sla_tier",
            color_discrete_map={
                "⚡ Express (< 25m)": "#10B981",
                "✅ On-Time (25-35m)": "#FC8019",
                "⚠️ Minor Delay (36-45m)": "#F59E0B",
                "🚨 Severe Delay (> 45m)": "#EF4444"
            }
        )
        fig_sla.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
        fig_sla.update_layout(template="plotly_white", height=340, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_sla, use_container_width=True, config={"displayModeBar": False})

    # Bottom Row: City SLA Benchmark + Green Fleet Comparison
    col_d3, col_d4 = st.columns(2)
    with col_d3:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🏙️ City On-Time SLA Fulfillment Benchmark (% ≤ 35 min)</div>
            <div class="visual-sub">Kolkata and Delhi lead on-time rates; Bangalore & Hyderabad face traffic delays.</div>
        </div>
        """, unsafe_allow_html=True)
        
        city_perf = delivered_df.groupby("city")["delivery_time_mins"].agg(
            total="count",
            ontime=lambda x: (x <= 35).sum()
        ).reset_index()
        city_perf["ontime_pct"] = (city_perf["ontime"] / city_perf["total"]) * 100
        city_perf = city_perf.sort_values(by="ontime_pct", ascending=True)
        
        fig_city_sla = px.bar(
            city_perf,
            x="ontime_pct",
            y="city",
            orientation="h",
            text="ontime_pct",
            color="ontime_pct",
            color_continuous_scale=[[0, "#FB923C"], [1, "#10B981"]],
            labels={"city": "City", "ontime_pct": "On-Time Fulfillment (%)"}
        )
        fig_city_sla.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_city_sla.update_layout(
            template="plotly_white",
            height=320,
            coloraxis_showscale=False,
            margin=dict(l=10, r=30, t=10, b=10),
            xaxis=dict(showgrid=True, gridcolor="#F3F4F6", range=[50, 75], title="On-Time Rate (% Orders ≤ 35 Mins)"),
            yaxis=dict(title=None)
        )
        st.plotly_chart(fig_city_sla, use_container_width=True, config={"displayModeBar": False})
        
    with col_d4:
        st.markdown("""
        <div class="visual-box">
            <div class="visual-header">🌱 Green Fleet Transition: Electric Vehicles (EV) vs. Petrol</div>
            <div class="visual-sub">EV riders achieve higher customer ratings (4.34 ★) and reduce fuel subsidies.</div>
        </div>
        """, unsafe_allow_html=True)
        
        fleet_df = delivered_df.groupby("vehicle_type").agg(
            Deliveries=("order_id", "count"),
            Avg_Duration=("delivery_time_mins", "mean"),
            Rider_Rating=("rating_rider", "mean")
        ).reset_index()
        
        fleet_html = """
        <table class="pbi-table">
            <thead>
                <tr>
                    <th>Vehicle Fleet</th>
                    <th>Deliveries</th>
                    <th>Share %</th>
                    <th>Avg Duration</th>
                    <th>Rider Rating</th>
                    <th>ESG Status</th>
                </tr>
            </thead>
            <tbody>
        """
        total_fleet_deliv = fleet_df["Deliveries"].sum()
        for _, f_row in fleet_df.iterrows():
            is_ev = "Electric" in f_row["vehicle_type"]
            badge = '<span class="badge-pill-green">🌱 Net Zero Pioneer</span>' if is_ev else '<span class="badge-pill-muted">Standard Fleet</span>'
            fleet_html += f"""
                <tr>
                    <td><b>{f_row['vehicle_type']}</b></td>
                    <td>{int(f_row['Deliveries']):,}</td>
                    <td><b>{(f_row['Deliveries']/total_fleet_deliv*100):.1f}%</b></td>
                    <td>{f_row['Avg_Duration']:.1f} mins</td>
                    <td><b style="color: #FC8019;">{f_row['Rider_Rating']:.2f} ★</b></td>
                    <td>{badge}</td>
                </tr>
            """
        fleet_html += "</tbody></table>"
        st.markdown(fleet_html, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #DEF7EC; border: 1px solid #BCF0DA; border-radius: 8px; padding: 10px 14px; margin-top: 14px; font-size: 12px; color: #03543F; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 18px;">🔋</span>
            <div>
                <b>Swiggy Green Mile:</b> 1,905 zero-emission deliveries completed in FY24, preventing an estimated <b>28.4 tonnes of CO2 emissions</b>.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Operational Alerts Table
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="visual-box">
        <div class="visual-header">⚠️ Quality Risk Alert: High Volume / Low Rating (< 4.0 ★) Kitchens (SQL Query 12)</div>
        <div class="visual-sub">Immediate operational review required for kitchens with high fulfillment volume but lagging customer ratings.</div>
    </div>
    """, unsafe_allow_html=True)
    
    rest_risk = delivered_df.groupby(["restaurant_name", "city", "cuisine", "rating_rest"]).agg(
        Orders_Fulfilled=("order_id", "count"),
        Total_GMV=("total_amount", "sum"),
        Avg_Delivery=("delivery_time_mins", "mean")
    ).reset_index()
    risk_alert = rest_risk[(rest_risk["Orders_Fulfilled"] >= 50) & (rest_risk["rating_rest"] < 4.0)].sort_values(by="Orders_Fulfilled", ascending=False)
    
    if not risk_alert.empty:
        risk_html = """
        <table class="pbi-table">
            <thead>
                <tr>
                    <th>Restaurant Partner</th>
                    <th>City</th>
                    <th>Cuisine</th>
                    <th>Rating</th>
                    <th>Fulfilled Orders</th>
                    <th>Total GMV</th>
                    <th>Avg Speed</th>
                    <th>Operational Recommendation</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r_row in risk_alert.iterrows():
            action = "Audit Kitchen Prep SLA" if r_row["Avg_Delivery"] > 35 else "Packaging & Temperature Review"
            risk_html += f"""
                <tr>
                    <td><b>{r_row['restaurant_name']}</b></td>
                    <td>{r_row['city']}</td>
                    <td>{r_row['cuisine']}</td>
                    <td><span class="badge-pill-red">{r_row['rating_rest']:.1f} ★</span></td>
                    <td><b>{int(r_row['Orders_Fulfilled'])}</b></td>
                    <td>₹ {r_row['Total_GMV']:,.0f}</td>
                    <td>{r_row['Avg_Delivery']:.1f} mins</td>
                    <td><span style="background: #EFF6FF; color: #1D4ED8; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">{action}</span></td>
                </tr>
            """
        risk_html += "</tbody></table>"
        st.markdown(risk_html, unsafe_allow_html=True)
    else:
        st.success("No high-volume restaurants with sub-4.0 ratings detected under current filter selection.")
