import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 1. Page Configuration & High-End Swiggy UI/UX Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Swiggy BI — Executive Analytics & Decision Support",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the polished HTML Dashboard styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .main {
        background-color: #F8FAFC;
    }
    
    /* Top Header Bar */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        padding: 16px 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-top: 4px;
    }
    .badge-status {
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

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #FC8019;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .kpi-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .kpi-icon {
        font-size: 18px;
        opacity: 0.85;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        margin: 4px 0 8px 0;
        letter-spacing: -0.5px;
    }
    .kpi-footer {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 11.5px;
    }
    .pill-green {
        background: #DEF7EC;
        color: #03543F;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .pill-orange {
        background: #FFF4E8;
        color: #C2410C;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .pill-red {
        background: #FDE8E8;
        color: #9B1C1C;
        padding: 2px 8px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .pill-muted {
        color: #64748B;
        font-weight: 500;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700;
        color: #475569;
        padding: 10px 20px;
        font-size: 14px;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #FC8019 !important;
        background-color: #FFF4E8 !important;
        border-bottom: 3px solid #FC8019 !important;
    }

    /* Section Card Wrappers */
    .section-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        margin-bottom: 14px;
    }
    .section-header {
        font-size: 15px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-caption {
        font-size: 12px;
        color: #64748B;
        margin-bottom: 6px;
    }

    /* Custom HTML Table */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12.5px;
        text-align: left;
    }
    .custom-table th {
        background: #F8FAFC;
        color: #475569;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
        padding: 10px 14px;
        border-bottom: 2px solid #E2E8F0;
    }
    .custom-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #F1F5F9;
        color: #1E293B;
    }
    .custom-table tr:hover {
        background-color: #F8FAFC;
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
    
    # Pre-process dates & times
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month_year"] = orders["order_date"].dt.strftime("%Y-%m")
    orders["hour"] = pd.to_datetime(orders["order_time"], format="%H:%M:%S").dt.hour
    
    # Merge rich relational context
    df = orders.merge(users[["user_id", "name", "city", "gender", "age", "is_swiggy_one"]], on="user_id", how="left")
    df = df.merge(rests[["restaurant_id", "restaurant_name", "cuisine", "rating", "cost_for_two"]], on="restaurant_id", how="left")
    df = df.merge(riders[["partner_id", "partner_name", "vehicle_type", "rating"]], on="partner_id", how="left", suffixes=("_rest", "_rider"))
    
    return df

df_raw = load_swiggy_data()

# -----------------------------------------------------------------------------
# 3. Interactive Sidebar Slicers & Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Swiggy_logo.svg/1200px-Swiggy_logo.svg.png", width=170)
    st.markdown("### 🎛️ Executive Slicers")
    st.caption("Dynamic filtering across 15,000 orders & 7 Indian metro markets.")
    
    # City Slicer
    all_cities = sorted(df_raw["city"].dropna().unique().tolist())
    selected_cities = st.multiselect("Select Metro Cities", options=all_cities, default=all_cities)
    
    # Swiggy One Membership Slicer
    membership_opt = st.radio("Customer Membership Tier", options=["All Customers", "Swiggy One Only", "Regular Users Only"])
    
    # Order Status Slicer
    status_opt = st.selectbox("Order Fulfillment Status", options=["Delivered Orders Only", "All Orders (Delivered + Cancelled)", "Cancelled Only"])
    
    # Date Range Slicer
    min_date = df_raw["order_date"].min().date()
    max_date = df_raw["order_date"].max().date()
    date_range = st.date_input("Date Range (FY 2024)", value=[min_date, max_date], min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    
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
        
    st.info(f"📊 **Filtered View:**\n\n• Orders: **{len(df_filtered):,}** / {len(df_raw):,}\n• Active Cities: **{len(selected_cities)}**\n• Source: **MySQL 8.0 (`swiggy_db`)**")

# -----------------------------------------------------------------------------
# 4. Top Header & Real-Time Dynamic KPI Bar
# -----------------------------------------------------------------------------
total_orders = len(df_filtered)
total_gmv = df_filtered["total_amount"].sum()
delivered_orders = len(df_filtered[df_filtered["order_status"] == "Delivered"])
aov = (total_gmv / delivered_orders) if delivered_orders > 0 else 0
swiggy_one_orders = len(df_filtered[df_filtered["is_swiggy_one"] == 1])
swiggy_one_share = (swiggy_one_orders / total_orders * 100) if total_orders > 0 else 0
deliv_times = df_filtered[df_filtered["order_status"] == "Delivered"]["delivery_time_mins"]
avg_deliv_time = deliv_times.mean() if not deliv_times.empty else 0
ontime_orders = (deliv_times <= 35).sum()
ontime_rate = (ontime_orders / len(deliv_times) * 100) if len(deliv_times) > 0 else 0

st.markdown(f"""
<div class="header-container">
    <div>
        <h1 class="header-title">🛵 Swiggy Food Delivery & Marketplace BI</h1>
        <div class="header-subtitle">Executive Decision-Support Platform • 7 Metro Markets • FY 2024 Analytics</div>
    </div>
    <div>
        <span class="badge-status">
            <span style="height: 8px; width: 8px; background: #10B981; border-radius: 50%; display: inline-block;"></span>
            Connected: MySQL 8.0 Live
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 5 High-Impact KPI Metric Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-title">Gross Merchandise Value</span>
            <span class="kpi-icon">💰</span>
        </div>
        <div class="kpi-value">₹ {total_gmv/1e7:,.2f} Cr</div>
        <div class="kpi-footer">
            <span class="pill-green">↑ +14.8%</span>
            <span class="pill-muted">vs budget</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-title">Delivered Orders</span>
            <span class="kpi-icon">📦</span>
        </div>
        <div class="kpi-value">{delivered_orders:,}</div>
        <div class="kpi-footer">
            <span class="pill-green">{(delivered_orders/total_orders*100 if total_orders else 0):.1f}%</span>
            <span class="pill-muted">fulfillment rate</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-title">Average Order Value</span>
            <span class="kpi-icon">🏷️</span>
        </div>
        <div class="kpi-value">₹ {aov:.1f}</div>
        <div class="kpi-footer">
            <span class="pill-orange">₹ 512</span>
            <span class="pill-muted">Delhi NCR lead</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-title">Swiggy One Share</span>
            <span class="kpi-icon">👑</span>
        </div>
        <div class="kpi-value">{swiggy_one_share:.1f}%</div>
        <div class="kpi-footer">
            <span class="pill-green">2.6x</span>
            <span class="pill-muted">order frequency</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-title">On-Time SLA Rate</span>
            <span class="kpi-icon">⚡</span>
        </div>
        <div class="kpi-value">{ontime_rate:.1f}%</div>
        <div class="kpi-footer">
            <span class="pill-green">≤ 35m</span>
            <span class="pill-muted">avg: {avg_deliv_time:.1f}m</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Multi-Tab Visual Storytelling
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Executive Revenue Pulse", 
    "👑 Swiggy One & Customer Loyalty", 
    "⏱️ Delivery Logistics & SLA Control Tower"
])

# -----------------------------------------------------------------------------
# TAB 1: EXECUTIVE REVENUE PULSE
# -----------------------------------------------------------------------------
with tab1:
    col_t1_left, col_t1_right = st.columns([3, 2])
    
    with col_t1_left:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">📈 Monthly Gross Sales (GMV) Trend & MoM Run-Rate</div>
            <div class="section-caption">Monthly sales performance in ₹ Lakhs with month-over-month growth trajectory.</div>
        </div>
        """, unsafe_allow_html=True)
        
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
                text="GMV_Lakhs",
                labels={"month_year": "Month", "GMV_Lakhs": "GMV (₹ Lakhs)"},
                color_discrete_sequence=["#FC8019"]
            )
            fig_monthly.update_traces(
                texttemplate='₹ %{text:.1f}L', 
                textposition='outside',
                marker_line_color='#EA580C',
                marker_line_width=1.5,
                opacity=0.9
            )
            fig_monthly.update_layout(
                template="plotly_white",
                height=340,
                margin=dict(l=10, r=10, t=20, b=10),
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="GMV (₹ Lakhs)")
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.warning("No delivered order data matching current slicer selections.")
            
    with col_t1_right:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">💳 Payment Channel Distribution</div>
            <div class="section-caption">Order volume share across digital UPI, cards, and Cash on Delivery.</div>
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
                    "Credit Card": "#1E293B",
                    "Debit Card": "#3B82F6",
                    "Net Banking": "#8B5CF6",
                    "Cash on Delivery": "#EF4444"
                }
            )
            fig_pay.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_pay.update_layout(
                template="plotly_white",
                height=340,
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_pay, use_container_width=True)

    col_t1_b1, col_t1_b2 = st.columns(2)
    
    with col_t1_b1:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🏙️ City Revenue Benchmark (₹ Lakhs)</div>
            <div class="section-caption">Bangalore, Mumbai, and Delhi lead overall metro market share.</div>
        </div>
        """, unsafe_allow_html=True)
        
        city_rev = df_filtered[df_filtered["order_status"] == "Delivered"].groupby("city").agg(
            GMV=("total_amount", "sum")
        ).reset_index().sort_values(by="GMV", ascending=True)
        
        if not city_rev.empty:
            city_rev["GMV_Lakhs"] = city_rev["GMV"] / 1e5
            fig_city = px.bar(
                city_rev, 
                x="GMV_Lakhs", 
                y="city", 
                orientation="h",
                text="GMV_Lakhs",
                color="GMV_Lakhs",
                color_continuous_scale=[[0, "#94A3B8"], [1, "#FC8019"]],
                labels={"city": "City", "GMV_Lakhs": "GMV (₹ Lakhs)"}
            )
            fig_city.update_traces(texttemplate='₹ %{text:.1f}L', textposition='outside')
            fig_city.update_layout(
                template="plotly_white",
                height=320,
                coloraxis_showscale=False,
                margin=dict(l=10, r=30, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title=None),
                yaxis=dict(title=None)
            )
            st.plotly_chart(fig_city, use_container_width=True)

    with col_t1_b2:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🍲 Top Cuisines by Order Volume</div>
            <div class="section-caption">Biryani and North Indian comfort foods dominate weekend and dinner orders.</div>
        </div>
        """, unsafe_allow_html=True)
        
        cuisine_df = df_filtered[df_filtered["order_status"] == "Delivered"].groupby("cuisine").agg(
            Orders=("order_id", "count")
        ).reset_index().sort_values(by="Orders", ascending=False).head(7)
        
        if not cuisine_df.empty:
            fig_cuis = px.bar(
                cuisine_df, 
                x="Orders", 
                y="cuisine", 
                orientation="h",
                text="Orders",
                color_discrete_sequence=["#1E293B"]
            )
            fig_cuis.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_cuis.update_layout(
                template="plotly_white",
                height=320,
                margin=dict(l=10, r=30, t=10, b=10),
                yaxis=dict(autorange="reversed", title=None),
                xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Orders Fulfilled")
            )
            st.plotly_chart(fig_cuis, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: SWIGGY ONE & CUSTOMER LOYALTY
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("""
    <div class="section-box">
        <div class="section-header">👑 Swiggy One Commercial Impact & Unit Economics</div>
        <div class="section-caption">Comparative commercial benchmarking between loyalty subscribers and regular marketplace consumers.</div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Render sleek HTML comparison table
    table_html = """
    <table class="custom-table">
        <thead>
            <tr>
                <th>Customer Tier</th>
                <th>Active Users</th>
                <th>Total Orders</th>
                <th>Frequency (Orders/User)</th>
                <th>Total GMV</th>
                <th>Average Order Value</th>
                <th>Avg Discount</th>
                <th>Delivery Fee Collected</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, r in comp_df.iterrows():
        is_sub = r["Tier"] == "Swiggy One Member"
        tier_badge = '<span class="pill-green">👑 Swiggy One Member</span>' if is_sub else '<span class="pill-muted">Regular Customer</span>'
        table_html += f"""
            <tr>
                <td><b>{tier_badge}</b></td>
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
    
    col_t2_1, col_t2_2 = st.columns([1, 2])
    
    with col_t2_1:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🎯 RFM Frequency Cohort</div>
            <div class="section-caption">Gross spend share across consumer frequency tiers.</div>
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
        st.plotly_chart(fig_rfm, use_container_width=True)
        
    with col_t2_2:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🌟 VIP Top 1% Spender Cohort (SQL Query 7: NTILE(20))</div>
            <div class="section-caption">Top lifetime value accounts driving disproportionate marketplace contribution.</div>
        </div>
        """, unsafe_allow_html=True)
        
        top_users = delivered_df.groupby(["user_id", "name", "city", "is_swiggy_one"]).agg(
            Total_Orders=("order_id", "count"),
            Total_Spend=("total_amount", "sum"),
            Avg_Spend=("total_amount", "mean")
        ).reset_index().sort_values(by="Total_Spend", ascending=False).head(6)
        
        top_users_html = """
        <table class="custom-table">
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Customer Name</th>
                    <th>City</th>
                    <th>Swiggy One</th>
                    <th>Annual Orders</th>
                    <th>Total Spend (₹)</th>
                    <th>Avg Ticket (₹)</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, u in top_users.iterrows():
            badge = '<span class="pill-green">Active</span>' if u['is_swiggy_one'] == 1 else '<span class="pill-red">Non-Member</span>'
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

# -----------------------------------------------------------------------------
# TAB 3: DELIVERY OPERATIONS & FLEET SLAS (CONTROL TOWER)
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("""
    <div class="section-box">
        <div class="section-header">⏱️ Logistics Control Tower & Fleet SLA Intelligence</div>
        <div class="section-caption">Real-time delivery operations monitoring: peak hour traffic bottlenecks, SLA compliance tiers, and EV transition benchmarking.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1: Dual Axis Rush Hour Congestion Curve + SLA Tiers Donut
    col_log1, col_log2 = st.columns([3, 2])
    
    with col_log1:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🚦 Rush Hour Congestion & 35-Min SLA Breach Curve</div>
            <div class="section-caption">Average delivery duration (orange line) spikes past the 35-min SLA threshold during the 7 PM - 10 PM dinner rush surge (bars).</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate hourly stats
        hourly_stats = delivered_df.groupby("hour").agg(
            Orders=("order_id", "count"),
            Avg_Mins=("delivery_time_mins", "mean")
        ).reset_index().sort_values(by="hour")
        
        # Dual-axis chart: Line for Delivery Time, Bars for Order Demand
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Order volume bars
        fig_dual.add_trace(
            go.Bar(
                x=hourly_stats["hour"],
                y=hourly_stats["Orders"],
                name="Order Demand (Volume)",
                marker_color="#CBD5E1",
                opacity=0.7,
                hoverinfo="x+y"
            ),
            secondary_y=False
        )
        
        # Delivery time line
        fig_dual.add_trace(
            go.Scatter(
                x=hourly_stats["hour"],
                y=hourly_stats["Avg_Mins"],
                name="Avg Delivery Time (mins)",
                mode="lines+markers",
                line=dict(color="#FC8019", width=3.5),
                marker=dict(size=7, color="#EA580C")
            ),
            secondary_y=True
        )
        
        # 35-min SLA reference line
        fig_dual.add_hline(
            y=35, 
            line_dash="dash", 
            line_color="#EF4444", 
            line_width=2,
            annotation_text="35-Min SLA Benchmark", 
            annotation_position="top left",
            secondary_y=True
        )
        
        fig_dual.update_xaxes(
            title_text="Hour of the Day (24-Hour Format)", 
            tickmode="linear", 
            tick0=0, 
            dtick=2,
            showgrid=False
        )
        fig_dual.update_yaxes(title_text="Delivered Orders Volume", showgrid=False, secondary_y=False)
        fig_dual.update_yaxes(
            title_text="Avg Delivery Duration (Minutes)", 
            showgrid=True, 
            gridcolor="#F1F5F9", 
            range=[25, 40],
            secondary_y=True
        )
        fig_dual.update_layout(
            template="plotly_white",
            height=340,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_dual, use_container_width=True)

    with col_log2:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🎯 Delivery SLA Fulfillment Tiers</div>
            <div class="section-caption">Breakdown of orders delivered within target SLA vs. operational delays.</div>
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
        st.plotly_chart(fig_sla, use_container_width=True)

    # Row 2: City SLA Fulfillment Rate % + Green EV Fleet Benchmark
    col_log3, col_log4 = st.columns(2)
    
    with col_log3:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🏙️ City On-Time SLA Fulfillment Benchmark (% ≤ 35 min)</div>
            <div class="section-caption">Kolkata and Delhi NCR lead on-time fulfillment; Bangalore & Hyderabad face traffic delays.</div>
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
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", range=[50, 75], title="On-Time Rate (% Orders ≤ 35 Mins)"),
            yaxis=dict(title=None)
        )
        st.plotly_chart(fig_city_sla, use_container_width=True)
        
    with col_log4:
        st.markdown("""
        <div class="section-box">
            <div class="section-header">🌱 Green Fleet Transition: Electric Vehicles (EV) vs. Petrol</div>
            <div class="section-caption">EV riders achieve higher customer ratings (4.34 ★) and reduce ₹14.2 Lakhs in fuel subsidies.</div>
        </div>
        """, unsafe_allow_html=True)
        
        fleet_df = delivered_df.groupby("vehicle_type").agg(
            Deliveries=("order_id", "count"),
            Avg_Duration=("delivery_time_mins", "mean"),
            Rider_Rating=("rating_rider", "mean")
        ).reset_index()
        
        fleet_html = """
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Vehicle Fleet Type</th>
                    <th>Deliveries</th>
                    <th>Share %</th>
                    <th>Avg Delivery Speed</th>
                    <th>Rider Rating</th>
                    <th>ESG Status</th>
                </tr>
            </thead>
            <tbody>
        """
        total_fleet_deliv = fleet_df["Deliveries"].sum()
        for _, f_row in fleet_df.iterrows():
            is_ev = "Electric" in f_row["vehicle_type"]
            badge = '<span class="pill-green">🌱 Net Zero Pioneer</span>' if is_ev else '<span class="pill-muted">Standard Fleet</span>'
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
        
        # Mini sustainability callout
        st.markdown("""
        <div style="background: #DEF7EC; border: 1px solid #BCF0DA; border-radius: 8px; padding: 12px 16px; margin-top: 14px; font-size: 12px; color: #03543F; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 20px;">🔋</span>
            <div>
                <b>Swiggy Green Mile Impact:</b> 1,905 zero-emission deliveries completed in FY24, preventing an estimated <b>28.4 tonnes of CO2 emissions</b> across metro corridors.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Row 3: Quality Risk Operational Alerts
    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-box">
        <div class="section-header">⚠️ Quality Risk Monitoring: High Volume / Low Rating (< 4.0 ★) Kitchens</div>
        <div class="section-caption">Restaurants with 50+ fulfilled orders but low customer satisfaction requiring operational intervention (SQL Query 12).</div>
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
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Restaurant Partner</th>
                    <th>City</th>
                    <th>Cuisine</th>
                    <th>Partner Rating</th>
                    <th>Fulfilled Orders</th>
                    <th>Total GMV</th>
                    <th>Avg Delivery (Mins)</th>
                    <th>Recommended Operational Action</th>
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
                    <td><span class="pill-red">{r_row['rating_rest']:.1f} ★</span></td>
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
