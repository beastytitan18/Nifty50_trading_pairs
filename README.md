# Nifty 50 Pairs Trading Backtest & Analytics

[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-0099C6?logo=streamlit)](https://nifty50tradingpairs.streamlit.app/)

A robust, bias-aware backtesting and analytics dashboard for pairs trading on the Nifty 50 universe (2015–2024). Explore interactive visualizations, portfolio metrics, and discover the power of systematic trading research.

---

## 🚀 Live Demo

👉 **[Launch the Streamlit Dashboard](https://nifty50tradingpairs.streamlit.app/)**

---

## 📈 Project Highlights

- **Yearly rebalanced universe** to avoid survivorship bias
- **Top 5 pairs selection** per year, realistic transaction costs
- **Portfolio-level aggregation** and performance metrics
- **Interactive, finance-grade dashboard** (Streamlit + Plotly)
- **Clean, modular codebase** for easy extension

---

## 🧑‍💻 How to Run Locally

1. **Clone the repo:**
   ```bash
   git clone https://github.com/beastytitan18/Nifty50_trading_pairs.git
   cd Nifty50_trading_pairs
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the dashboard:**
   ```bash
   streamlit run prod/src/view_results.py
   ```

---

## 🏦 Methodology

- **Universe:** Nifty 50, rebalanced annually (2015–2024)
- **Pair Selection:** Statistical cointegration and spread analysis
- **Backtesting:** Each pair traded with fixed notional, realistic costs, no lookahead
- **Portfolio:** Top 5 pairs per year, aggregated PnL, no capital reuse
- **Metrics:** Total/annualized return, Sharpe ratio, period

---

## 📊 Dashboard Features

- **Pairwise PnL:** Drill down into individual pair performance
- **Yearly Portfolio:** Visualize top 5 pairs for any year, compare interactively
- **Aggregated Portfolio:** See the big picture—portfolio growth and risk metrics

---

## 💡 Why This Project?

- **Bias-aware:** Avoids common pitfalls in quant research
- **Transparent:** All code and data handling is open and reproducible
- **Interactive:** Results are easy to explore and communicate
- **Production-ready:** Modular, readable, and extensible codebase

---

## 📚 Further Ideas

- Add more advanced risk controls or dynamic allocation
- Try other universes or more frequent rebalancing
- Integrate live data for real-time analytics

---

## 👤 Author

Santhosh Venkatesan  
[GitHub](https://github.com/beastytitan18) | [LinkedIn](https://www.linkedin.com/in/santhosh-venkatesan/)

---

> *“In research, clarity is power. In trading, discipline is edge.”*

---

**If you find this useful, please star the repo!**

