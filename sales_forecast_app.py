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
            "2026 Actual": [2500646,2405295,1317182,717692],
            "Goal": [2105000,2912500,2777500,3010000]
        })
else:
    q = pd.DataFrame({
        "Quarter": ["Q1","Q2","Q3","Q4"],
        "2025 Actual": [2166506,2773441,2621216,2970993],
        "2026 Actual": [2500646,2405295,1317182,717692],
        "Goal": [2105000,2912500,2777500,3010000]
    })

r = pd.DataFrame({
    "Region": ["Overall","CDN","Boston","NYC","Malls","Chicago SF"],
    "Goal": [10805000,5795000,75000,100000,90000,181
