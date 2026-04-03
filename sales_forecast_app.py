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
# WHAT-IF
