import os
import pandas as pd

PAIR_FIELDS = [
    "date", "price_a", "price_b", "spread", "zscore", "position",
    "quantity_a", "quantity_b", "daily_pnl", "cumulative_pnl"
]

def save_pair_results(results, year, a, b):
    """Save detailed pairwise backtest results to CSV."""
    df = results.get("details")
    if df is None:
        return
    # Ensure correct columns and order
    df = df[PAIR_FIELDS]
    outdir = f"results"
    os.makedirs(outdir, exist_ok=True)
    fname = f"{year}_{a}_{b}.csv"
    df.to_csv(os.path.join(outdir, fname), index=False)

import pandas as pd
import os

def aggregate_yearly_results(year_results, year):
    """
    year_results: list of DataFrames, each with 'date' and 'daily_pnl'
    Returns: DataFrame with 'date', 'yearly_pnl', 'cumulative_pnl'
    """
    # Ensure all results are DataFrames
    dfs = []
    for res in year_results:
        # If res is a dict, get the DataFrame
        if isinstance(res, dict) and 'date' in res:
            df = pd.DataFrame(res)
        elif isinstance(res, pd.DataFrame):
            df = res
        else:
            raise ValueError("Each result must be a DataFrame or dict with 'date'")
        dfs.append(df[['date', 'daily_pnl']].rename(columns={'daily_pnl': f"pnl_{len(dfs)+1}"}))

    # Merge on date
    merged = dfs[0]
    for df in dfs[1:]:
        merged = pd.merge(merged, df, on='date', how='outer')
    merged = merged.sort_values('date').fillna(0)
    merged['yearly_pnl'] = merged.iloc[:, 1:].sum(axis=1)
    merged['cumulative_pnl'] = merged['yearly_pnl'].cumsum()
    merged['year'] = year

    # Save to CSV
    os.makedirs("results", exist_ok=True)
    merged.to_csv(f"results/{year}_yearly_pnl.csv", index=False)
    return merged

def aggregate_final_portfolio(years):
    """Concatenate yearly pnl for continuous cumulative pnl and save final csv."""
    all_years = []
    last_cum = 0
    for year in years:
        f = f"results/{year}_yearly_pnl.csv"
        if not os.path.exists(f):
            continue
        df = pd.read_csv(f)
        df["cumulative_pnl"] = df["yearly_pnl"].cumsum() + last_cum
        last_cum = df["cumulative_pnl"].iloc[-1]
        df["year"] = year
        all_years.append(df)
    if all_years:
        final = pd.concat(all_years, ignore_index=True)
        final.to_csv("results/final_portfolio_pnl.csv", index=False)
        return final
    return None