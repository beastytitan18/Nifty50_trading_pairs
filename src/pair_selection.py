import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from statsmodels.tsa.stattools import coint

def find_robust_pairs(price_matrix: pd.DataFrame, 
                     min_correlation: float = 0.7,
                     min_coint_pvalue: float = 0.05) -> List[Tuple]:
    """Safe pair finding with proper correlation handling"""
    valid_pairs = []
    symbols = price_matrix.columns.tolist()
    
    # Calculate correlation matrix properly
    corr_matrix = price_matrix.corr().abs()
    np.fill_diagonal(corr_matrix.values, 0)  # Zero out diagonal
    
    # Get upper triangle pairs with high correlation
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] >= min_correlation:
                a = corr_matrix.columns[i]
                b = corr_matrix.columns[j]
                high_corr_pairs.append((a, b))
    
    print(f"Testing {len(high_corr_pairs)} correlated pairs...")
    
    for a, b in high_corr_pairs:
        try:
            # Price validation
            prices_a = price_matrix[a]
            prices_b = price_matrix[b]
            
            if prices_a.isnull().any() or prices_b.isnull().any():
                continue
                
            # Cointegration test
            with np.errstate(all='raise'):
                try:
                    score, pvalue, _ = coint(prices_a, prices_b)
                    if not (np.isfinite(score) and np.isfinite(pvalue)):
                        continue
                except:
                    continue

            # Skip if not significant
            if pvalue >= min_coint_pvalue:
                continue
                
            # Hedge ratio
            beta = np.polyfit(prices_b, prices_a, 1)[0]
            if not np.isfinite(beta) or abs(beta) < 0.1 or abs(beta) > 10:
                continue
                
            # Spread properties
            spread = prices_a - beta * prices_b
            if spread.std() < 1e-6:
                continue
                
            # Half-life
            lag = spread.shift(1).dropna()
            delta = spread.diff().dropna()
            if len(delta) < 20:
                continue
                
            try:
                beta_hl = np.polyfit(lag, delta, 1)[0]
                half_life = max(5, min(60, -np.log(2)/beta_hl)) if beta_hl < 0 else np.nan
                if not np.isfinite(half_life):
                    continue
            except:
                continue
                
            valid_pairs.append((a, b, {
                'p_value': pvalue,
                'beta': beta,
                'half_life': half_life,
                'spread_std': spread.std()
            }))
            
        except Exception as e:
            print(f"Error testing {a}-{b}: {str(e)}")
            continue
    
    valid_pairs.sort(key=lambda x: x[2]['p_value'])
    return valid_pairs