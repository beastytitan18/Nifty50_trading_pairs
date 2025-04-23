
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union

def load_price_data(data_dir: str, years: range) -> pd.DataFrame:
    """Load and concatenate yearly parquet files with error handling."""
    dfs = []
    for year in years:
        try:
            file_path = f"{data_dir}/nifty50_{year}.parquet"
            df = pd.read_parquet(file_path)
            if not {'date', 'symbol', 'close'}.issubset(df.columns):
                raise ValueError(f"Missing required columns in {file_path}")
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {year}: {str(e)}")
            continue
    
    if not dfs:
        raise ValueError("No valid data files found")
    
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