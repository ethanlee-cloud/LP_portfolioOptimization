import sqlite3
from pathlib import Path

import pandas as pd


def save_to_sqlite(prices, returns, summary, db_path="data/portfolio_optimizer.db"):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        prices.to_sql("monthly_prices", conn, if_exists="replace", index=False)
        returns.to_sql("monthly_returns", conn, if_exists="replace", index=False)
        summary.to_sql("summary_table", conn, if_exists="replace", index=False)
    finally:
        conn.close()


def load_summary_from_db(db_path="data/portfolio_optimizer.db"):
    db_path = Path(db_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query("SELECT * FROM summary_table", conn)
    finally:
        conn.close()
