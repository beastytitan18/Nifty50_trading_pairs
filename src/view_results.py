import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import numpy as np

RESULTS_DIR = "results"

def compute_metrics(df, n_pairs=5, capital_per_pair=1_000_000, risk_free_rate=0.06):
    """Compute portfolio performance metrics from a DataFrame, with risk-free rate."""
    if 'yearly_pnl' in df:
        daily_pnl = df['yearly_pnl']
    elif 'daily_pnl' in df:
        daily_pnl = df['daily_pnl']
    else:
        return {}

    total_capital = n_pairs * capital_per_pair
    daily_return = daily_pnl / total_capital
    rf_daily = (1 + risk_free_rate) ** (1/252) - 1

    # Sharpe with risk-free rate
    excess_daily_return = daily_return - rf_daily
    sharpe = (excess_daily_return.mean() / excess_daily_return.std()) * np.sqrt(252) if excess_daily_return.std() > 0 else np.nan

    total_return = 100 * daily_pnl.sum() / total_capital
    n_years = (df['date'].iloc[-1] - df['date'].iloc[0]).days / 365.25
    annualized_return = 100 * (daily_pnl.sum() / total_capital) / n_years if n_years > 0 else np.nan

    # Add max drawdown (use cumulative_pnl if available)
    if 'cumulative_pnl' in df:
        max_dd = compute_max_drawdown(df['cumulative_pnl'])
    else:
        max_dd = np.nan
    calmar = annualized_return / abs(max_dd) if max_dd and abs(max_dd) > 1e-6 else np.nan
    if 'position' in df:
        num_trades = count_num_trades(df['position'])
    else:
        num_trades = None
    return {
        "Total Return (%)": total_return,
        "Annualized Sharpe": sharpe,
        "Annualized Return (%)": annualized_return,
        "Max Drawdown (%)": max_dd,
        "Calmar Ratio": calmar,
        "Number of Trades" : num_trades,
        "Period": f"{df['date'].iloc[0].strftime('%Y-%m-%d')} to {df['date'].iloc[-1].strftime('%Y-%m-%d')}"
    }
def count_num_trades(position_series):
    """
    Counts the number of round-trip trades (entry and exit) from a position series.
    A trade is counted when the position changes from 0 to nonzero (entry) and back to 0 (exit).
    """
    positions = position_series.values
    # Entry: 0 -> 1 or -1, Exit: 1 or -1 -> 0
    entries = ((np.roll(positions, 1) == 0) & (positions != 0))
    exits = ((np.roll(positions, 1) != 0) & (positions == 0))
    # The number of trades is the number of exits (round-trips)
    return int(np.sum(exits))

def get_pair_files():
    return sorted([f for f in os.listdir(RESULTS_DIR) if f.endswith('.csv') and '_yearly_pnl' not in f and 'final_portfolio_pnl' not in f])

def compute_max_drawdown(series):
    """
    Compute max drawdown as a percentage of peak cumulative PnL.
    Assumes series starts at 0 (pure PnL, not portfolio value).
    Returns 0.0 if no positive peak is reached.
    """
    peak = np.maximum.accumulate(series)
    # Avoid division by zero: mask where peak is zero
    valid = peak > 0
    drawdown = np.zeros_like(series, dtype=float)
    drawdown[valid] = (peak[valid] - series[valid]) / peak[valid]
    max_dd = np.max(drawdown) if np.any(valid) else 0.0
    return max_dd * 100

def get_yearly_files():
    return sorted([f for f in os.listdir(RESULTS_DIR) if '_yearly_pnl.csv' in f])

def load_pair_df(filename):
    df = pd.read_csv(os.path.join(RESULTS_DIR, filename))
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_yearly_df(filename):
    df = pd.read_csv(os.path.join(RESULTS_DIR, filename))
    df['date'] = pd.to_datetime(df['date'])
    return df

def load_aggregated_df():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "final_portfolio_pnl.csv"))
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_line_chart(df, y_col, title, name, color, width=3):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['date'], y=df[y_col],
        mode='lines', name=name,
        line=dict(width=width, color=color)
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Date", yaxis_title="Cumulative PnL",
        template="plotly_white"
    )
    return fig

def display_metrics(metrics):
    st.markdown("### Performance Metrics")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col1.metric("Total Return (%)", f"{metrics['Total Return (%)']:.2f}")
    col2.metric("Annualized Sharpe", f"{metrics['Annualized Sharpe']:.2f}")
    col3.metric("Annualized Return (%)", f"{metrics['Annualized Return (%)']:.2f}")
    col4.metric("Max Drawdown (%)", f"{metrics['Max Drawdown (%)']:.2f}")
    col5.metric("Calmar Ratio", f"{metrics['Calmar Ratio']:.2f}")
    col6.metric("Number of Trades", f"{metrics.get('Number of Trades', 'N/A')}")
    st.markdown(f"**Period:** {metrics['Period']}")

def main():
    st.set_page_config(page_title="Pairs Trading Results", layout="wide")
    st.markdown(
    "<h1 style='text-align: center; color: #F8F8F8;'>Pairs Trading Backtest Results</h1>",
    unsafe_allow_html=True
)
    st.markdown(
    "<div style='text-align: center; color: #D3D3D3;'></div>",
    unsafe_allow_html=True
)
    st.sidebar.title("Navigation")
    view = st.sidebar.radio(
    "Navigation",
    ["Methodology", "Aggregated Portfolio", "Pairwise PnL", "Yearly Portfolio"],
    index=1
)   
    if view == "Methodology":
        st.markdown("# 📚 Methodology")
        st.markdown(r"""
    This repository outlines a pairs trading strategy applied to the Nifty50 universe. The strategy focuses on identifying cointegrated stock pairs and trading on the mean reversion of their spread.

    ## Strategy Overview

    1.  **Pair Selection & Cointegration Testing Universe**:
        * Each year, the Nifty50 universe is reconstituted to avoid survivorship bias.

    2.  **Correlation Filter**:
        * All possible stock pairs are filtered for high absolute correlation (default ≥ 0.7) on daily closing prices.

    3.  **Cointegration Test**:
        * For each highly correlated pair, the Engle-Granger two-step method is used:
            * **Step 1: Estimate hedge ratio (β) via OLS regression:**
            
                $$
                \text{Stock}_A = \alpha + \beta \cdot \text{Stock}_B + \epsilon
                $$
            
            * **Step 2: Augmented Dickey-Fuller (ADF) test:**

                $$
                \Delta y_t = \alpha + \beta t + \gamma y_{t-1} + \sum_{i=1}^p \delta_i \Delta y_{t-i} + \epsilon_t
                $$

    4.  **Selection**:
        * Pairs with ADF p-value < 0.05 are considered cointegrated and eligible for trading.

    5.  **Spread & Z-Score Calculation**:
        * **Spread**: For each pair, the spread is computed as:
        
            $$
            Spread_t = Stock_A - \beta \cdot Stock_B
            $$
        
        * **Z-Score Normalization**: The spread is normalized to a z-score:
        
            $$
            Z_t = \frac{Spread_t - \mu_{spread}}{\sigma_{spread}}
            $$
            

    6.  **Trading Strategy**:
        * **Entry Signals**:
            * **Long Spread**: Enter when $Z_t < -1.5$ (Buy Stock A, Sell $\beta$ shares of Stock B).
            * **Short Spread**: Enter when $Z_t > +1.5$ (Sell Stock A, Buy $\beta$ shares of Stock B).
        * **Exit Signals**:
            * **Close Position**: Exit when $|Z_t| < 0.15$ (Spread crosses the mean).
        * **Position Sizing**: Fixed notional capital per pair (e.g., ₹1,000,000), with quantities dynamically calculated based on prices and hedge ratio.
        * **Transaction Costs**: Realistic transaction costs are applied to each trade.

    7.  **Benchmarking**:
        * For each stock in a traded pair, a buy-and-hold PnL is computed by investing ₹500,000 in each leg at the start of the year and liquidating at year-end. This provides a direct performance benchmark against the pairs trading strategy.

    8.  **Portfolio Construction & Aggregation**:
        * **Top Pairs**: Each year, the top 5 cointegrated pairs (lowest p-value) are selected and traded independently.
        * **Yearly Aggregation**: Daily PnL from all pairs is summed to form the yearly portfolio PnL.
        * **Final Portfolio**: Yearly portfolios are chained together to form a continuous, multi-year cumulative PnL.

    9.  **Performance Analytics**:
        * Metrics: Total return, annualized return, Sharpe ratio, and period are computed for each pair, yearly portfolio, and the aggregated portfolio.

    10. **Visualization**:
        * Interactive dashboards (Streamlit + Plotly) allow exploration of pairwise, yearly, and aggregated results, including buy-and-hold benchmarks.
        """, unsafe_allow_html=True)
        st.stop()

    if view == "Pairwise PnL":
        pair_files = get_pair_files()
        pair = st.sidebar.selectbox("Select Pair", pair_files)
        df = load_pair_df(pair)
        fig = plot_line_chart(df, 'cumulative_pnl', f"Cumulative PnL: {pair}", pair, '#636EFA', width=2)
        if 'bh_pnl_a' in df.columns and 'bh_pnl_b' in df.columns:
        # Show as horizontal lines for final PnL
            bh_pnl_a = df['bh_pnl_a'].iloc[0] if not df['bh_pnl_a'].isnull().all() else None
            bh_pnl_b = df['bh_pnl_b'].iloc[0] if not df['bh_pnl_b'].isnull().all() else None
            if bh_pnl_a is not None:
                fig.add_hline(y=bh_pnl_a, line_dash="dot", line_color="#EF553B", 
                            annotation_text="Buy & Hold A", annotation_position="top left")
            if bh_pnl_b is not None:
                fig.add_hline(y=bh_pnl_b, line_dash="dot", line_color="#00CC96", 
                            annotation_text="Buy & Hold B", annotation_position="bottom left")

        st.plotly_chart(fig, use_container_width=True)
        num_trades = count_num_trades(df['position'])
        metrics = compute_metrics(df, n_pairs=1)
        metrics["Number of Trades"] = num_trades
        display_metrics(metrics)
        with st.expander("ℹ️ **Metric Definitions**", expanded=False):
            st.markdown("""
- **Total Return (%):**  
  Total profit or loss as a percentage of total capital deployed over the period.

- **Annualized Sharpe:**  
  Measures risk-adjusted return.  
  $$\\text{Sharpe Ratio} = \\frac{\\text{Mean Daily Return} - \\text{Risk-Free Rate}}{\\text{Std Dev of Daily Return}} \\times \\sqrt{252}$$

- **Annualized Return (%):**  
  Total return scaled to a yearly rate.

- **Max Drawdown (%):**  
  Largest observed drop from a peak to a trough in cumulative PnL, as a percentage of the peak.

- **Calmar Ratio:**  
  $$\\text{Calmar Ratio} = \\frac{\\text{Annualized Return}}{|\\text{Max Drawdown}|}$$  
  Higher values indicate better risk-adjusted performance.

- **Number of Trades:**  
  The number of round-trip trades (entry and exit) executed in the period.
    """)

    elif view == "Yearly Portfolio":
        yearly_files = get_yearly_files()
        years = [f.split('_')[0] for f in yearly_files]
        year = st.sidebar.selectbox("Select Year", years)

        # Find all pair files for the selected year
        pair_files = sorted([f for f in os.listdir(RESULTS_DIR)
                            if f.startswith(year + "_") and f.endswith(".csv") and "yearly_pnl" not in f])

        color_palette = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
        fig = go.Figure()
        pair_dfs = []
        total_trades = 0
        for i, pair_file in enumerate(pair_files):
            pair_df = pd.read_csv(os.path.join(RESULTS_DIR, pair_file))
            pair_df['date'] = pd.to_datetime(pair_df['date'])
            pair_name = pair_file.replace(f"{year}_", "").replace(".csv", "")
            fig.add_trace(go.Scatter(
                x=pair_df['date'],
                y=pair_df['cumulative_pnl'],
                mode='lines',
                name=pair_name,
                line=dict(width=3, color=color_palette[i % len(color_palette)]),
                opacity=0.4,
                hovertemplate=f"<b>{pair_name}</b><br>Date: %{{x}}<br>Cum. PnL: %{{y:.2f}}<extra></extra>"
            ))
            pair_dfs.append(pair_df)
            # Count trades for this pair
            if 'position' in pair_df:
                total_trades += count_num_trades(pair_df['position'])

        # Compute average cumulative PnL across all 5 pairs
        for df in pair_dfs:
            df['date'] = pd.to_datetime(df['date'])
        avg_df = pd.DataFrame({'date': pair_dfs[0]['date']})
        avg_df['avg_cumulative_pnl'] = np.mean([df['cumulative_pnl'].values for df in pair_dfs], axis=0)

        # Add average line to the chart
        fig.add_trace(go.Scatter(
            x=avg_df['date'],
            y=avg_df['avg_cumulative_pnl'],
            mode='lines',
            name="Average Total Return (5 Pairs)",
            line=dict(width=3, color='#FFD800', dash='dash'),
            opacity=0.9,
            hovertemplate="<b>Average Total Return</b><br>Date: %{x}<br>Avg Cum. PnL: %{y:.2f}<extra></extra>"
        ))

        fig.update_layout(
            title={
                'text': f"Year {year} - Cumulative PnL (Top 5 Pairs)",
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=24, family='Arial Black')
            },
            xaxis_title="Date",
            yaxis_title="Cumulative PnL",
            template="plotly_dark",
            font=dict(family="Arial", size=16, color="#F8F8F8"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            ),
            plot_bgcolor="#22223B",
            paper_bgcolor="#22223B",
            margin=dict(l=40, r=40, t=80, b=40)
        )
        st.markdown(
            "<div style='text-align:center; color:#AAA; font-size:15px;'>Tip: Click a pair name in the legend to highlight it and hide others.</div>",
            unsafe_allow_html=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Aggregate the 5 pairs for metrics
        agg_df = pd.concat(pair_dfs)
        agg_df = agg_df.groupby('date').agg({'daily_pnl': 'sum'}).reset_index()
        agg_df['cumulative_pnl'] = agg_df['daily_pnl'].cumsum()
        metrics = compute_metrics(agg_df)
        metrics["Number of Trades"] = total_trades
        st.markdown("### Performance Metrics")
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        col1.metric("Total Return (%)", f"{metrics['Total Return (%)']:.2f}")
        col2.metric("Annualized Sharpe", f"{metrics['Annualized Sharpe']:.2f}")
        col3.metric("Max Drawdown (%)", f"{metrics['Max Drawdown (%)']:.2f}")
        col4.metric("Calmar Ratio", f"{metrics['Calmar Ratio']:.2f}")
        col5.metric("Number of Trades", f"{metrics.get('Number of Trades', 'N/A')}")
        st.markdown(f"**Period:** {metrics['Period']}")
        with st.expander("ℹ️ **Metric Definitions**", expanded=False):
            st.markdown("""
- **Total Return (%):**  
  Total profit or loss as a percentage of total capital deployed over the period.

- **Annualized Sharpe:**  
  Measures risk-adjusted return.  
  $$\\text{Sharpe Ratio} = \\frac{\\text{Mean Daily Return} - \\text{Risk-Free Rate}}{\\text{Std Dev of Daily Return}} \\times \\sqrt{252}$$


- **Max Drawdown (%):**  
  Largest observed drop from a peak to a trough in cumulative PnL, as a percentage of the peak.

- **Calmar Ratio:**  
  $$\\text{Calmar Ratio} = \\frac{\\text{Annualized Return}}{|\\text{Max Drawdown}|}$$  
  Higher values indicate better risk-adjusted performance.

- **Number of Trades:**  
  The number of round-trip trades (entry and exit) executed in the period.
    """)

    elif view == "Aggregated Portfolio":
        df = load_aggregated_df()
        # Count total trades across all pairs and years
        total_trades = 0
        # Optionally, parse all pair files in results for total trades
        for f in get_pair_files():
            pair_df = load_pair_df(f)
            if 'position' in pair_df:
                total_trades += count_num_trades(pair_df['position'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['cumulative_pnl'],
            mode='lines',
            name="Aggregated Portfolio",
            line=dict(width=2, color='#0099C6'),
            hovertemplate="<b>Aggregated Portfolio</b><br>Date: %{x}<br>Cum. PnL: %{y:.2f}<extra></extra>"
        ))
        fig.update_layout(
            title={
                'text': "Aggregated Portfolio Cumulative PnL (2015-2024)",
                'x': 0.5,
                'xanchor': 'center',
                'font': dict(size=24, family='Roboto, Lato, Segoe UI, Arial', color="#F8F8F8")
            },
            xaxis_title="Date",
            yaxis_title="Cumulative PnL",
            template="plotly_dark",
            font=dict(family="Roboto, Lato, Segoe UI, Arial", size=16, color="#F8F8F8"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=14)
            ),
            plot_bgcolor="#23272E",
            paper_bgcolor="#23272E",
            margin=dict(l=40, r=40, t=80, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        metrics = compute_metrics(df)
        metrics["Number of Trades"] = total_trades
        display_metrics(metrics)
        with st.expander("ℹ️ **Metric Definitions**", expanded=False):
            st.markdown("""
- **Total Return (%):**  
  Total profit or loss as a percentage of total capital deployed over the period.

- **Annualized Sharpe:**  
  Measures risk-adjusted return.  
  $$\\text{Sharpe Ratio} = \\frac{\\text{Mean Daily Return} - \\text{Risk-Free Rate}}{\\text{Std Dev of Daily Return}} \\times \\sqrt{252}$$

- **Annualized Return (%):**  
  Total return scaled to a yearly rate.

- **Max Drawdown (%):**  
  Largest observed drop from a peak to a trough in cumulative PnL, as a percentage of the peak.

- **Calmar Ratio:**  
  $$\\text{Calmar Ratio} = \\frac{\\text{Annualized Return}}{|\\text{Max Drawdown}|}$$  
  Higher values indicate better risk-adjusted performance.

- **Number of Trades:**  
  The number of round-trip trades (entry and exit) executed in the period.
    """)
    st.markdown(
        "<hr><div style='text-align: center; color: #9A8C98;'></div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()