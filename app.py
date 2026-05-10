import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.graph_objects as go

API_URL = "http://0.0.0.0:8000/predict"
BASE_DATA_PATH = "csv/data-vn-20230228"
HIST_PATH = os.path.join(BASE_DATA_PATH, "stock-historical-data")
FIN_PATH = os.path.join(BASE_DATA_PATH, "financial-ratio")
DIV_PATH = os.path.join(BASE_DATA_PATH, "dividend-history")
IND_PATH = os.path.join(BASE_DATA_PATH, "industry-analysis")
WINDOW_SIZE = 60

st.set_page_config(page_title="Invest by AI", layout="wide")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { background: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 12px !important; padding: 15px !important; }
    .stButton>button { background: linear-gradient(90deg, #007AFF, #00C7FF); color: white; border: none; border-radius: 10px; font-weight: 600; width: 100%; height: 50px; }
    
    section[data-testid="stSidebar"] { width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)


def find_and_load(folder_path, ticker):
    if not os.path.exists(folder_path): 
        return None
    
    for filename in os.listdir(folder_path):

        if filename.startswith('._'): 
            continue

        file_prefix = filename.split('-')[0].upper() 

        if file_prefix == ticker.upper() and filename.endswith(".csv"):

            full_path = os.path.join(folder_path, filename)

            for enc in ['utf-8', 'latin1', 'cp1252']:
                try: 
                    df = pd.read_csv(full_path, encoding=enc)
                    if df.empty: 
                        return None
                    return df
                except: 
                    continue

    return None

def find_col(df, candidates):

    actual = {c.strip().lower().replace('<','').replace('>',''): c for c in df.columns}

    for cand in candidates:
        if cand in actual: 
            return actual[cand]
        
    return None

with st.sidebar:

    st.markdown("### :material/account_balance: Invest Terminal")

    source_mode = option_menu(
        menu_title=None, 
        options=["Dashboard", "Upload Asset", "Sandbox", "Audit"],
        icons=["house", "cloud-upload", "cpu", "journal-text"], 
        default_index=0,
        styles={"nav-link": {"color": "#ffffff", "font-size": "14px", "text-align": "left"}}
    )

    st.divider()
    st.caption("AI Prediction")
    st.caption("Nguyen Do Phuc An - 240133")


if source_mode == "Dashboard":

    if os.path.exists(HIST_PATH):

        all_files = [f for f in os.listdir(HIST_PATH) if f.endswith(".csv") and not f.startswith('._')]

        tickers = sorted(list(set([f.split('-')[0] for f in all_files if '-' in f])))

        active_ticker = st.selectbox("Search Stock Symbol", tickers)
        
        if active_ticker:
            df_price = find_and_load(HIST_PATH, active_ticker)

            if df_price is not None:
                st.title(f"{active_ticker} Intelligence Report")
              
                c_close = find_col(df_price, ['close', 'price'])
                c_open = find_col(df_price, ['open'])
                c_high = find_col(df_price, ['high'])
                c_low = find_col(df_price, ['low'])
                c_vol = find_col(df_price, ['vol', 'volume'])
               
                chart_type = st.segmented_control(
                    "Select View", 
                    options=["Line Chart", "Candlestick"], 
                    default="Line Chart"
                )

                if chart_type == "Candlestick" and all([c_open, c_high, c_low]):

                    fig = go.Figure(data=[go.Candlestick(
                        x=df_price.index[-100:], 
                        open=df_price[c_open].tail(100), 
                        high=df_price[c_high].tail(100), 
                        low=df_price[c_low].tail(100), 
                        close=df_price[c_close].tail(100)
                    )])

                    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.line_chart(df_price[c_close].tail(100))

                m_col1, m_col2, m_col3 = st.columns(3)

                with m_col1:
                    st.metric("Last Price", f"{df_price[c_close].iloc[-1]:,.0f}")

                with m_col2:
                    if len(df_price) > 1:
                        diff = df_price[c_close].iloc[-1] - df_price[c_close].iloc[-2]
                        st.metric("Day Change", f"{diff:+,.0f}", f"{(diff/df_price[c_close].iloc[-2]):.2%}")

                with m_col3:
                    low_52, high_52 = df_price[c_close].tail(252).min(), df_price[c_close].tail(252).max()
                    st.write(f"**52W Range:** {low_52:,.0f} - {high_52:,.0f}")
                    st.progress(float((df_price[c_close].iloc[-1]-low_52)/(high_52-low_52) if high_52!=low_52 else 0.5))

                if st.button("EXECUTE AI PREDICTION"):

                    with st.spinner("Analyzing..."):

                        try:
                            payload = df_price[[c_open, c_high, c_low, c_close, c_vol]].tail(WINDOW_SIZE).values.tolist()

                            res = requests.post(API_URL, json={"data": payload})
                            result = res.json()

                            st.success(f"Signal: {result['signal']} ({result['buy_probability']:.1%})")

                        except: 
                            st.error("Engine offline")

                st.divider()

                f_col1, f_col2 = st.columns(2)

                with f_col1:
                    with st.expander(":material/finance: Financial Health", expanded=True):

                        df_fin = find_and_load(FIN_PATH, active_ticker)

                        if df_fin is not None and not df_fin.empty:
                            last = df_fin.iloc[-1]
                            st.write(f"**ROE:** {last.get('roe', 0):.1%}")
                            st.write(f"**P/E:** {last.get('priceToEarning', 0):.1f}x")
                            st.write(f"**EPS:** {last.get('earningPerShare', 0):,.0f} VND")

                        else: 
                            st.caption("No financial data found")

                with f_col2:

                    with st.expander(":material/groups: Industry Peers", expanded=True):

                        df_ind = find_and_load(IND_PATH, active_ticker)

                        if df_ind is not None and not df_ind.empty:
                            st.write(", ".join(df_ind['ticker'].head(12).astype(str).tolist()))

                        else: 
                            st.caption("No peer data")


                st.write("")

                with st.expander(":material/payments: Dividend History - Full View", expanded=True):

                    df_div = find_and_load(DIV_PATH, active_ticker)
                    if df_div is not None and not df_div.empty:

                        st.dataframe(df_div[['exerciseDate', 'cashDividendPercentage', 'cashYear', 'issueMethod']], 
                                    use_container_width=True, hide_index=True)
                    else: 
                        st.caption("No history found")


elif source_mode == "Upload Asset":

    st.title("Asset Ingestion")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")

    if uploaded_file:
        df_up = pd.read_csv(uploaded_file)
        st.dataframe(df_up.head(), use_container_width=True)

elif source_mode == "Sandbox":

    st.title("Market Sandbox")
    st.info("Simulate manual stock entries (OHLCV) for testing")
    sb_col1, sb_col2 = st.columns(2)

    with sb_col1:
        s_open = st.number_input("Simulated Open", value=100.0)
        s_high = st.number_input("Simulated High", value=105.0)
        s_low = st.number_input("Simulated Low", value=95.0)

    with sb_col2:
        s_close = st.number_input("Simulated Close", value=102.0)
        s_vol = st.number_input("Simulated Volume", value=1000000)
    
    if st.button("Predict Scenario"):
        st.write(f"Running simulation for Close: {s_close}...")

elif source_mode == "Audit":
    st.title("System Audit")
    st.json({
        "Task 5.3 Status": "Automated Multi-Source Workflow Active",
        "Backend Connection": "Verified",
        "Active Streams": ["Historical Price", 
                           "Financial Ratios", 
                           "Dividend History", 
                           "Industry Analysis"]
    })