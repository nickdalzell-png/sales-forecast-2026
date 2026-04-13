import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

st.set_page_config(page_title="2026 Sales Forecast", layout="wide")
st.title("2026 Sales Forecast Dashboard")
st.caption("Live from your Excel file")

st.sidebar.header("Live Data")
uf = st.sidebar.file_uploader("Upload xlsx", type=["xlsx"])

if uf:
    try:
        df = pd.read_excel(uf, sheet_name="25 vs 26 ", header=None)
        st.sidebar.success("Excel loaded!")
        q = pd.DataFrame({
            "Quarter": ["Q1","Q2","Q3","Q4"],
            "2025 Actual": df.iloc[1:5,1].values,
            "2026 Actual": df.iloc[1:5,2].values,
            "Goal": df.iloc[1:5,3].values
        })
    except:
        st.sidebar.warning("Using default data")
        q = pd.DataFrame({
            "Quarter": ["Q1","Q2","Q3","Q4"],
            "2025 Actual": [2166506,2773441,2621216,2970993],
            "2026 Actual": [2500378,2537639,1367351,717692],
            "Goal": [2105000,2912500,2777500,3010000]
        })
else:
    q = pd.DataFrame({
        "Quarter": ["Q1","Q2","Q3","Q4"],
        "2025 Actual": [2166506,2773441,2621216,2970993],
        "2026 Actual": [2500378,2537639,1367351,717692],
        "Goal": [2105000,2912500,2777500,3010000]
    })

r = pd.DataFrame({
    "Region": ["Overall","CDN","Boston","NYC","Malls","Chicago SF"],
    "Goal": [10805000,5795000,75000,100000,90000,1818959],
    "Actual": [6400097,4238745,93840,237780,7267,0]
})

st.sidebar.header("What-If 4Q")
q1p = st.sidebar.slider("Q1 %", 0, 200, 119, step=1)
q2p = st.sidebar.slider("Q2 %", 0, 200, 73, step=1)
q3p = st.sidebar.slider("Q3 %", 0, 200, 51, step=1)
q4p = st.sidebar.slider("Q4 %", 0, 200, 24, step=1)

q1_proj = q["Goal"][0] * q1p / 100
q2_proj = q["Goal"][1] * q2p / 100
q3_proj = q["Goal"][2] * q3p / 100
q4_proj = q["Goal"][3] * q4p / 100
total_proj = q1_proj + q2_proj + q3_proj + q4_proj
total_goal = q["Goal"].sum()
pct_to_goal = (total_proj / total_goal) * 100

h1_actual = q["2026 Actual"].iloc[0:2].sum()
h1_goal = q["Goal"].iloc[0:2].sum()
h1_pct = (h1_actual / h1_goal * 100)
h2_actual = q["2026 Actual"].iloc[2:4].sum()
h2_goal = q["Goal"].iloc[2:4].sum()
h2_pct = (h2_actual / h2_goal * 100)

yoy_region = ["Regional Team"]*4 + ["CDN"]*2 + ["Chicago SF"]*4 + ["Malls"]*4 + ["NYC"]*4 + ["Boston"]*4
yoy_period = ["Q1","Q2","Q3","Q4"] + ["H1","H2"] + ["Q1","Q2","Q3","Q4"]*4
yoy_2025 = [2166506,2773441,2621216,2970993,2661466,2869271,763087,1281712,1193128,1293456,30685,14399,15080,29325,67816,34200.16,87182,24794,89940,374,17,80500]
yoy_2026 = [2500378,2537639,1367351,717692,3044271,1403808,775074,927669,494178,135671,42634,145067,25596,24483,51000,42840,0,0]
yoy_cash = [-4132059,-658369,-1552155,-2255675,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

yoy = pd.DataFrame({
    "Region": yoy_region,
    "Period": yoy_period,
    "2025": yoy_2025,
    "2026": yoy_2026,
    "Cash": yoy_cash
})
yoy["YoY"] = (yoy["2026"] / yoy["2025"] * 100).round(2)

tabs_list = st.tabs(["Overview", "Regional", "What-If", "YoY"])
tab1 = tabs_list[0]
tab2 = tabs_list[1]
tab3 = tabs_list[2]
tab4 = tabs_list[3]

with tab1:
    st.subheader("Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("2026 Total Actual", f"${q['2026 Actual'].sum():,.0f}", f"{pct_to_goal:.1f}% to Goal")
    with c2: st.metric("Total Goal", f"${total_goal:,.0f}")
    with c3: st.metric("1st Half", f"{h1_pct:.1f}%", "Strong")
    with c4: st.metric("2nd Half", f"{h2_pct:.1f}%", "Needed")

    st.subheader("Quarterly Performance")
    fig = px.bar(q, x="Quarter", y=["2026 Actual", "Goal"], barmode="group")
    fig.add_scatter(x=q["Quarter"], y=q["2025 Actual"], mode="lines+markers", name="2025 Actual")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Strong Quarterly Performances")
    ca, cb, cc, cd = st.columns(4)
    with ca: st.metric("Q1 Regional", "Overperformed", "+18.8%")
    with cb: st.metric("Q1 CDN", "Overperformed", "+29.0%")
    with cc: st.metric("Q1 Total", "Overperformed", "+18.8%")
    with cd: st.metric("1st Half", "Strong", "91.9%")

with tab2:
    st.subheader("Regional Actual vs Goal")
    st.dataframe(r.style.format({"Goal": "${:,.0f}", "Actual": "${:,.0f}"}), use_container_width=True)

with tab3:
    st.subheader("What-If Forecast - All 4 Quarters")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Q1 Projected", f"${q1_proj:,.0f}", f"{q1p}%")
    with c2: st.metric("Q2 Projected", f"${q2_proj:,.0f}", f"{q2p}%")
    with c3: st.metric("Q3 Projected", f"${q3_proj:,.0f}", f"{q3p}%")
    with c4: st.metric("Q4 Projected", f"${q4_proj:,.0f}", f"{
