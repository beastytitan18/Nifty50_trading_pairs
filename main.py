import os
import pandas as pd
from src.data_loader import load_and_validate_data, create_clean_price_matrix
from src.pair_selection import find_pairs
from src.backtesting import backtest_pair
from src.utils import save_pair_results, aggregate_yearly_results


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
def buy_and_hold_pnl(price_series: pd.Series, capital: float) -> float:
    """
    Calculate buy-and-hold PnL for a stock.
    Buys at first available price, sells at last available price.
    """
    buy_price = price_series.iloc[0]
    sell_price = price_series.iloc[-1]
    quantity = capital / buy_price
    pnl = (sell_price - buy_price) * quantity
    return pnl

def main():
    years = list(range(2015, 2025))
    all_results = []
    window = 20  # rolling window size for z-score

    yearly_data = load_and_validate_data(years)

    for idx, year in enumerate(years):
        print(f"\n=== Processing {year} ===")
        try:
            df = yearly_data[year]
            nifty_symbols = globals()[f"nifty50_{year}"]
            valid_symbols = [s for s in nifty_symbols if s in df['symbol'].unique()]
            print(f"{year}: {len(valid_symbols)} valid symbols")

            if len(valid_symbols) < 20:
                print(f"Skipping {year} - insufficient symbols")
                continue

            price_matrix = create_clean_price_matrix(df[df['symbol'].isin(valid_symbols)])
            if price_matrix.empty:
                print(f"Skipping {year} - empty price matrix")
                continue

            # Prepare previous year price_matrix for warm-up
            if idx > 0:
                prev_year = years[idx - 1]
                prev_df = yearly_data[prev_year]
                prev_valid_symbols = [s for s in nifty_symbols if s in prev_df['symbol'].unique()]
                prev_price_matrix = create_clean_price_matrix(prev_df[prev_df['symbol'].isin(prev_valid_symbols)])
            else:
                prev_price_matrix = None

            pairs = find_pairs(price_matrix)
            print(f"Found {len(pairs)} valid pairs for {year}")

            if not pairs:
                continue

            year_results = []
            for a, b, stats in pairs[:5]:
                try:
                    # Prepare price series with warm-up
                    if prev_price_matrix is not None and a in prev_price_matrix and b in prev_price_matrix:
                        price_a_full = pd.concat([prev_price_matrix[a].iloc[-window:], price_matrix[a]])
                        price_b_full = pd.concat([prev_price_matrix[b].iloc[-window:], price_matrix[b]])
                    else:
                        price_a_full = price_matrix[a]
                        price_b_full = price_matrix[b]

                    # Align indexes
                    price_a_full, price_b_full = price_a_full.align(price_b_full, join='inner')

                    print(f"Backtesting {a}-{b}...")
                    results = backtest_pair(
                        price_a_full,
                        price_b_full,
                        stats['beta'],
                        entry_z=1.5,
                        exit_z=0.15
                    )

                    # Slice off the first `window` rows so only current year remains
                    if isinstance(results, dict) and "details" in results:
                        df_pair = results["details"].iloc[window:].copy()
                    elif isinstance(results, pd.DataFrame):
                        df_pair = results.iloc[window:].copy()
                    else:
                        print(f"Warning: Unexpected results type for {a}-{b}")
                        continue

                    bh_pnl_a = buy_and_hold_pnl(price_matrix[a], 500_000)
                    bh_pnl_b = buy_and_hold_pnl(price_matrix[b], 500_000)
                    print(f"Buy & Hold {a}: {bh_pnl_a:,.2f}, {b}: {bh_pnl_b:,.2f}")

                    df_pair['year'] = year
                    df_pair['pair'] = f"{a}-{b}"
                    df_pair['bh_pnl_a'] = bh_pnl_a
                    df_pair['bh_pnl_b'] = bh_pnl_b
                    year_results.append(df_pair)
                    save_pair_results({"details": df_pair}, year, a, b)
                except Exception as e:
                    print(f"Error backtesting {a}-{b}: {str(e)}")
                    continue

            if year_results:
                # Aggregate yearly results (cumulative_pnl starts from 0)
                yearly_pnl = aggregate_yearly_results(year_results, year)
                yearly_pnl.to_csv(f"results/{year}_yearly_pnl.csv", index=False)
                all_results.append(yearly_pnl)

        except Exception as e:
            print(f"Error processing {year}: {str(e)}")
            continue

    if all_results:
        # Build continuous cumulative_pnl for final portfolio
        final_results = []
        carry_forward = 0
        for yearly_pnl in all_results:
            yearly_pnl = yearly_pnl.copy()
            yearly_pnl['cumulative_pnl'] = yearly_pnl['cumulative_pnl'] + carry_forward
            carry_forward = yearly_pnl['cumulative_pnl'].iloc[-1]
            final_results.append(yearly_pnl)
        final_results = pd.concat(final_results, ignore_index=True)
        final_results.to_csv("results/final_portfolio_pnl.csv", index=False)
        print("\n=== Final Performance ===")
        print(f"Total Portfolio Value: {final_results['cumulative_pnl'].iloc[-1]:,.2f}")
    else:
        print("No valid results generated")

if __name__ == "__main__":
    main()