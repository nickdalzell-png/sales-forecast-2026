import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

st.set_page_config(page_title="2026 Sales Forecast", layout="wide")
st.title("🚀 2026 Sales Forecast Dashboard")
st.caption("Live from your new 2026 sales.xlsx • Sheet \"25 vs 26\"")

q = pd.DataFrame({
    "Quarter": ["Q1","Q2","Q3","Q4"],
    "2025": [2166506,2773441,2621216,2970993],
    "2026": [2500646,2115072,1069061,715318],
    "Goal": [2105000,2912500,2777500,3010000]
})

r = pd.DataFrame({
    "Region": ["Overall","CDN","Boston","NYC","Malls","Chicago SF"],
    "Goal": [10805000,5795000,75000,100000,90000,1818959],
    "Actual": [6400097,4238745,93840,237780,7267,0],
    "Pct": [59.23,73.14,125.12,237.78,8.07,0],
    "YoY": [60.77,93.98,54.93,111.12,8.12,40.22]
})

p = pd.DataFrame({
    "Date": ["Oct 1","Oct 15","Nov 1","Nov 15","Dec 1","Dec 15",
             "Jan 1","Jan 15","Feb 1","Feb 15","Mar 1","Mar 15"],
    "Cum": [656000,800000,861000,1210000,1300000,2370000,
            3930000,4350000,4650000,4920000,5310000,5960000],
    "Pct": [7,8,9,12,12,23,37,41,44,47,51,57]
})

yoy = pd.DataFrame({
    "Region": ["Regional Team"]*4 + ["CDN"]*2 + ["Chicago SF"]*4 + ["Malls"]*4 + ["NYC"]*4 + ["Boston"]*4,
    "Period": ["Q1","Q2","Q3","Q4"] + ["H1","H2"] + ["Q1","Q2","Q3","Q4"]*4,
    "2025": [2166506,2773441,2621216,2970993,2661466,2869271,763087,1281712,1193128,1293456,30685,14399,15080,29325,67816,34200.16,87182,24794,89940,374,17,80500],
    "2026": [2500646,2115072,1069061,715318,2930442,1308303,775342,622433,290011,134679,5299,661,668,639,42634,145067,25596,24483,51000,42840,0,0],
    "Cash": [-4132059,-658369,-1552155,-2255675,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
})
yoy["YoY"] = (yoy["2026"] / yoy["2025"] * 100).round(2)

st.sidebar.header("🔮 What-If (All 4 Quarters)")
q1p = st.sidebar.slider("Q1 %", 0, 200, 119, step=1)
q2p = st.sidebar.slider("Q2 %", 0, 200, 73, step=1)
q3p = st.sidebar.slider("Q3 %", 0, 200, 51, step=1)
q4p = st.sidebar.slider("Q4 %", 0, 200, 24, step=1)

proj = (q["Goal"][0] * q1p / 100) + (q["Goal"][1] * q2p / 100) + (q["Goal"][2] * q3p / 100) + (q["Goal"][3] * q4p / 100)
pct = (proj / 10805000) * 100

st.sidebar.header("🔌 Live Data")
uf = st.sidebar.file_uploader("Upload xlsx", type=["xlsx"])
gu = st.sidebar.text_input("Google Sheets CSV link", placeholder="https://docs.google.com/.../pub?output=csv")

st.sidebar.header("🔎 Filters")
regs = st.sidebar.multiselect("Regions", options=r["Region"].tolist(), default=r["Region"].tolist())
fr = r[r["Region"].isin(regs)]

t1, t2, t3, t4, t5 = st.tabs(["Overview", "Regional", "Pacing", "What-If", "YoY"])

with t1:
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("2026 Actual", f"${6400097:,.0f}", "59.2% to Goal")
    with c2: st.metric("Shortfall", "-$4,404,903", "vs $10.8M goal")
    with c3: st.metric("1st Half", "91.9% to Goal", "Strong")
    with c4: st.metric("2nd Half", "30.8% to Goal", "Recovery needed")

    st.subheader("Quarterly Performance")
    fq = px.bar(q, x="Quarter", y=["2026 Actual", "2026 Goal"], barmode="group")
    fq.add_scatter(x=q["Quarter"], y=q["2025 Actual"], mode="lines+markers", name="2025 Actual", line=dict(color="#16a34a"))
    st.plotly_chart(fq, use_container_width=True)

    st.subheader("🔥 Strong Quarterly Performances")
    ca, cb, cc, cd = st.columns(4)
    with ca: st.metric("Q1 Regional Team", "Overperformed ✅", "+18.8% vs Goal")
    with cb: st.metric("Q1 CDN", "Overperformed ✅", "+29.0% vs Goal")
    with cc: st.metric("Q1 Total Revenue", "Overperformed ✅", "+18.8% vs Goal")
    with cd: st.metric("1st Half Overall", "Strong ✅", "91.9% to Goal")

with t2:
    st.subheader("Regional Performance")
    st.dataframe(fr.style.format({"2026 Goal": "${:,.0f}", "2026 Actual": "${:,.0f}"}), use_container_width=True)
    fr_chart = px.bar(fr, x="Region", y=["2026 Actual", "2026 Goal"], barmode="group")
    st.plotly_chart(fr_chart, use_container_width=True)

with t3:
    st.subheader("Monthly Pacing")
    st.dataframe(p.style.format({"Cumulative $": "${:,.0f}"}), use_container_width=True)
    fp = px.line(p, x="Date", y="% of Goal", markers=True, title="Cumulative % of Goal")
    fp.add_bar(x=p["Date"], y=p["Cumulative $"]/10000, name="Cumulative $ (×10k)")
    st.plotly_chart(fp, use_container_width=True)

with t4:
    st.subheader("What-If Forecast Results")
    ca, cb, cc, cd = st.columns(4)
    with ca: st.metric("Q1", f"${q1_proj:,.0f}", f"{q1p}%")
    with cb: st.metric("Q2", f"${q2_proj:,.0f}", f"{q2p}%")
    with cc: st.metric("Q3", f"${q3_proj:,.0f}", f"{q3p}%")
    with cd: st.metric("Q4", f"${q4_proj:,.0f}", f"{q4p}%")
    st.metric("**Full Year**", f"${projected_total:,.0f}", f"{pct:.1f}% to Goal")
    if pct >= 100:
        st.success("🎉 On track!")
    else:
        st.error(f"Still ${total_goal - projected_total:,.0f} short")

with t5:
    st.subheader("Year-over-Year — By Quarter")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Overall YoY", "60.8%", "vs 2025")
    with c2: st.metric("CDN YoY", "94.0%", "Strong")
    with c3: st.metric("Regional Variance", "-$4.1M", "Cash shortfall")
    with c4: st.metric("Chicago SF YoY", "40.2%", "Decline")

    st.dataframe(yoy.style.format({
        "2025 Actual": "${:,.0f}",
        "2026 Actual": "${:,.0f}",
        "YoY %": "{:.2f}%",
        "Cash Growth / Variance": "${:,.0f}"
    }), use_container_width=True)

    fy = px.bar(yoy, x="Period", y="YoY %", color="Region", barmode="group", title="YoY % by Quarter", text="YoY %")
    fy.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st
