import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scipy.optimize import linprog

workspace_root = Path(__file__).resolve().parents[1]
sys.path.extend([str(workspace_root / "python"), str(workspace_root / "sql")])

from data_pipeline import fetch_and_process
from db_utils import load_summary_from_db, save_to_sqlite

st.title("Portfolio Allocation Optimizer")

st.markdown(
    "Use this app to enter tickers, fetch monthly price data, save it to SQLite, and run the portfolio optimizer."
)

with st.form(key="fetch_form"):
    tickers_input = st.text_input(
        "Tickers (comma-separated)", value="", placeholder="e.g. SPY, IWM, TLT"
    )
    start_date = st.date_input("Start Date", value=pd.to_datetime("2024-05-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2026-05-31"))
    risk_limit = st.slider("Risk Limit", 0.01, 0.20, 0.03, 0.001)
    max_allocation = st.slider("Max Allocation Per ETF", 0.05, 0.80, 0.30, 0.05)
    investment_amount = st.number_input("Investment Amount", min_value=1, value=100000)
    run_pipeline = st.form_submit_button("Fetch Data and Optimize")

summary = None

if run_pipeline:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]

    if len(tickers) < 2:
        st.warning("Please enter at least two tickers separated by commas.")
    else:
        with st.spinner("Fetching data and saving to database..."):
            prices, returns, summary = fetch_and_process(
                tickers,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            )
            save_to_sqlite(prices, returns, summary)

        st.success("Data fetched and saved successfully.")
        st.subheader("Fetched ETF Summary")
        st.dataframe(summary)

if summary is None:
    try:
        summary = load_summary_from_db()
        st.subheader("Loaded Summary from existing SQLite database")
        st.dataframe(summary)
    except Exception:
        summary_path = workspace_root / "data" / "processed" / "summary_table.csv"
        if summary_path.exists():
            summary = pd.read_csv(summary_path)
            st.subheader("Loaded Summary from existing CSV")
            st.dataframe(summary)
        else:
            st.info("Enter tickers and press the button to fetch data and create the dashboard.")

if summary is not None and len(summary) >= 2:
    assets = summary["Asset"].tolist()
    returns = summary["Expected_Return"].values
    risk = summary["Risk"].values
    n = len(assets)

    c = -returns
    A_eq = [[1.0] * n]
    b_eq = [1.0]
    A_ub = [risk.tolist() if hasattr(risk, "tolist") else risk]
    b_ub = [risk_limit]
    bounds = [(0, max_allocation) for _ in range(n)]

    result = linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs",
    )

    if result.success:
        allocation = result.x
        output = pd.DataFrame(
            {
                "Asset": assets,
                "Expected_Return": returns,
                "Risk": risk,
                "Allocation": allocation,
                "Dollar_Allocation": allocation * investment_amount,
            }
        )

        expected_return = float((returns * allocation).sum())
        portfolio_risk = float((risk * allocation).sum())

        st.subheader("Optimized Allocation")
        st.dataframe(output)
        st.metric("Expected Monthly Return", f"{expected_return:.2%}")
        st.metric("Portfolio Risk", f"{portfolio_risk:.2%}")

        fig, ax = plt.subplots()
        ax.bar(output["Asset"], output["Allocation"], color="#4c72b0")
        ax.set_ylabel("Allocation")
        ax.set_xlabel("Asset")
        ax.set_title("Optimized Portfolio Allocation")
        ax.set_ylim(0, 1)
        st.pyplot(fig)
    else:
        st.error("No feasible solution found. Try increasing the risk limit or max allocation.")
