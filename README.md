# Nifty 50 Cointegration Pairs Trading Research

[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-0099C6?logo=streamlit)](https://nifty50tradingpairs.streamlit.app/)

Backtesting and Analytics suite for **cointegration-based pairs trading** on the Nifty 50 (2015–2024).  
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
### 1. Pair Selection & Cointegration Testing

- **Universe:**  
  Each year, the Nifty50 universe is reconstituted to avoid survivorship bias.

- **Correlation Filter:**  
  All possible stock pairs are filtered for high absolute correlation (default ≥ 0.7) on daily closing prices.

- **Cointegration Test:**  
  For each highly correlated pair, the Engle-Granger two-step method is used:
    - **Step 1:** Estimate hedge ratio (β) via OLS regression:  
      $\text{Stock}_A = \alpha + \beta \cdot \text{Stock}_B + \epsilon$
    - **Step 2:** Test the residuals (spread) for stationarity using the Augmented Dickey-Fuller (ADF) test:  
      $\Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^p \delta_i \Delta y_{t-i} + \epsilon_t$

- **Selection:**  
  Pairs with ADF p-value < 0.05 are considered cointegrated and eligible for trading.

---

### 2. Spread & Z-Score Calculation

- **Spread:**  
  For each pair, the spread is computed as:  
  $Spread_t = Stock_A - \beta \cdot Stock_B$

- **Z-Score Normalization:**  
  The spread is normalized to a z-score using a rolling mean and std (default window=30), calculated with **no lookahead bias**:
  - The rolling window is "warmed up" using the last N days of the previous year, so signals are robust from the first day of each year.
  - Only past data is used for each day's z-score.

  $Z_t = \frac{Spread_t - \mu_{spread}}{\sigma_{spread}}$

---

### 3. Trading Strategy

- **Entry Signals:**
    - **Long Spread:** Enter when $Z_t < -1.5$
    - **Short Spread:** Enter when $Z_t > +1.5$

- **Exit Signals:**
    - **Close Position:** Exit when $|Z_t| < 0.5$ (spread crosses the mean)

- **Position Sizing:**  
  Fixed notional capital per pair (e.g., ₹1,000,000), with quantities dynamically calculated based on prices and hedge ratio.

- **Transaction Costs:**  
  Realistic transaction costs are applied to each trade.

- **Risk Controls:**  
  Stop-loss logic is applied per pair (e.g., close all positions if cumulative PnL drops below a set threshold).

---

### 4. Benchmarking

- For each stock in a traded pair, a buy-and-hold PnL is computed by investing ₹500,000 in each leg at the start of the year and liquidating at year-end.  
  This provides a direct performance benchmark against the pairs trading strategy.

---

### 5. Portfolio Construction & Aggregation

- **Top Pairs:**  
  Each year, the top 5 cointegrated pairs (lowest p-value) are selected and traded independently.

- **Yearly Aggregation:**  
  Daily PnL from all pairs is summed to form the yearly portfolio PnL.

- **Final Portfolio:**  
  Yearly portfolios are chained together to form a continuous, multi-year cumulative PnL.

---

### 6. Performance Analytics & Visualization

- **Metrics:**  
  Total return, annualized return, Sharpe ratio, Calmar ratio, max drawdown, number of trades, and period are computed for each pair, yearly portfolio, and the aggregated portfolio.

- **Visualization:**  
  Interactive dashboards (Streamlit + Plotly) allow exploration of pairwise, yearly, and aggregated results, including buy-and-hold benchmarks.
  - **Metric Definitions:** All metrics are explained in the dashboard for transparency.

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
