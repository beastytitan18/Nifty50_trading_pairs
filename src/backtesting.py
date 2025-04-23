import pandas as pd
import numpy as np
from numba import jit
from typing import Dict

@jit(nopython=True)
def calculate_positions(zscore: np.ndarray, entry_z: float, exit_z: float) -> np.ndarray:
    positions = np.zeros_like(zscore)
    for i in range(1, len(zscore)):
        if positions[i-1] == 0:
            if zscore[i] < -entry_z:
                positions[i] = 1  # Long spread
            elif zscore[i] > entry_z:
                positions[i] = -1  # Short spread
        else:
            if ((positions[i-1] == 1 and zscore[i] > -exit_z) or 
                (positions[i-1] == -1 and zscore[i] < exit_z)):
                positions[i] = 0
            else:
                positions[i] = positions[i-1]
    return positions

def backtest_pair(
    price_a: pd.Series,
    price_b: pd.Series,
    beta: float,
    entry_z: float = 1.5,
    exit_z: float = 0.5,
    cost_rate: float = 0.001,
    book_size: float = 1_000_000
) -> Dict[str, pd.Series]:
    """Realistic backtest with proper position sizing and P&L"""
    # Calculate spread and z-score
    spread = price_a - beta * price_b
    zscore = (spread - spread.mean()) / spread.std()
    
    # Generate positions
    positions = calculate_positions(zscore.values, entry_z, exit_z)
    
    # Calculate dollar quantities
    a_quantity = np.round((book_size / price_a) * positions)
    b_quantity = np.round((-book_size * beta / price_b) * positions)
    
    # Calculate P&L
    pnl = np.zeros_like(positions)
    prev_position = 0
    for i in range(1, len(positions)):
        # Price changes
        a_return = (price_a.iloc[i] - price_a.iloc[i-1]) / price_a.iloc[i-1]
        b_return = (price_b.iloc[i] - price_b.iloc[i-1]) / price_b.iloc[i-1]
        
        # Position P&L
        pnl[i] = (a_quantity[i-1] * price_a.iloc[i-1] * a_return + 
                 b_quantity[i-1] * price_b.iloc[i-1] * b_return)
        
        # Transaction costs
        if positions[i] != positions[i-1]:
            pnl[i] -= cost_rate * book_size * abs(positions[i] - positions[i-1])
    
    return {
        'dates': price_a.index,
        'positions': pd.Series(positions, index=price_a.index),
        'a_quantity': pd.Series(a_quantity, index=price_a.index),
        'b_quantity': pd.Series(b_quantity, index=price_a.index),
        'pnl': pd.Series(np.cumsum(pnl), index=price_a.index),
        'daily_pnl': pd.Series(pnl, index=price_a.index),
        'zscore': pd.Series(zscore, index=price_a.index),
        'spread': pd.Series(spread, index=price_a.index)
    }