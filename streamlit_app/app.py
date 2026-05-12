import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.title("Portfolio Allocation Optimizer")

summary = pd.read_csv("data/processed/summary_table.csv")

st.subheader("ETF Summary")
st.dataframe(summary)

risk_limit = st.slider("Risk Limit", 0.01, 0.06, 0.03, 0.001)
max_allocation = st.slider("Max Allocation Per ETF", 0.10, 0.60, 0.30, 0.05)
investment_amount = st.number_input("Investment Amount", value=100000)

assets = summary["Asset"].tolist()
returns = summary["Expected_Return"].values
risk = summary["Risk"].values
n = len(assets)

# scipy minimizes, so multiply returns by -1 to maximize
c = -returns

A_eq = [[1] * n]
b_eq = [1]

A_ub = [risk]
b_ub = [risk_limit]

bounds = [(0, max_allocation) for _ in range(n)]

result = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method="highs"
)

if result.success:
    allocation = result.x

    output = pd.DataFrame({
        "Asset": assets,
        "Expected_Return": returns,
        "Risk": risk,
        "Allocation": allocation,
        "Dollar_Allocation": allocation * investment_amount
    })

    expected_return = sum(returns * allocation)
    portfolio_risk = sum(risk * allocation)

    st.subheader("Optimized Allocation")
    st.dataframe(output)

    st.metric("Expected Monthly Return", f"{expected_return:.2%}")
    st.metric("Portfolio Risk", f"{portfolio_risk:.2%}")

    fig, ax = plt.subplots()
    ax.bar(output["Asset"], output["Allocation"])
    ax.set_ylabel("Allocation")
    ax.set_title("Optimized Portfolio Allocation")
    st.pyplot(fig)

else:
    st.error("No feasible solution found. Try increasing the risk limit or max allocation.")
