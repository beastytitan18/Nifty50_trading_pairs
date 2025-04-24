# Nifty 50 Cointegration Pairs Trading Research

[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-0099C6?logo=streamlit)](https://nifty50tradingpairs.streamlit.app/)

A Robust backtesting and analytics suite for **cointegration-based pairs trading** on the Nifty 50 (2015–2024).  
This project demonstrates robust statistical testing, realistic backtesting, and clear portfolio analytics—built for transparency and practical insight.

---

## 🔍 Core Idea

- **Cointegration**: Each year, we scan the Nifty 50 universe for stock pairs whose prices move together in the long run (using the Engle-Granger test).
- **Pairs Trading**: For each selected pair, we trade the spread when it diverges from its mean, betting on mean reversion.
- **Bias Avoidance**: The universe is rebalanced yearly to avoid survivorship bias.
- **Portfolio Construction**: Top 5 cointegrated pairs per year, each traded with fixed capital and realistic costs.

---

## 📊 Dashboard

- **Pairwise PnL**: Inspect any pair’s cumulative profit and loss.
- **Yearly Portfolio**: See all 5 pairs for a year, compare their performance interactively.
- **Aggregated Portfolio**: Track the combined portfolio’s growth and risk.

👉 [Check Results here!](https://nifty50tradingpairs.streamlit.app/)

---

## 🧑‍💻 How to Run

```bash
git clone https://github.com/beastytitan18/Nifty50_trading_pairs.git
cd Nifty50_trading_pairs
pip install -r requirements.txt
streamlit run prod/src/view_results.py
```

---

## 📚 Methodology

- **Statistical Test**: Engle-Granger cointegration test for pair selection.
- **Signal**: Z-score of spread; enter/exit on thresholds.
- **Execution**: Fixed notional per pair, transaction costs, no lookahead.
- **Metrics**: Total/annualized return, Sharpe, period.

---

## 🛠️ Code Structure & Naming

- `spread`: The price difference (or linear combination) between two stocks.
- `positions`: The trading position (+1, -1, or 0) for each day.
- `zscore`: Standardized spread, used for entry/exit signals.
- `pnl`: Daily profit and loss for the pair.
- `cumulative_pnl`: Running total of PnL.
- `yearly_pnl.csv`: Aggregated portfolio PnL for each year.
- `final_portfolio_pnl.csv`: Aggregated portfolio PnL for the full period.

**Tip:**  
For clarity, use explicit variable names like `spread_series`, `pair_positions`, `daily_pnl`, `cumulative_pnl`, etc.  
Group related results in dictionaries or data classes for easier access and maintenance.

---

## 👤 Author

Santhosh Venkatesan  
[GitHub](https://github.com/beastytitan18)

---

> *Cointegration is the backbone of robust pairs trading. This project is about doing it right—statistically, practically, and transparently.*

---

**Star the repo if you find it useful!**
