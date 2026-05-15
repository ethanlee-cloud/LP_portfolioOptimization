# 📈 LP Portfolio Optimizer

An open-source portfolio optimization tool that uses **Linear Programming (LP)** to maximize expected return subject to risk and diversification constraints — no paid tools like Morningstar or Koyfin needed.

Built from an academic project (MSBA 204, Cal State Sacramento) and extended into a fully automated pipeline with a live Streamlit dashboard.

---

## 🚀 Live Demo

> Run locally with the steps below, or deploy to [Streamlit Cloud](https://streamlit.io/cloud) for free.

---

## ✨ Features

- **Auto-fetches & cleans** historical price data from Yahoo Finance via `yfinance`
- **Calculates** expected monthly returns and risk (2× standard deviation) per asset
- **Solves** the LP optimization problem using `scipy` (Python) and `lpSolve` (R)
- **Stores** results in a local SQLite database for auditability and reuse
- **Visualizes** portfolio allocations, scenario comparisons, and sensitivity analysis via Streamlit
- **Scenario analysis** across four risk profiles: Base Case, Conservative, Aggressive, Strict Diversification

---

## 📦 Quick Start

```bash
# 1. Install dependencies
pip install yfinance pandas streamlit scipy matplotlib

# 2. Fetch and clean data
python python/01_fetch_clean_data.py

# 3. Set up the database
python sql/create_database.py

# 4. Launch the Streamlit app
streamlit run streamlit_app/app.py
```

---

## 🧠 How It Works

The model solves the following Linear Program:

**Maximize:** `Z = Σ (Expected Return × Allocation)`

**Subject to:**
| Constraint | Rule |
|---|---|
| Budget | All capital must be fully invested (allocations sum to 100%) |
| Risk | Weighted portfolio risk ≤ threshold (default 3%) |
| Diversification | No single asset exceeds 30% of portfolio |
| Non-negativity | No short selling |

---

## 📊 Example Output (Base Case — 6 ETFs)

| Asset | Expected Return | Risk | Allocation |
|-------|----------------|------|------------|
| SPY   | 1.57%          | 3.53% | **30%** |
| IEMG  | 2.27%          | 4.41% | **30%** |
| SHY   | 0.35%          | 0.44% | **30%** |
| IWM   | 1.58%          | 5.38% | 8.7% |
| VCIT  | 0.53%          | 1.22% | 1.3% |
| TLT   | 0.20%          | 3.07% | 0% |

**Portfolio Expected Monthly Return: 1.40% | Portfolio Risk: 3.00%**

### Sensitivity Scenarios

| Scenario | Return | Risk |
|----------|--------|------|
| Base Case | 1.40% | 3.00% |
| Conservative | 1.25% | 2.50% |
| Aggressive | 1.53% | 3.50% |
| Strict Constraints | 0.87% | 2.20% |

---

## 🗂️ Project Structure

```
LP_portfolioOptimization/
├── python/          # Data fetching, cleaning, LP solver
├── R/               # Original R implementation (lpSolve)
├── sql/             # SQLite database setup and queries
├── streamlit_app/   # Interactive dashboard
├── data/            # Raw and processed CSVs
└── README.md
```


---

## 🔭 Roadmap

This project is actively being developed. Planned improvements:

- [ ] **Modern return models** — replace historical averages with CAPM or Dividend Discount Model
- [ ] **Advanced risk metrics** — incorporate Beta, Max Drawdown, and Value at Risk (VaR)
- [ ] **AI-powered sentiment layer** — use LLMs to analyze financial news and assign sentiment scores as additional LP constraints
- [ ] **Broader asset support** — extend beyond ETFs to individual stocks, crypto, and commodities
- [ ] **Portfolio rebalancing scheduler** — trigger re-optimization when allocations drift beyond a threshold
- [ ] **Streamlit Cloud deployment** — one-click public demo

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Historical returns do not guarantee future performance. Always conduct your own due diligence before making investment decisions.

---

## 📄 License

MIT — free to use, modify, and build upon.

---

## 🙋 Author

**Thanh Ly** — MSBA, Cal State Sacramento  
[GitHub](https://github.com/tqly-builds)
