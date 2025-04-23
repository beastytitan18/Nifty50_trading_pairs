# main.py
import os
import pandas as pd
from src.data_loader import load_and_validate_data, create_clean_price_matrix
from src.pair_selection import find_robust_pairs
from src.backtesting import backtest_pair
from src.visualisation import plot_backtest_results
# Add to the top of main.py
from src.utils import (
    save_pair_results,
    aggregate_yearly_results,
    plot_yearly_results,
    plot_final_results
)

# Find cointegrated pairs
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

def main():
    years = list(range(2015, 2025))
    all_results = []
    
    # Load all data first with validation
    yearly_data = load_and_validate_data(years)
    
    for year, df in yearly_data.items():
        print(f"\n=== Processing {year} ===")
        
        # Get Nifty symbols for the year
        try:
            nifty_symbols = globals()[f"nifty50_{year}"]
            valid_symbols = [s for s in nifty_symbols if s in df['symbol'].unique()]
            print(f"{year}: {len(valid_symbols)} valid symbols")
            
            if len(valid_symbols) < 20:
                print(f"Skipping {year} - insufficient symbols")
                continue
                
            # Create clean price matrix
            price_matrix = create_clean_price_matrix(df[df['symbol'].isin(valid_symbols)])
            if price_matrix.empty:
                print(f"Skipping {year} - empty price matrix")
                continue
                
            # Find robust pairs
            pairs = find_robust_pairs(price_matrix)
            print(f"Found {len(pairs)} valid pairs for {year}")
            
            if not pairs:
                continue
                
            # Backtest top 5 pairs
            year_results = []
            for a, b, stats in pairs[:5]:
                try:
                    print(f"Backtesting {a}-{b}...")
                    results = backtest_pair(
                        price_matrix[a],
                        price_matrix[b],
                        stats['beta'],
                        entry_z=1.5,
                        exit_z=0.5
                    )
                    results['year'] = year
                    results['pair'] = f"{a}-{b}"
                    year_results.append(results)
                    save_pair_results(results, year, a, b)
                except Exception as e:
                    print(f"Error backtesting {a}-{b}: {str(e)}")
                    continue
                    
            if year_results:
                yearly_pnl = aggregate_yearly_results(year_results)
                all_results.append(yearly_pnl)
                plot_yearly_results(yearly_pnl, year)
                
        except Exception as e:
            print(f"Error processing {year}: {str(e)}")
            continue
            
    if all_results:
        final_results = pd.concat(all_results)
        plot_final_results(final_results)
        print("\n=== Final Performance ===")
        print(f"Total Portfolio Value: ${final_results['Cumulative_PnL'].iloc[-1]:,.2f}")
    else:
        print("No valid results generated")

if __name__ == "__main__":
    main()