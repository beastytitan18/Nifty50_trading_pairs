
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union

def load_price_data(data_dir: Union[str, Path], years: range) -> pd.DataFrame:
    """Load and concatenate yearly parquet files."""
    data_dir = Path(data_dir)
    dfs = []
    for year in years:
        file_path = data_dir / f"nifty50_{year}.parquet"
        df = pd.read_parquet(file_path)
        df['date'] = pd.to_datetime(df['date'])
        dfs.append(df)
    return pd.concat(dfs).drop_duplicates(['date', 'symbol'])

def create_price_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create pivoted price matrix with validation."""
    required_cols = {'date', 'symbol', 'close'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"DataFrame must contain {required_cols} columns")
        
    return df.pivot_table(
        index='date',
        columns='symbol',
        values='close',
        aggfunc='first'
    ).sort_index()