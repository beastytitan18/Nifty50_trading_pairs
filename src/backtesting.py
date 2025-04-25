import pandas as pd
import numpy as np

from typing import Dict


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
    book_size: float = 1_000_000,
    stop_loss_pct: float = 0.10  # 10% stop-loss on book size
) -> Dict[str, pd.Series]:
    # Calculate spread and z-score
    window = 30  # or another reasonable value
    spread = price_a - beta * price_b
    spread_mean = spread.rolling(window).mean().shift(1)
    spread_std = spread.rolling(window).std().shift(1)
    zscore = (spread - spread_mean) / spread_std

    # Generate positions
    positions = calculate_positions(zscore.values, entry_z, exit_z)

    # Calculate dollar quantities
    abs_beta = abs(beta)
    notional_a = book_size / (1 + abs_beta)
    notional_b = book_size * abs_beta / (1 + abs_beta)

    a_quantity = np.round((notional_a / price_a.values) * positions)
    b_quantity = np.round((-np.sign(beta) * notional_b / price_b.values) * positions)

    # Calculate P&L
    pnl = np.zeros_like(positions)
    cumulative_pnl = np.zeros_like(positions)
    stop_loss_triggered = False
    for i in range(1, len(positions)):
        a_return = (price_a.iloc[i] - price_a.iloc[i-1]) / price_a.iloc[i-1]
        b_return = (price_b.iloc[i] - price_b.iloc[i-1]) / price_b.iloc[i-1]

        # Position P&L
        pnl[i] = (a_quantity[i-1] * price_a.iloc[i-1] * a_return +
                  b_quantity[i-1] * price_b.iloc[i-1] * b_return)

        # Transaction costs
        if positions[i] != positions[i-1]:
            pnl[i] -= cost_rate * book_size * abs(positions[i] - positions[i-1])

        cumulative_pnl[i] = cumulative_pnl[i-1] + pnl[i]

        # Stop-loss: force flat if cumulative PnL drops below -stop_loss_pct * book_size
        if not stop_loss_triggered and cumulative_pnl[i] < -stop_loss_pct * book_size:
            positions[i:] = 0
            a_quantity[i:] = 0
            b_quantity[i:] = 0
            stop_loss_triggered = True
            break  # Optionally, stop further trading for this pair

    # Count number of round-trip trades
    exits = ((np.roll(positions, 1) != 0) & (positions == 0))
    num_trades = int(np.sum(exits))

    df = pd.DataFrame({
        'date': price_a.index,
        'price_a': price_a.values,
        'price_b': price_b.values,
        'spread': spread.values,
        'zscore': zscore.values,
        'position': positions,
        'quantity_a': a_quantity,
        'quantity_b': b_quantity,
        'daily_pnl': pnl,
        'cumulative_pnl': cumulative_pnl
    })
    return {"details": df, "num_trades": num_trades}