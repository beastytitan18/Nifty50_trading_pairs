import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from src.data_loader import load_price_data, create_price_matrix
from src.cointegration import find_cointegrated_pairs
from src.backtesting import backtest_pair
from src.visualisation import plot_backtest_results
import matplotlib.pyplot as plt
\

# Load data
df = load_price_data("data/raw", range(2015, 2021))
price_matrix = create_price_matrix(df)

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



# def run_analysis():
#     os.makedirs("results", exist_ok=True)

#     # 1. Load and prepare data
#     print("Loading in-sample data (2015-2020)...")
#     df_in = load_price_data("data/raw", range(2015, 2021))
#     price_matrix_in = create_price_matrix(df_in)

#     print("Loading out-of-sample data (2021-2024)...")
#     df_out = load_price_data("data/raw", range(2021, 2025))
#     price_matrix_out = create_price_matrix(df_out)

#     # 2. Filter for common symbols
#     base_universe = nifty50_2018  # or any year you want as your universe
#     in_cols = set(price_matrix_in.columns)
#     out_cols = set(price_matrix_out.columns)
#     common_symbols = [s for s in base_universe if s in in_cols and s in out_cols]

#     missing_in = [s for s in base_universe if s not in in_cols]
#     missing_out = [s for s in base_universe if s not in out_cols]
#     print(f"Missing in in-sample: {missing_in}")
#     print(f"Missing in out-of-sample: {missing_out}")
#     print(f"Using {len(common_symbols)} common symbols for pair selection.")

#     # 3. Find cointegrated pairs on in-sample
#     print("Finding cointegrated pairs (in-sample)...")
#     pairs = find_cointegrated_pairs(price_matrix_in, common_symbols, n_jobs=1)
#     pairs = [p for p in pairs if p is not None]

#     if not pairs:
#         raise ValueError("No cointegrated pairs found!")

#     # Sort pairs by p-value (strongest cointegration first)
#     pairs = sorted(pairs, key=lambda x: x[2]['p_value'])
#     top_pairs = pairs[:5]

#     # 3. Backtest each pair and aggregate portfolio PnL
#     portfolio_in = []
#     portfolio_out = []
#     pair_names = []

#     for i, (a, b, stats) in enumerate(top_pairs):
#         print(f"Backtesting pair {i+1}: {a} vs {b}")

#         # In-sample
#         spread_in = price_matrix_in[a] - stats['beta'] * price_matrix_in[b]
#         results_in = backtest_pair(spread_in, entry_z=1.5, exit_z=0.5)
#         portfolio_in.append(results_in['pnl'].reindex(price_matrix_in.index, fill_value=0))
#         pair_names.append(f"{a}-{b}")

#         # Out-of-sample
#         spread_out = price_matrix_out[a] - stats['beta'] * price_matrix_out[b]
#         results_out = backtest_pair(spread_out, entry_z=1.5, exit_z=0.5)
#         portfolio_out.append(results_out['pnl'].reindex(price_matrix_out.index, fill_value=0))

#         # Optionally save individual results
#         pd.DataFrame({
#             'Spread': spread_in,
#             'ZScore': (spread_in - spread_in.mean()) / spread_in.std(),
#             'Position': results_in['positions'],
#             'PnL': results_in['pnl']
#         }).to_csv(f"results/backtest_data_in_sample_{a}_{b}.csv")
#         pd.DataFrame({
#             'Spread': spread_out,
#             'ZScore': (spread_out - spread_out.mean()) / spread_out.std(),
#             'Position': results_out['positions'],
#             'PnL': results_out['pnl']
#         }).to_csv(f"results/backtest_data_out_sample_{a}_{b}.csv")

#     # 4. Portfolio aggregation
#     portfolio_in_df = pd.DataFrame(portfolio_in).T.fillna(0)
#     portfolio_out_df = pd.DataFrame(portfolio_out).T.fillna(0)
#     portfolio_in_df.columns = pair_names
#     portfolio_out_df.columns = pair_names

#     portfolio_in_df['Portfolio_PnL'] = portfolio_in_df.sum(axis=1)
#     portfolio_out_df['Portfolio_PnL'] = portfolio_out_df.sum(axis=1)

#     # Save and plot
#     portfolio_in_df.to_csv("results/portfolio_in_sample.csv")
#     portfolio_out_df.to_csv("results/portfolio_out_sample.csv")

#     plt.figure(figsize=(12, 5))
#     plt.plot(portfolio_in_df.index, portfolio_in_df['Portfolio_PnL'].cumsum(), label='In-sample')
#     plt.plot(portfolio_out_df.index, portfolio_out_df['Portfolio_PnL'].cumsum(), label='Out-of-sample')
#     plt.title("Portfolio Cumulative PnL (Top 5 Pairs)")
#     plt.xlabel("Date")
#     plt.ylabel("Cumulative PnL")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig("results/portfolio_cumulative_pnl.png")
#     plt.show()

#     print("Portfolio analysis complete! Results saved in results/ folder")

# if __name__ == "__main__":
#     run_analysis()
def get_nifty_list_for_year(year):
    # Map year to your NIFTY50 list variable
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
    """Return only those symbols from nifty_list that are present in price_matrix columns."""
    return [s for s in nifty_list if s in price_matrix.columns]

def run_yearly_portfolio_backtest():
    os.makedirs("results", exist_ok=True)
    all_years = range(2015, 2025)
    all_portfolio_pnl = []

    for year in all_years:
        print(f"\n=== Processing Year {year} ===")
        # 1. Load data for this year
        df = load_price_data("data/raw", range(year, year+1))
        price_matrix = create_price_matrix(df)
        nifty_list = get_nifty_list_for_year(year)
        filtered_nifty = filter_nifty_list(nifty_list, price_matrix)

        missing = [s for s in nifty_list if s not in price_matrix.columns]
        if missing:
            print(f"Missing symbols for {year}: {missing}")
        print(f"Using {len(filtered_nifty)} symbols for {year}")

        # 2. Find top 5 cointegrated pairs
        pairs = find_cointegrated_pairs(price_matrix, filtered_nifty, n_jobs=1)
        pairs = [p for p in pairs if p is not None]
        if not pairs:
            print(f"No cointegrated pairs found for {year}, skipping.")
            continue
        pairs = sorted(pairs, key=lambda x: x[2]['p_value'])
        top_pairs = pairs[:5]
        print(f"Top {len(top_pairs)} pairs for {year}: {[f'{a}-{b}' for a,b,_ in top_pairs]}")

        # 3. Backtest each pair, store individual and portfolio PnL
        pair_pnls = []
        pair_names = []
        for a, b, stats in top_pairs:
            spread = price_matrix[a] - stats['beta'] * price_matrix[b]
            results = backtest_pair(
    spread=spread,
    price_a=price_matrix[a],
    price_b=price_matrix[b],
    beta=stats['beta'],
    entry_z=1.,
    exit_z=0.,
    cost=0.001,
    book_size=1_000_000
)
            pair_pnls.append(results['pnl'].reindex(price_matrix.index, fill_value=0))
            pair_names.append(f"{a}-{b}")
            # Save individual pair results
            pd.DataFrame({
                'Spread': spread,
                'ZScore': (spread - spread.mean()) / spread.std(),
                'Position': results['positions'],
                'PnL': results['pnl']
            }).to_csv(f"results/backtest_{year}_{a}_{b}.csv")

        # 4. Portfolio aggregation for the year
        portfolio_df = pd.DataFrame(pair_pnls).T.fillna(0)
        portfolio_df.columns = pair_names
        portfolio_df['Portfolio_PnL'] = portfolio_df.sum(axis=1)
        portfolio_df.to_csv(f"results/portfolio_{year}.csv")

        # Store for final graph
        all_portfolio_pnl.append(portfolio_df['Portfolio_PnL'])

    # 5. Combine all years for final graph
    all_portfolio_pnl_concat = pd.concat(all_portfolio_pnl)
    all_portfolio_pnl_concat = all_portfolio_pnl_concat.sort_index()
    all_portfolio_cum_pnl = all_portfolio_pnl_concat.cumsum()

    plt.figure(figsize=(14, 6))
    plt.plot(all_portfolio_cum_pnl.index, all_portfolio_cum_pnl.values, label="Cumulative Portfolio PnL")
    plt.title("Cumulative Portfolio PnL (2015-2024, 5 pairs/year)")
    plt.xlabel("Date")
    plt.ylabel("Cumulative PnL")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/final_portfolio_cumulative_pnl.png")
    plt.show()

    print("All yearly portfolio results saved and final graph generated.")

if __name__ == "__main__":
    run_yearly_portfolio_backtest()