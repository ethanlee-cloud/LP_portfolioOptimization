import yfinance as yf
import pandas as pd
from pathlib import Path


# 1. Settings


tickers = ["SPY", "IEMG", "IWM", "TLT", "SHY", "VCIT"]

start_date = "2024-05-01"
end_date = "2026-05-31"

raw_dir = Path("data/raw")
processed_dir = Path("data/processed")

raw_dir.mkdir(parents=True, exist_ok=True)
processed_dir.mkdir(parents=True, exist_ok=True)


# 2. Fetch data from Yahoo Finance


data = yf.download(
    tickers=tickers,
    start=start_date,
    end=end_date,
    interval="1mo",
    auto_adjust=True,
    progress=False
)

# Use adjusted close prices
prices = data["Close"]


# 3. Clean data


prices = prices.reset_index()

# Make column names cleaner
prices.columns.name = None

# Save monthly prices
prices.to_csv(processed_dir / "monthly_prices.csv", index=False)


# 4. Calculate monthly returns


returns = prices.copy()
returns[tickers] = returns[tickers].pct_change()

returns = returns.dropna()

# Save monthly returns
returns.to_csv(processed_dir / "monthly_returns.csv", index=False)


# 5. Create summary table


summary = pd.DataFrame({
    "Asset": tickers,
    "Expected_Return": returns[tickers].mean().values,
    "Risk": returns[tickers].std().values
})

summary.to_csv(processed_dir / "summary_table.csv", index=False)

print("Data pipeline complete.")
print(summary)
