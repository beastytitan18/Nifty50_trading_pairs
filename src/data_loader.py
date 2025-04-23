# src/data_loader.py
import pandas as pd
import numpy as np
from typing import List, Dict

def load_and_validate_data(years: List[int]) -> Dict[int, pd.DataFrame]:
    """Load and validate yearly data with strict checks"""
    yearly_data = {}
    for year in years:
        try:
            df = pd.read_parquet(f"data/raw/nifty50_{year}.parquet")
            
            # Strict validation
            if not {'date', 'symbol', 'close'}.issubset(df.columns):
                print(f"Missing required columns in {year}")
                continue
                
            df = df.dropna(subset=['date', 'symbol', 'close'])
            df['date'] = pd.to_datetime(df['date'])
            
            # Remove duplicate entries
            df = df.drop_duplicates(['date', 'symbol'])
            
            # Filter for sufficient data points
            symbol_counts = df['symbol'].value_counts()
            valid_symbols = symbol_counts[symbol_counts >= 200].index.tolist()
            df = df[df['symbol'].isin(valid_symbols)]
            
            if not df.empty:
                yearly_data[year] = df
            else:
                print(f"No valid data for {year}")
                
        except Exception as e:
            print(f"Error loading {year}: {str(e)}")
    
    return yearly_data

def create_clean_price_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Create price matrix with additional validation"""
    # Check for sufficient data
    if len(df['symbol'].unique()) < 20:
        return pd.DataFrame()
    
    price_matrix = df.pivot(index='date', columns='symbol', values='close')
    
    # Filter for stocks with sufficient history
    price_matrix = price_matrix.loc[:, price_matrix.count() >= 200]
    
    # Forward fill up to 5 days, then drop remaining NA
    price_matrix = price_matrix.ffill(limit=5).dropna(axis=1)
    
    return price_matrix