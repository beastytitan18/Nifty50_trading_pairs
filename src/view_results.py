import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os
import numpy as np

RESULTS_DIR = "results"

def compute_metrics(df, n_pairs=5, capital_per_pair=1_000_000):
    """Compute portfolio performance metrics from a DataFrame."""
    if 'yearly_pnl' in df:
        daily_pnl = df['yearly_pnl']
    elif 'daily_pnl' in df:
        daily_pnl = df['daily_pnl']
    else:
        return {}

    total_capital = n_pairs * capital_per_pair
    total_return = 100 * daily_pnl.sum() / total_capital
    sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252) if daily_pnl.std() > 0 else np.nan
    n_years = (df['date'].iloc[-1] - df['date'].iloc[0]).days / 365.25
    annualized_return = 100 * (daily_pnl.sum() / total_capital) / n_years if n_years > 0 else np.nan

    return {
        "Total Return (%)": total_return,
        "Annualized Sharpe": sharpe,
        "Annualized Return (%)": annualized_return,
        "Period": f"{df['date'].iloc[0].strftime('%Y-%m-%d')} to {df['date'].iloc[-1].strftime('%Y-%m-%d')}"
    }

def get_pair_files():
    return sorted([f for f in os.listdir(RESULTS_DIR) if f.endswith('.csv') and '_yearly_pnl' not in f and 'final_portfolio_pnl' not in f])

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
    col1.metric("Total Return (%)", f"{metrics['Total Return (%)']:.2f}")
    col2.metric("Annualized Sharpe", f"{metrics['Annualized Sharpe']:.2f}")
    col3.metric("Annualized Return (%)", f"{metrics['Annualized Return (%)']:.2f}")
    col4.metric("Period", metrics['Period'])

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
    "Select View",
    ["Pairwise PnL", "Yearly Portfolio", "Aggregated Portfolio"],
    index=2
)

    if view == "Pairwise PnL":
        pair_files = get_pair_files()
        pair = st.sidebar.selectbox("Select Pair", pair_files)
        df = load_pair_df(pair)
        fig = plot_line_chart(df, 'cumulative_pnl', f"Cumulative PnL: {pair}", pair, '#636EFA', width=2)
        st.plotly_chart(fig, use_container_width=True)

    elif view == "Yearly Portfolio":
        yearly_files = get_yearly_files()
        years = [f.split('_')[0] for f in yearly_files]
        year = st.sidebar.selectbox("Select Year", years)

        # Find all pair files for the selected year
        pair_files = sorted([f for f in os.listdir(RESULTS_DIR)
                             if f.startswith(year + "_") and f.endswith(".csv") and "yearly_pnl" not in f])

        color_palette = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
        fig = go.Figure()
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
                opacity=0.6,  # Set all lines to semi-transparent
                hovertemplate=f"<b>{pair_name}</b><br>Date: %{{x}}<br>Cum. PnL: %{{y:.2f}}<extra></extra>"
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
        agg_df = pd.concat([pd.read_csv(os.path.join(RESULTS_DIR, f)) for f in pair_files])
        agg_df['date'] = pd.to_datetime(agg_df['date'])
        agg_df = agg_df.groupby('date').agg({'daily_pnl': 'sum'}).reset_index()
        agg_df['cumulative_pnl'] = agg_df['daily_pnl'].cumsum()
        metrics = compute_metrics(agg_df)
        display_metrics(metrics) 
    elif view == "Aggregated Portfolio":
        #displau
        df = load_aggregated_df()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['cumulative_pnl'],
            mode='lines',
            name="Aggregated Portfolio",
            line=dict(width=4, color='#0099C6'),  # Professional blue
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
        display_metrics(metrics)

    st.markdown(
        "<hr><div style='text-align: center; color: #9A8C98;'></div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()