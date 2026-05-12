import yfinance as yf
import pandas as pd
from pathlib import Path


def fetch_prices(tickers, start_date, end_date, interval="1mo"):
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )
    prices = data["Close"]
    prices = prices.reset_index()
    prices.columns.name = None
    return prices


def calculate_returns(prices, tickers):
    returns = prices.copy()
    returns.loc[:, tickers] = returns[tickers].pct_change()
    returns = returns.dropna()
    return returns


def calculate_summary(returns, tickers):
    return pd.DataFrame(
        {
            "Asset": tickers,
            "Expected_Return": returns[tickers].mean().values,
            "Risk": returns[tickers].std().values,
        }
    )


def fetch_and_process(
    tickers,
    start_date,
    end_date,
    raw_dir="data/raw",
    processed_dir="data/processed",
):
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    prices = fetch_prices(tickers, start_date, end_date)
    prices.to_csv(processed_dir / "monthly_prices.csv", index=False)

    returns = calculate_returns(prices, tickers)
    returns.to_csv(processed_dir / "monthly_returns.csv", index=False)

    summary = calculate_summary(returns, tickers)
    summary.to_csv(processed_dir / "summary_table.csv", index=False)

    return prices, returns, summary


if __name__ == "__main__":
    default_tickers = ["SPY", "ORCL", "IWM", "TLT", "AMD", "NVDA"]
    fetch_and_process(default_tickers, "2024-05-01", "2026-05-31")
    print("Data pipeline complete.")
