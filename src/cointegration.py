
from joblib import Parallel, delayed
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import pandas as pd
import numpy as np

def engle_granger_test(series_x: pd.Series, series_y: pd.Series, 
                      significance: float = 0.05) -> dict:
    """Enhanced Engle-Granger test with residual diagnostics."""
    df = pd.concat([series_x, series_y], axis=1).dropna()
    if len(df) < 100:
        return None
        
    x = sm.add_constant(df.iloc[:, 1])
    model = sm.OLS(df.iloc[:, 0], x).fit()
    residuals = model.resid
    
    # ADF test with optimized parameters
    adf_result = adfuller(residuals, maxlag=int(12*(len(residuals)/100)**(1/4)))
    
    return {
        'beta': model.params[1],
        'alpha': model.params[0],
        'adf_stat': adf_result[0],
        'p_value': adf_result[1],
        'is_cointegrated': adf_result[1] < significance,
        'residuals': residuals
    }

def find_cointegrated_pairs(price_matrix: pd.DataFrame, 
                           symbols: list, 
                           n_jobs: int = -1) -> list:
    """Parallel cointegration testing with pre-filtering."""
    valid_symbols = [s for s in symbols if s in price_matrix.columns]
    pairs = combinations(valid_symbols, 2)
    
    return Parallel(n_jobs=n_jobs)(
        delayed(_process_pair)(price_matrix, a, b) 
        for a, b in pairs
    )

def _process_pair(price_matrix, a, b):
    result = engle_granger_test(price_matrix[a], price_matrix[b])
    return (a, b, result) if result and result['is_cointegrated'] else None