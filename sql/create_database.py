import pandas as pd
from pathlib import Path

from db_utils import save_to_sqlite


def main():
    prices = pd.read_csv("data/processed/monthly_prices.csv")
    returns = pd.read_csv("data/processed/monthly_returns.csv")
    summary = pd.read_csv("data/processed/summary_table.csv")

    save_to_sqlite(prices, returns, summary)
    print("SQLite database created successfully.")


if __name__ == "__main__":
    main()

