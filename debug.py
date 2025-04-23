import pandas as pd

def check_portfolio_activity(portfolio_csv):
    df = pd.read_csv(portfolio_csv, index_col=0, parse_dates=True)
    print(f"{portfolio_csv}: {df.index[0]} to {df.index[-1]}")
    print("Number of nonzero Portfolio_PnL days:", (df['Portfolio_PnL'] != 0).sum())
    print("Number of all-zero days:", (df['Portfolio_PnL'] == 0).sum())
    print("First 10 rows with nonzero PnL:")
    print(df[df['Portfolio_PnL'] != 0].head(10))
    print()

# Example usage:
for year in range(2015, 2019):
    check_portfolio_activity(f"results/portfolio_{year}.csv")