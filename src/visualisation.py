import matplotlib.pyplot as plt
import pandas as pd

def plot_backtest_results(
    spread: pd.Series, 
    results: dict, 
    save_path: str = None,
    entry_z: float = 1.0,
    exit_z: float = 0.0
) -> plt.Figure:
    """
    Plot backtest results with 3 subplots:
    1. Spread and positions
    2. Z-score
    3. Cumulative PnL

    Args:
        spread: Original spread series
        results: Output from backtest_pair()
        save_path: Optional path to save figure
        entry_z: Z-score entry threshold
        exit_z: Z-score exit threshold
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    
    # Plot 1: Spread and positions
    spread.plot(ax=ax1, color='blue', label='Spread')
    ax1.plot(results['positions'].index, 
            results['positions'] * spread.max() * 0.8, 
            'r-', alpha=0.3, label='Position')
    ax1.legend()
    ax1.set_title('Spread and Trading Positions')
    
    # Plot 2: Z-score
    zscore = (spread - spread.mean()) / spread.std()
    zscore.plot(ax=ax2, color='green')
    ax2.axhline(entry_z, color='r', linestyle='--')
    ax2.axhline(-entry_z, color='r', linestyle='--')
    ax2.axhline(exit_z, color='g', linestyle='--')
    ax2.axhline(-exit_z, color='g', linestyle='--')
    ax2.set_title('Z-Score')
    
    # Plot 3: PnL
    results['pnl'].plot(ax=ax3, color='purple')
    ax3.set_title('Cumulative PnL')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    
    return fig

import plotly.graph_objs as go

def plot_yearly_results(yearly_pnl, year):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_pnl['date'],
        y=yearly_pnl['cumulative_pnl'],
        mode='lines',
        name=f"{year} Cumulative PnL"
    ))
    fig.update_layout(
        title=f"Year {year} - Cumulative PnL (Top 5 Pairs)",
        xaxis_title="Date",
        yaxis_title="Cumulative PnL"
    )
    fig.show()

def plot_final_results(final_results):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=final_results['date'],
        y=final_results['cumulative_pnl'],
        mode='lines',
        name="Continuous Cumulative PnL"
    ))
    fig.update_layout(
        title="Continuous Cumulative PnL (2015-2024)",
        xaxis_title="Date",
        yaxis_title="Cumulative PnL"
    )
    fig.show()