from statsmodels.tsa.stattools import coint
import pandas as pd
import numpy as np
from typing import Optional, Dict

def robust_cointegration_test(
    series_a: pd.Series,
    series_b: pd.Series,
    min_periods: int = 100
) -> Optional[Dict]:
    """Safe cointegration test with comprehensive error handling"""
    try:
        # Align and validate data
        aligned = pd.concat([series_a, series_b], axis=1).dropna()
        if len(aligned) < min_periods:
            return None
        
        # Check for sufficient price variation
        if (aligned.iloc[:,0].std() < 1e-6) or (aligned.iloc[:,1].std() < 1e-6):
            return None

        # Cointegration test with error handling
        with np.errstate(all='raise'):
            try:
                score, pvalue, _ = coint(aligned.iloc[:,0], aligned.iloc[:,1])
            except (ValueError, FloatingPointError):
                return None

        # Hedge ratio calculation with validation
        try:
            beta = np.polyfit(aligned.iloc[:,1], aligned.iloc[:,0], 1)[0]
            if not np.isfinite(beta):
                return None
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return None

        # Spread calculation
        spread = aligned.iloc[:,0] - beta * aligned.iloc[:,1]
        
        # Half-life calculation with validation
        try:
            lag = spread.shift(1).dropna()
            delta = spread[1:] - lag
            if len(delta) < 10:  # Need sufficient samples
                return None
                
            beta_hl = np.polyfit(lag, delta, 1)[0]
            if not np.isfinite(beta_hl):
                return None
                
            half_life = max(1, -np.log(2)/beta_hl) if beta_hl < 0 else np.nan
        except (ValueError, FloatingPointError, np.linalg.LinAlgError):
            return None

        # Final validation checks
        is_valid = (
            pvalue < 0.05 and 
            np.isfinite(pvalue) and
            (5 < half_life < 60) and 
            (0.1 < abs(beta) < 10))
        
        return {
            'cointegrated': is_valid,
            'p_value': pvalue,
            'beta': beta,
            'half_life': half_life,
            'spread': spread
        } if is_valid else None
    except Exception as e:
        print(f"Error testing pair {series_a.name}-{series_b.name}: {str(e)}")
        return None