import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path("data/portfolio_optimizer.db")

prices = pd.read_csv("data/processed/monthly_prices.csv")
returns = pd.read_csv("data/processed/monthly_returns.csv")
summary = pd.read_csv("data/processed/summary_table.csv")

conn = sqlite3.connect(db_path)

prices.to_sql("monthly_prices", conn, if_exists="replace", index=False)
returns.to_sql("monthly_returns", conn, if_exists="replace", index=False)
summary.to_sql("summary_table", conn, if_exists="replace", index=False)

conn.close()

print("SQLite database created successfully.")
