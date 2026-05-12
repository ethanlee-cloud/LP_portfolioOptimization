from pathlib import Path

from data_pipeline import fetch_and_process


def main():
    tickers = ["SPY", "ORCL", "IWM", "TLT", "AMD", "NVDA"]
    start_date = "2024-05-01"
    end_date = "2026-05-31"

    prices, returns, summary = fetch_and_process(tickers, start_date, end_date)
    print("Data pipeline complete.")
    print(summary)


if __name__ == "__main__":
    main()
