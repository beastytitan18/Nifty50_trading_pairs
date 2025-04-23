# src/backtesting.py
import pandas as pd
import numpy as np
from numba import jit

@jit(nopython=True)
def calculate_pnl(spread: np.ndarray, zscore: np.ndarray, 
                 entry_z: float, exit_z: float) -> np.ndarray:
    """Vectorized PnL calculation using Numba."""
    positions = np.zeros_like(spread)
    pnl = np.zeros_like(spread)
    
    for i in range(1, len(spread)):
        if positions[i-1] == 0:
            if zscore[i] < -entry_z:
                positions[i] = 1
            elif zscore[i] > entry_z:
                positions[i] = -1
            else:
                positions[i] = 0
        else:
            if (positions[i-1] == 1 and zscore[i] > -exit_z) or \
               (positions[i-1] == -1 and zscore[i] < exit_z):
                positions[i] = 0
            else:
                positions[i] = positions[i-1]
                
        pnl[i] = positions[i-1] * (spread[i] - spread[i-1])
    
    return pnl.cumsum()

def backtest_pair(spread_series: pd.Series, 
                 entry_z: float = 1.0, 
                 exit_z: float = 0.5) -> pd.DataFrame:
    """Complete backtest for a single pair."""
    zscore = (spread_series - spread_series.mean()) / spread_series.std()
    spread_values = spread_series.values
    
    cumulative_pnl = calculate_pnl(
        spread_values,
        zscore.values,
        entry_z,
        exit_z
    )
    
    return pd.DataFrame({
        'Spread': spread_series,
        'Z-Score': zscore,
        'Position': np.sign(cumulative_pnl),
        'PnL': cumulative_pnl
    }, index=spread_series.index)