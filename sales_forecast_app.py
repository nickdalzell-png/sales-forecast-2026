import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

st.set_page_config(page_title="2026 Sales Forecast", layout="wide")
st.title("2026 Sales Forecast Dashboard")
st.caption("From new 2026 sales.xlsx")

q = pd.DataFrame({
    "Q": ["Q1","Q2","Q3","Q4"],
    "2025": [2166506,2773441,2621216,2970993],
    "2026": [2500646,2115072,1069061,715318],
    "Goal": [2105000,2912500,2777500,3010000]
})

r = pd.DataFrame({
    "Region": ["Overall","CDN","Boston","NYC","Malls","Chicago SF"],
    "Goal": [10805000,5795000,75000,100000,90000,1818959],
    "Actual": [6400097,4238745,93840,237780,7267,0]
})

p = pd.DataFrame({
    "Date": ["Oct1","Oct15","Nov1","Nov15","Dec1","Dec15","Jan1","Jan15","Feb1","Feb15","Mar1","Mar15"],
    "Cum": [656000,800000,861000,1210000,1300000,2370000,3930000,4350000,4650000,4920000,5310000,5960000],
    "Pct": [7,8,9,12,12,23,37,41,44,47,51,57]
})

yoy_region = ["Regional Team"]*4 + ["CDN"]*2 + ["Chicago SF"]*4 + ["Malls"]*4 + ["NYC"]*4 + ["Boston"]*4
yoy_period = ["Q1","Q2","Q3","Q4"] + ["H1","H2"] + ["Q1","Q2","Q3","Q4"]*4
yoy_2025 = [2166506,2773441,2621216,2970993,2661466,2869271,763087,1281712,1193128,1293456,30685,14399,15080,29325,67816,34200.16,87182,24794,89940,374,17,80500]
yoy_2026 = [2500646,2115072,1069061,715318,2930442,1308303,775342,622433,290011,134679,5299,661,668,639,42634,145067,25596,24483,51000,42840,0,0]
yoy_cash = [-4132059,-658369,-1552155,-2255675,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

yoy = pd.DataFrame({
    "Region": yoy_region,
    "Period": yoy_period,
    "2025": yoy_2025,
    "2026": yoy_2026,
    "Cash": yoy_cash
})
yoy["YoY"] = (yoy["2026"] / yoy["2025"] * 100).round(2)

st.sidebar.header("What-If 4Q")
q1p = st.sidebar.slider("Q1 %", 0, 200, 119, step=1)
q2p = st.sidebar.slider("Q2 %", 0, 200, 73, step=1)
q3p = st.sidebar.slider("Q3 %", 0, 200, 51, step=1)
q4p = st.sidebar.slider("Q4 %", 0, 200, 24, step=1)

q1_proj = q["Goal"][0] * q1p / 100
q2_proj = q["Goal"][1] * q2p / 100
q3_proj = q["Goal"][2] * q3p / 100
q4_proj = q["Goal"][3] * q4p / 100
proj = q1_proj + q2_proj + q3_proj + q4_proj
pct = (proj / 10805000) * 100

st.sidebar.header("Live Data")
uf = st.sidebar.file_uploader("Upload xlsx", type=["xlsx"])

st.sidebar.header("Filters")
regs = st.sidebar.multiselect("Regions", options=r["Region"].tolist(), default=r["Region"].tolist())
fr = r[r["Region"].isin(regs)]

t1, t2, t3, t4, t5 = st.tabs(["Overview", "Regional", "Pacing", "What-If", "YoY"])

with t1:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("2026 Actual", f"${6400097:,.0f}", "59.2%")
    with c2: st.metric("Shortfall", "-$4.4M", "vs goal")
    with c3: st.metric("1st Half", "91.9%", "Strong")
    with c4: st.metric("2nd Half", "30.8%", "Needed")

    st.subheader("Quarterly Performance")
    fq = px.bar(q, x="Q", y=["2026", "Goal"], barmode="group")
    fq.add_scatter(x=q["Q"], y=q["2025"], mode="lines+markers", name="2025")
    st.plotly_chart(fq, use_container_width=True)

    st.subheader("🔥 Strong Quarterly Performances")
    ca, cb, cc, cd = st.columns(4)
    with ca: st.metric("Q1 Regional Team", "Overperformed ✅", "+18.8% vs Goal")
    with cb: st.metric("Q1 CDN", "Overperformed ✅", "+29.0% vs Goal")
    with cc: st.metric("Q1 Total Revenue", "Overperformed ✅", "+18.8% vs Goal")
    with cd: st.metric("1st Half Overall", "Strong ✅", "91.9% to Goal")
