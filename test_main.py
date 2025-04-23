import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import numpy as np
from src.data_loader import load_price_data, create_price_matrix
from src.cointegration import robust_cointegration_test
from src.backtesting import backtest_pair
# from src.visualisation import plot_backtest_results
import matplotlib.pyplot as plt
import warnings
from itertools import combinations
warnings.filterwarnings('ignore')

nifty50_2015 = [
    "ACC", "AMBUJACEM", "ASIANPAINT", "AXISBANK", "BANKBARODA", "BHEL", "BPCL", "BHARTIARTL",
    "CAIRN", "CIPLA", "COALINDIA", "DLF", "DRREDDY", "GAIL", "GRASIM", "HCLTECH", "HDFC",
    "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "IDFC", "INDUSINDBK",
    "INFY", "ITC", "KOTAKBANK", "LT", "LUPIN", "M&M", "MARUTI", "NTPC", "ONGC", "PNB",
    "POWERGRID", "RELIANCE", "SBIN", "SSLT", "SUNPHARMA", "TATAMOTORS", "TATAPOWER",
    "TATASTEEL", "TCS", "TECHM", "ULTRACEMCO", "VEDL", "WIPRO", "YESBANK", "ZEEL"
]
nifty50_2016 = [
    "ACC", "ADANIPORTS", "AMBUJACEM", "ASIANPAINT", "AXISBANK", "BANKBARODA", "BHEL", "BPCL", "BHARTIARTL",
    "BOSCHLTD", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH", "HDFC",
    "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "IDEA", "INDUSINDBK", "INFY",
    "ITC", "KOTAKBANK", "LT", "LUPIN", "M&M", "MARUTI", "NTPC", "ONGC", "POWERGRID", "RELIANCE",
    "SBIN", "SUNPHARMA", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TCS", "TECHM", "ULTRACEMCO",
    "VEDL", "WIPRO", "YESBANK", "ZEEL"
]
nifty50_2017 = [
    "ACC", "ADANIPORTS", "AMBUJACEM", "ASIANPAINT", "AUROPHARMA", "AXISBANK", "BANKBARODA", "BHEL", "BPCL",
    "BHARTIARTL", "BOSCHLTD", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH",
    "HDFC", "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDPETRO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK",
    "INFY", "ITC", "KOTAKBANK", "LT", "LUPIN", "M&M", "MARUTI", "NTPC", "ONGC", "POWERGRID", "RELIANCE",
    "SBIN", "SUNPHARMA", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TCS", "TECHM", "ULTRACEMCO", "VEDL",
    "WIPRO", "YESBANK", "ZEEL"
]
nifty50_2018 = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH", "HDFC", "HDFCBANK",
    "HEROMOTOCO", "HINDALCO", "HINDPETRO", "HINDUNILVR", "IBULHSGFIN", "ICICIBANK", "INDUSINDBK", "INFY",
    "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "LUPIN", "M&M", "MARUTI", "NTPC", "ONGC", "POWERGRID",
    "RELIANCE", "SBIN", "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS", "TECHM", "TITAN", "ULTRACEMCO",
    "UPL", "VEDL", "WIPRO", "YESBANK", "ZEEL"
]
nifty50_2019 = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH", "HDFC",
    "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY", "IOC",
    "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "LUPIN", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "VEDL", "WIPRO", "ZEEL"
]
nifty50_2020 = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH",
    "HDFC", "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY",
    "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]
nifty50_2021 = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL", "GRASIM", "HCLTECH",
    "HDFC", "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY",
    "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO", "DIVISLAB"
]
nifty50_2022 = [
    "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFC",
    "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY", "IOC",
    "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]
nifty50_2023 = [
    "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFC",
    "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY", "IOC",
    "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC",
    "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TCS",
    "TECHM", "TITAN", "ULTRACEMCO", "UPL", "WIPRO"
]
nifty50_2024 = [
    "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BHARTIARTL", "BPCL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "INDUSINDBK", "INFY", "IOC", "ITC", "JSWSTEEL",
    "KOTAKBANK", "LT", "M&M", "MARUTI", "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "RELIANCE", "SBIN",
    "SHREECEM", "SUNPHARMA", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TCS", "TECHM", "TITAN", "ULTRACEMCO",
    "UPL", "WIPRO"
]



def get_nifty_list_for_year(year):
    return {
        2015: nifty50_2015,
        2016: nifty50_2016,
        2017: nifty50_2017,
        2018: nifty50_2018,
        2019: nifty50_2019,
        2020: nifty50_2020,
        2021: nifty50_2021,
        2022: nifty50_2022,
        2023: nifty50_2023,
        2024: nifty50_2024,
    }[year]

def filter_nifty_list(nifty_list, price_matrix):
    return [s for s in nifty_list if s in price_matrix.columns]

def calculate_half_life(spread):
    """Calculate half-life of mean reversion for optimal lookback period"""
    spread_lag = spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]
    spread_ret = spread - spread_lag
    spread_ret.iloc[0] = spread_ret.iloc[1]
    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_ret, spread_lag2)
    res = model.fit()
    return -np.log(2) / res.params[1]

import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from src.data_loader import load_price_data, create_price_matrix
from src.cointegration import robust_cointegration_test
from src.backtesting import backtest_pair

def yearly_pairs_backtest():
    os.makedirs("results", exist_ok=True)
    all_years = range(2015, 2025)
    yearly_results = []

    for year in all_years:
        print(f"\n=== Processing {year} ===")
        
        # Load data with validation
        try:
            df = load_price_data("data/raw", [year])
            if df.empty:
                print(f"No data for {year}")
                continue
                
            price_matrix = create_price_matrix(df)
            if price_matrix.empty:
                print(f"Empty price matrix for {year}")
                continue
        except Exception as e:
            print(f"Error loading {year} data: {str(e)}")
            continue
            
        # Get valid symbols for year
        try:
            nifty_list = globals()[f"nifty50_{year}"]
            valid_symbols = [
                s for s in nifty_list 
                if s in price_matrix.columns 
                and price_matrix[s].notnull().all()
            ]
            print(f"Found {len(valid_symbols)} valid symbols for {year}")
        except KeyError:
            print(f"No Nifty list found for {year}")
            continue
            
        # Find and test candidate pairs
        candidate_pairs = []
        tested_pairs = set()
        
        for a, b in combinations(valid_symbols, 2):
            pair_key = frozenset({a, b})
            if pair_key in tested_pairs:
                continue
            tested_pairs.add(pair_key)
            
            # Skip if prices contain NaN/inf
            if (price_matrix[a].isnull().any() or 
                price_matrix[b].isnull().any() or
                not np.isfinite(price_matrix[a]).all() or 
                not np.isfinite(price_matrix[b]).all()):
                continue
                
            result = robust_cointegration_test(price_matrix[a], price_matrix[b])
            if result and result['cointegrated']:
                candidate_pairs.append((a, b, result))
        
        if not candidate_pairs:
            print(f"No valid pairs found for {year}")
            continue
            
        # Sort by strongest cointegration
        candidate_pairs.sort(key=lambda x: x[2]['p_value'])
        top_pairs = candidate_pairs[:5]
        print(f"Selected top {len(top_pairs)} pairs for {year}")
        
        # Backtest each pair
        year_pnl = pd.DataFrame(index=price_matrix.index)
        for i, (a, b, stats) in enumerate(top_pairs):
            try:
                print(f"Backtesting {a}-{b}...")
                
                results = backtest_pair(
                    price_a=price_matrix[a],
                    price_b=price_matrix[b],
                    beta=stats['beta'],
                    entry_z=1.5,
                    exit_z=0.5,
                    cost_rate=0.001,
                    book_size=1_000_000
                )
                
                pair_name = f"{a}-{b}"
                year_pnl[pair_name] = results['daily_pnl']
                
                # Save results
                results_df = pd.DataFrame({
                    'Date': results['dates'],
                    'Price_A': price_matrix[a],
                    'Price_B': price_matrix[b],
                    'Spread': results['spread'],
                    'ZScore': results['zscore'],
                    'Position': results['positions'],
                    'Quantity_A': results['a_quantity'],
                    'Quantity_B': results['b_quantity'],
                    'Daily_PnL': results['daily_pnl'],
                    'Cumulative_PnL': results['pnl']
                })
                results_df.to_csv(f"results/{year}_{a}_{b}.csv", index=False)
                
            except Exception as e:
                print(f"Error backtesting {a}-{b}: {str(e)}")
                continue
        
        # Aggregate yearly results
        if not year_pnl.empty:
            year_pnl['Yearly_PnL'] = year_pnl.sum(axis=1)
            year_pnl['Cumulative_PnL'] = year_pnl['Yearly_PnL'].cumsum()
            yearly_results.append(year_pnl)
            
            # Plot yearly performance
            plt.figure(figsize=(12, 6))
            for col in year_pnl.columns[:-2]:
                plt.plot(year_pnl.index, year_pnl[col].cumsum(), alpha=0.4, label=col)
            plt.plot(year_pnl.index, year_pnl['Cumulative_PnL'], 'k-', linewidth=2, label='Portfolio')
            plt.title(f"{year} Pairs Trading Performance")
            plt.legend()
            plt.savefig(f"results/{year}_performance.png")
            plt.close()
    
    # Combine all results
    if not yearly_results:
        print("No valid results to aggregate")
        return
        
    full_results = pd.concat(yearly_results)
    full_results['Total_PnL'] = full_results.filter(like='Yearly_PnL').sum(axis=1)
    full_results['Cumulative_Total'] = full_results['Total_PnL'].cumsum()
    
    # Save final results
    full_results.to_csv("results/full_backtest_results.csv")
    
    # Plot final performance
    plt.figure(figsize=(14, 7))
    plt.plot(full_results.index, full_results['Cumulative_Total'], 'b-', linewidth=2)
    plt.title("10-Year Pairs Trading Performance (2015-2024)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative P&L ($)")
    plt.grid(True)
    plt.savefig("results/final_performance.png")
    plt.show()
    
    # Print summary
    print("\n=== Final Results ===")
    print(f"Total Pairs Tested: {len(tested_pairs)}")
    print(f"Profitable Years: {len(yearly_results)}/{len(all_years)}")
    if not full_results.empty:
        print(f"Final Portfolio Value: ${full_results['Cumulative_Total'].iloc[-1]:,.2f}")
        
def calculate_max_drawdown(series: pd.Series) -> float:
    running_max = series.cummax()
    drawdown = (series - running_max) / running_max.abs().replace(0, 1e-10)
    return drawdown.min()

if __name__ == "__main__":
    yearly_pairs_backtest()