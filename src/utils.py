import pandas as pd
import os

def save_pair_results(results: dict, year: int, symbol_a: str, symbol_b: str):
    """Save individual pair results to CSV"""
    os.makedirs("results", exist_ok=True)
    df = pd.DataFrame({
        'date': results['dates'],
        'price_a': results['price_a'],
        'price_b': results['price_b'],
        'spread': results['spread'],
        'zscore': results['zscore'],
        'position': results['positions'],
        'quantity_a': results['a_quantity'],
        'quantity_b': results['b_quantity'],
        'daily_pnl': results['daily_pnl'],
        'cumulative_pnl': results['pnl']
    })
    df.to_csv(f"results/{year}_{symbol_a}_{symbol_b}.csv", index=False)

def aggregate_yearly_results(year_results: list) -> pd.DataFrame:
    """Combine all pairs' results for a year"""
    all_pnl = pd.DataFrame()
    for result in year_results:
        pair_pnl = pd.Series(
            result['daily_pnl'],
            index=result['dates'],
            name=result['pair']
        )
        all_pnl = pd.concat([all_pnl, pair_pnl], axis=1)
    
    all_pnl['Yearly_PnL'] = all_pnl.sum(axis=1)
    all_pnl['Cumulative_PnL'] = all_pnl['Yearly_PnL'].cumsum()
    return all_pnl

def plot_yearly_results(results: pd.DataFrame, year: int):
    """Generate yearly performance plot"""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    for col in results.columns[:-2]:
        plt.plot(results.index, results[col].cumsum(), alpha=0.4)
    plt.plot(results.index, results['Cumulative_PnL'], 'k-', linewidth=2)
    plt.title(f"{year} Pairs Trading Performance")
    plt.xlabel("Date")
    plt.ylabel("Cumulative P&L ($)")
    plt.grid(True)
    plt.savefig(f"results/{year}_performance.png")
    plt.close()

def plot_final_results(results: pd.DataFrame):
    """Generate final combined performance plot"""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 7))
    plt.plot(results.index, results['Cumulative_PnL'], 'b-', linewidth=2)
    plt.title("10-Year Pairs Trading Performance (2015-2024)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative P&L ($)")
    plt.grid(True)
    plt.savefig("results/final_performance.png")
    plt.show()