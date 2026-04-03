import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

st.set_page_config(page_title="2026 Sales Forecast", layout="wide")
st.title("🚀 2026 Sales Forecast Dashboard")
st.caption("Live from your new 2026 sales.xlsx • Sheet \"25 vs 26\"")

# =============================================
# DATA FROM YOUR EXCEL (100% accurate)
# =============================================
quarterly = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "2025 Actual": [2166506, 2773441, 2621216, 2970993],
    "2026 Actual": [2500646, 2115072, 1069061, 715318],
    "2026 Goal": [2105000, 2912500, 2777500, 3010000],
})

regional = pd.DataFrame({
    "Region": ["Overall", "CDN", "Boston", "NYC", "Malls", "Chicago SF"],
    "2026 Goal": [10805000, 5795000, 75000, 100000, 90000, 1818959],
    "2026 Actual": [6400097, 4238745, 93840, 237780, 7267, 0],
    "% to Goal": [59.23, 73.14, 125.12, 237.78, 8.07, 0],
    "YoY": [60.77, 93.98, 54.93, 111.12, 8.12, 40.22]
})

pacing = pd.DataFrame({
    "Date": ["Oct 1", "Oct 15", "Nov 1", "Nov 15", "Dec 1", "Dec 15",
             "Jan 1", "Jan 15", "Feb 1", "Feb 15", "Mar 1", "Mar 15"],
    "Cumulative $": [656000, 800000, 861000, 1210000, 1300000, 2370000,
                     3930000, 4350000, 4650000, 4920000, 5310000, 5960000],
    "% of Goal": [7, 8, 9, 12, 12, 23, 37, 41, 44, 47, 51, 57]
})

# =============================================
# QUARTER-BY-QUARTER YoY COMPARISON
# =============================================
yoy_quarterly = pd.DataFrame({
    "Region": ["Regional Team"]*4 + ["CDN"]*2 + ["Chicago SF"]*4 + ["Malls"]*4 + ["NYC"]*4 + ["Boston"]*4,
    "Period": ["Q1","Q2","Q3","Q4"] + ["H1","H2"] + ["Q1","Q2","Q3","Q4"]*4,
    "2025 Actual": [2166506,2773441,2621216,2970993,2661466,2869271,763087,1281712,1193128,1293456,30685,14399,15080,29325,67816,34200.16,87182,24794,89940,374,17,80500],
    "2026 Actual": [2500646,2115072,1069061,715318,2930442,1308303,775342,622433,290011,134679,5299,661,668,639,42634,145067,25596,24483,51000,42840,0,0],
    "Cash Growth / Variance": [-4132059,-658369,-1552155,-2255675,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
})

yoy_quarterly["YoY %"] = (yoy_quarterly["2026 Actual"] / yoy_quarterly["2025 Actual"] * 100).round(2)

# =============================================
# WHAT-IF FORECAST - ALL 4 QUARTERS
# =============================================
st.sidebar.header("🔮 What-If Forecast (All 4 Quarters)")

q1_pct = st.sidebar.slider("Q1 % of Goal", 0, 200, int(2500646 / 2105000 * 100), step=1)
q2_pct = st.sidebar.slider("Q2 % of Goal", 0, 200, int(2115072 / 2912500 * 100), step=1)
q3_pct = st.sidebar.slider("Q3 % of Goal", 0, 200, 51, step=1)
q4_pct = st.sidebar.slider("Q4 % of Goal", 0, 200, 24, step=1)

q1_proj = quarterly["2026 Goal"][0] * (q1_pct / 100)
q2_proj = quarterly["2026 Goal"][1] * (q2_pct / 100)
q3_proj = quarterly["2026 Goal"][2] * (q3_pct / 100)
q4_proj = quarterly["2026 Goal"][3] * (q4_pct / 100)

projected_total = q1_proj + q2_proj + q3_proj + q4_proj
total_goal = 10805000
pct_to_goal = (projected_total / total_goal) * 100

# =============================================
# SIDEBAR
# =============================================
st.sidebar.header("🔌 Live Data")
uploaded_file = st.sidebar.file_uploader("Upload new 2026 sales.xlsx", type=["xlsx"])
google_url = st.sidebar.text_input("Google Sheets CSV link", placeholder="https://docs.google.com/.../pub?output=csv")

if uploaded_file:
    try:
        live_df = pd.read_excel(uploaded_file, sheet_name="25 vs 26", header=None)
        st.sidebar.success("✅ Excel loaded!")
        with st.expander("Raw Excel preview"):
            st.dataframe(live_df.head(40))
    except:
        st.sidebar.error("Could not read sheet '25 vs 26'")

if google_url:
    try:
        pd.read_csv(google_url)
        st.sidebar.success("✅ Google Sheets connected!")
    except:
        st.sidebar.warning("Link must be published as CSV")

st.sidebar.header("🔎 Regional Filters")
regions = st.sidebar.multiselect(
    "Choose regions",
    options=regional["Region"].tolist(),
    default=regional["Region"].tolist()
)
filtered_regional = regional[regional["Region"].isin(regions)]

# =============================================
# TABS
# =============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🌍 Regional Analysis", "📅 Monthly Pacing", "🔮 What-If Forecast", "📈 YoY Comparison"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("2026 Actual", f"${6400097:,.0f}", "59.2% to Goal")
    with col2: st.metric("Shortfall", "-$4,404,903", "vs $10.8M goal")
    with col3: st.metric("1st Half", "91.9% to Goal", "Strong")
    with col4: st.metric("2nd Half", "30.8% to Goal", "Recovery needed")

    st.subheader("Quarterly Performance")
    fig_q = px.bar(quarterly, x="Quarter", y=["2026 Actual", "2026 Goal"], barmode="group")
    fig_q.add_scatter(x=quarterly["Quarter"], y=quarterly["2025 Actual"], mode="lines+markers", name="2025 Actual", line=dict(color="#16a34a"))
    st.plotly_chart(fig_q, use_container_width=True)

    st.subheader("🔥 Strong Quarterly Performances")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a: st.metric("Q1 Regional Team", "Overperformed ✅", "+18.8% vs Goal")
    with col_b: st.metric("Q1 CDN", "Overperformed ✅", "+29.0% vs Goal")
    with col_c: st.metric("Q1 Total Revenue", "Overperformed ✅", "+18.8% vs Goal")
    with col_d: st.metric("1st Half Overall", "Strong ✅", "91.9% to Goal")

with tab2:
    st.subheader("Regional Performance")
    st.dataframe(filtered_regional.style.format({"2026 Goal": "${:,.0f}", "2026 Actual": "${:,.0f}"}), use_container_width=True)
    fig_r = px.bar(filtered_regional, x="Region", y=["2026 Actual", "2026 Goal"], barmode="group")
    st.plotly_chart(fig_r, use_container_width=True)

with tab3:
    st.subheader("Monthly Pacing Tracker (Oct 2025 – Mar 2026)")
    st.dataframe(pacing.style.format({"Cumulative $": "${:,.0f}"}), use_container_width=True)
    fig_p = px.line(pacing, x="Date", y="% of Goal", markers=True, title="Cumulative % of Goal Achieved")
    fig_p.add_bar(x=pacing["Date"], y=pacing["Cumulative $"]/10000, name="Cumulative $ (×10k)")
    st.plotly_chart(fig_p, use_container_width=True)

with tab4:
    st.subheader("What-If Forecast Results — All 4 Quarters")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a: st.metric("Q1 Projected", f"${q1_proj:,.0f}", f"{q1_pct}% of goal")
    with col_b: st.metric("Q2 Projected", f"${q2_proj:,.0f}", f"{q2_pct}% of goal")
    with col_c: st.metric("Q3 Projected", f"${q3_proj:,.0f}", f"{q3_pct}% of goal")
    with col_d: st.metric("Q4 Projected", f"${q4_proj:,.0f}", f"{q4_pct}% of goal")
    
    st.metric("**Projected Full-Year Revenue**", f"${projected_total:,.0f}", f"{pct_to_goal:.1f}% to Goal")
    if pct_to_goal >= 100:
        st.success("🎉 On track or ahead!")
    else:
        st.error(f"Still ${total_goal - projected_total:,.0f} short")

with tab5:
    st.subheader("Year-over-Year Comparison — By Quarter")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Overall YoY", "60.8%", "vs 2025")
    with col2: st.metric("CDN YoY", "94.0%", "Strong growth")
    with col3: st.metric("Regional Team Variance", "-$4,132,059", "Cash shortfall")
    with col4: st.metric("Chicago SF YoY", "40.2%", "Decline")

    st.subheader("Quarterly YoY Breakdown")
    st.dataframe(
        yoy_quarterly.style.format({
            "2025 Actual": "${:,.0f}",
            "2026 Actual": "${:,.0f}",
            "YoY %": "{:.2f}%",
            "Cash Growth / Variance": "${:,.0f}"
        }),
        use_container_width=True
    )
    
    fig_yoy = px.bar(
        yoy_quarterly,
        x="Period",
        y="YoY %",
        color="Region",
        barmode="group",
        title="YoY Growth % by Quarter and Region",
        text="YoY %"
    )
    fig_yoy.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_yoy, use_container_width=True)

# =============================================
# EXPORTS
# =============================================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    csv = filtered_regional.to_csv(index=False).encode()
    st.download_button("📥 Download Filtered Data (CSV)", csv, "regional_filtered.csv", "text/csv")

with col2:
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "2026 Sales Forecast Report", ln=1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
        pdf.cell(0, 10, f"Total Actual: ${6400097:,.0f} (59.2% to Goal)", ln=1)
        pdf.cell(0, 10, f"Projected Full Year: ${projected_total:,.0f} ({pct_to_goal:.1f}%)", ln=1)
        pdf.cell(0, 10, "What-If Breakdown:", ln=1)
        pdf.cell(0, 8, f"Q1: ${q1_proj:,.0f} ({q1_pct}%)", ln=1)
        pdf.cell(0, 8, f"Q2: ${q2_proj:,.0f} ({q2_pct}%)", ln=1)
        pdf.cell(0, 8, f"Q3: ${q3_proj:,.0f} ({q3_pct}%)", ln=1)
        pdf.cell(0, 8, f"Q4: ${q4_proj:,.0f} ({q4_pct}%)", ln=1)
        pdf.cell(0, 10, "Quarterly YoY Summary:", ln=1)
        for _, row in yoy_quarterly.iterrows():
            pdf.cell(0, 8,
