"""
Swiggy Business Performance & Financial Review Workbook Generator
Uses openpyxl to generate an executive-ready, multi-tab Excel model with:
- Professional Swiggy branding (#FC8019)
- Styled KPI cards
- Monthly Business Review (MBR)
- Unit Economics & Platform Take-Rate P&L
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
os.makedirs(EXCEL_DIR, exist_ok=True)

# Load data for real summary metrics
orders_df = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
rests_df = pd.read_csv(os.path.join(DATA_DIR, "restaurants.csv"))

delivered = orders_df[orders_df["order_status"] == "Delivered"].copy()
delivered["month"] = pd.to_datetime(delivered["order_date"]).dt.strftime("%Y-%m")

wb = openpyxl.Workbook()

# Define Color Palette (Swiggy Orange & Professional Dark Grays)
SWIGGY_ORANGE = "FC8019"
DARK_NAVY = "1F2937"
ACCENT_LIGHT = "FFF4E8"
BORDER_GRAY = "E5E7EB"
HEADER_GRAY = "F3F4F6"
SUCCESS_GREEN = "10B981"

font_title = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
font_sub = Font(name="Segoe UI", size=10, italic=True, color="FFFFFF")
font_section = Font(name="Segoe UI", size=12, bold=True, color=DARK_NAVY)
font_card_label = Font(name="Segoe UI", size=9, color="6B7280", bold=True)
font_card_value = Font(name="Segoe UI", size=16, bold=True, color=DARK_NAVY)
font_tbl_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_regular = Font(name="Segoe UI", size=10, color="1F2937")
font_bold = Font(name="Segoe UI", size=10, bold=True, color="1F2937")

fill_orange = PatternFill(start_color=SWIGGY_ORANGE, end_color=SWIGGY_ORANGE, fill_type="solid")
fill_dark = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
fill_card = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
fill_card_bg = PatternFill(start_color=ACCENT_LIGHT, end_color=ACCENT_LIGHT, fill_type="solid")
fill_header = PatternFill(start_color=DARK_NAVY, end_color=DARK_NAVY, fill_type="solid")
fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

thin_border = Border(
    left=Side(style="thin", color=BORDER_GRAY),
    right=Side(style="thin", color=BORDER_GRAY),
    top=Side(style="thin", color=BORDER_GRAY),
    bottom=Side(style="thin", color=BORDER_GRAY)
)

card_border = Border(
    left=Side(style="medium", color=SWIGGY_ORANGE),
    right=Side(style="thin", color=BORDER_GRAY),
    top=Side(style="thin", color=BORDER_GRAY),
    bottom=Side(style="thin", color=BORDER_GRAY)
)

# =============================================================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================================================
ws1 = wb.active
ws1.title = "Executive Summary"
ws1.views.sheetView[0].showGridLines = True

# Banner Header
ws1.merge_cells("A1:H2")
top_banner = ws1["A1"]
top_banner.value = "SWIGGY FOOD DELIVERY | EXECUTIVE PERFORMANCE DASHBOARD"
top_banner.font = font_title
top_banner.alignment = Alignment(horizontal="center", vertical="center")
top_banner.fill = fill_orange

# Subtitle
ws1.merge_cells("A3:H3")
sub_banner = ws1["A3"]
sub_banner.value = "Annual Business Review & Marketplace Metrics (FY 2024)"
sub_banner.font = Font(name="Segoe UI", size=10, bold=True, color="4B5563")
sub_banner.alignment = Alignment(horizontal="center", vertical="center")

# KPI Summary Values
total_orders_val = len(delivered)
total_gmv_val = delivered["total_amount"].sum()
aov_val = delivered["total_amount"].mean()
unique_users_val = delivered["user_id"].nunique()
swiggy_one_users = users_df["is_swiggy_one"].sum()
swiggy_one_pct = (swiggy_one_users / len(users_df)) * 100
ontime_orders = (delivered["delivery_time_mins"] <= 35).sum()
ontime_pct = (ontime_orders / total_orders_val) * 100

kpis = [
    ("TOTAL GMV (SALES)", f"₹ {total_gmv_val:,.0f}", "A5:B6"),
    ("TOTAL DELIVERED ORDERS", f"{total_orders_val:,}", "C5:D6"),
    ("AVERAGE ORDER VALUE (AOV)", f"₹ {aov_val:.1f}", "E5:F6"),
    ("ACTIVE RESTAURANTS", f"{len(rests_df):,}", "G5:H6"),
    ("ACTIVE CUSTOMERS", f"{unique_users_val:,}", "A8:B9"),
    ("SWIGGY ONE ADOPTION", f"{swiggy_one_pct:.1f}%", "C8:D9"),
    ("ON-TIME DELIVERY RATE", f"{ontime_pct:.1f}%", "E8:F9"),
    ("AVG DELIVERY TIME", f"{delivered['delivery_time_mins'].mean():.1f} mins", "G8:H9")
]

for label, val, rng in kpis:
    ws1.merge_cells(rng)
    start_cell = ws1[rng.split(":")[0]]
    start_cell.value = f"{label}\n{val}"
    start_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    start_cell.fill = fill_card_bg
    start_cell.font = font_card_value
    
    # Border for the card range
    r1, r2 = int(rng.split(":")[0][1:]), int(rng.split(":")[1][1:])
    c1, c2 = rng.split(":")[0][0], rng.split(":")[1][0]
    for row in ws1[rng]:
        for cell in row:
            cell.border = thin_border

# Section: City Breakdown
ws1["A12"].value = "Marketplace Performance by City"
ws1["A12"].font = font_section

city_headers = ["City", "Delivered Orders", "Total GMV (₹)", "AOV (₹)", "Avg Delivery (Mins)", "Active Restaurants"]
for col_idx, h in enumerate(city_headers, start=1):
    cell = ws1.cell(row=13, column=col_idx, value=h)
    cell.font = font_tbl_header
    cell.fill = fill_header
    cell.alignment = Alignment(horizontal="center", vertical="center")

merged_city = delivered.merge(users_df[["user_id", "city"]], on="user_id")
city_summary = merged_city.groupby("city").agg(
    orders=("order_id", "count"),
    gmv=("total_amount", "sum"),
    aov=("total_amount", "mean"),
    avg_deliv=("delivery_time_mins", "mean")
).reset_index().sort_values(by="gmv", ascending=False)

city_rests_map = rests_df["city"].value_counts().to_dict()

for row_idx, r in enumerate(city_summary.itertuples(), start=14):
    ws1.cell(row=row_idx, column=1, value=r.city).font = font_bold
    ws1.cell(row=row_idx, column=2, value=r.orders).number_format = "#,##0"
    ws1.cell(row=row_idx, column=3, value=r.gmv).number_format = "₹ #,##0"
    ws1.cell(row=row_idx, column=4, value=round(r.aov, 1)).number_format = "₹ #,##0.0"
    ws1.cell(row=row_idx, column=5, value=round(r.avg_deliv, 1)).number_format = "0.0"
    ws1.cell(row=row_idx, column=6, value=city_rests_map.get(r.city, 0)).number_format = "#,##0"
    
    for c in range(1, 7):
        ws1.cell(row=row_idx, column=c).border = thin_border
        if row_idx % 2 == 0:
            ws1.cell(row=row_idx, column=c).fill = fill_zebra

# =============================================================================
# TAB 2: MONTHLY BUSINESS REVIEW (MBR)
# =============================================================================
ws2 = wb.create_sheet(title="Monthly Business Review")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:G2")
mbr_banner = ws2["A1"]
mbr_banner.value = "SWIGGY FY24 MONTHLY BUSINESS REVIEW (MBR)"
mbr_banner.font = font_title
mbr_banner.alignment = Alignment(horizontal="center", vertical="center")
mbr_banner.fill = fill_dark

mbr_headers = ["Month", "Delivered Orders", "Gross GMV (₹)", "AOV (₹)", "Total Discounts (₹)", "Avg Delivery Time", "MoM Growth %"]
for col_idx, h in enumerate(mbr_headers, start=1):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.font = font_tbl_header
    cell.fill = fill_orange
    cell.alignment = Alignment(horizontal="center", vertical="center")

monthly_grp = delivered.groupby("month").agg(
    orders=("order_id", "count"),
    gmv=("total_amount", "sum"),
    aov=("total_amount", "mean"),
    discounts=("discount_amount", "sum"),
    deliv=("delivery_time_mins", "mean")
).reset_index()

for idx, r in enumerate(monthly_grp.itertuples(), start=5):
    ws2.cell(row=idx, column=1, value=r.month).font = font_bold
    ws2.cell(row=idx, column=2, value=r.orders).number_format = "#,##0"
    ws2.cell(row=idx, column=3, value=r.gmv).number_format = "₹ #,##0"
    ws2.cell(row=idx, column=4, value=round(r.aov, 1)).number_format = "₹ #,##0.0"
    ws2.cell(row=idx, column=5, value=r.discounts).number_format = "₹ #,##0"
    ws2.cell(row=idx, column=6, value=round(r.deliv, 1)).number_format = "0.0"
    
    # Dynamic MoM formula for column G
    if idx == 5:
        ws2.cell(row=idx, column=7, value="-").alignment = Alignment(horizontal="center")
    else:
        formula = f"=(C{idx}-C{idx-1})/C{idx-1}"
        cell_g = ws2.cell(row=idx, column=7, value=formula)
        cell_g.number_format = "0.0%"
        cell_g.font = font_bold
        
    for c in range(1, 8):
        ws2.cell(row=idx, column=c).border = thin_border
        if idx % 2 == 0:
            ws2.cell(row=idx, column=c).fill = fill_zebra

# Add Total Row
total_row = len(monthly_grp) + 5
ws2.cell(row=total_row, column=1, value="Full Year Total").font = font_bold
ws2.cell(row=total_row, column=2, value=f"=SUM(B5:B{total_row-1})").number_format = "#,##0"
ws2.cell(row=total_row, column=3, value=f"=SUM(C5:C{total_row-1})").number_format = "₹ #,##0"
ws2.cell(row=total_row, column=4, value=f"=AVERAGE(D5:D{total_row-1})").number_format = "₹ #,##0.0"
ws2.cell(row=total_row, column=5, value=f"=SUM(E5:E{total_row-1})").number_format = "₹ #,##0"
ws2.cell(row=total_row, column=6, value=f"=AVERAGE(F5:F{total_row-1})").number_format = "0.0"
ws2.cell(row=total_row, column=7, value="-").alignment = Alignment(horizontal="center")

for c in range(1, 8):
    ws2.cell(row=total_row, column=c).font = font_bold
    ws2.cell(row=total_row, column=c).fill = PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid")
    ws2.cell(row=total_row, column=c).border = thin_border

# =============================================================================
# TAB 3: COMMISSION & TAKE-RATE MODEL
# =============================================================================
ws3 = wb.create_sheet(title="Commission & Unit Economics")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells("A1:F2")
pnl_banner = ws3["A1"]
pnl_banner.value = "SWIGGY MARKETPLACE TAKE-RATE & UNIT ECONOMICS MODEL"
pnl_banner.font = font_title
pnl_banner.alignment = Alignment(horizontal="center", vertical="center")
pnl_banner.fill = fill_orange

ws3["A4"].value = "Revenue & Cost Drivers (Unit Economics)"
ws3["A4"].font = font_section

pnl_lines = [
    ("Total Food GMV (Gross Sales)", f"₹ {total_gmv_val:,.0f}", "100.0%", "Total marketplace gross merchandise value"),
    ("(-) Restaurant Payout (Food Cost)", f"₹ {total_gmv_val * 0.79:,.0f}", "79.0%", "Amount paid to restaurant partners (avg 79%)"),
    ("(=) Swiggy Restaurant Commission (Take Rate)", f"₹ {total_gmv_val * 0.21:,.0f}", "21.0%", "Blended 21% commission earned by Swiggy"),
    ("(+) Delivery Fees Collected from Customers", f"₹ {delivered['delivery_fee'].sum():,.0f}", f"{delivered['delivery_fee'].sum() / total_gmv_val * 100:.1f}%", "Customer delivery charges (₹0 for Swiggy One)"),
    ("(-) Delivery Partner Payouts", f"₹ {total_orders_val * 42:,.0f}", f"{(total_orders_val * 42) / total_gmv_val * 100:.1f}%", "Rider compensation (avg ₹42 per delivery trip)"),
    ("(-) Platform Subsidized Discounts", f"₹ {delivered['discount_amount'].sum():,.0f}", f"{delivered['discount_amount'].sum() / total_gmv_val * 100:.1f}%", "Promotions & Swiggy One membership discounts"),
    ("(=) Net Platform Contribution Margin", f"₹ {(total_gmv_val * 0.21 + delivered['delivery_fee'].sum() - total_orders_val * 42 - delivered['discount_amount'].sum()):,.0f}", "Calculated", "Net cash margin retained before corporate overheads")
]

pnl_headers = ["P&L Line Item", "Annual Value (₹)", "% of GMV", "Business Explanation"]
for c_idx, h in enumerate(pnl_headers, start=1):
    cell = ws3.cell(row=5, column=c_idx, value=h)
    cell.font = font_tbl_header
    cell.fill = fill_dark
    cell.alignment = Alignment(horizontal="center", vertical="center")

for idx, (item, val_str, pct_str, expl) in enumerate(pnl_lines, start=6):
    ws3.cell(row=idx, column=1, value=item).font = font_bold if "(=)" in item else font_regular
    ws3.cell(row=idx, column=2, value=val_str).font = font_bold if "(=)" in item else font_regular
    ws3.cell(row=idx, column=3, value=pct_str).alignment = Alignment(horizontal="center")
    ws3.cell(row=idx, column=4, value=expl).font = Font(name="Segoe UI", size=9, italic=True, color="4B5563")
    
    for c in range(1, 5):
        ws3.cell(row=idx, column=c).border = thin_border
        if "(=)" in item:
            ws3.cell(row=idx, column=c).fill = fill_card_bg

# Adjust column widths automatically
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

excel_output_path = os.path.join(EXCEL_DIR, "swiggy_business_performance_review.xlsx")
wb.save(excel_output_path)
print(f"SUCCESS: Generated professional Excel model at: {excel_output_path}")
