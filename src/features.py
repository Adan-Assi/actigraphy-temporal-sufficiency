import numpy as np
import pandas as pd
from typing import Dict
from src.windowing import get_chunks, WINDOW_LENGTHS

def calculate_ca(df_chunk: pd.DataFrame) -> float:
    """
    Calculates Circadian Amplitude (Relative Amplitude).
    RA = (M10 - L5) / (M10 + L5)
    """
    # Average activity per hour of the day across the chunk
    hourly_avg = df_chunk.groupby(df_chunk['timestamp'].dt.hour)['activity'].mean()
    
    # M10: Mean activity of the most active 10 hours
    m10 = hourly_avg.sort_values(ascending=False).head(10).mean()
    # L5: Mean activity of the least active 5 hours
    l5 = hourly_avg.sort_values(ascending=True).head(5).mean()
    
    if (m10 + l5) == 0: 
        return 0.0
    return (m10 - l5) / (m10 + l5)

def calculate_is_iv(df_chunk: pd.DataFrame) -> Dict[str, float]:
    """
    Calculates Inter-daily Stability (IS) and Intra-daily Variability (IV).
    IS: Similarities between days.
    IV: Fragmentation within days.
    """
    # Resample to hourly means to reduce minute-level noise
    hourly_series = df_chunk.set_index('timestamp')['activity'].resample('1H').mean()
    
    overall_mean = hourly_series.mean()
    n = len(hourly_series)
    p = 24  # hourly period
    
    # IS: (n * sum of squared deviations of hourly means) / (p * total variance)
    hourly_profile = hourly_series.groupby(hourly_series.index.hour).mean()
    is_numerator = n * np.sum((hourly_profile - overall_mean)**2)
    is_denominator = p * np.sum((hourly_series - overall_mean)**2)
    is_val = is_numerator / is_denominator if is_denominator != 0 else 0
    
    # IV: (n * sum of squared successive differences) / ((n-1) * total variance)
    iv_numerator = n * np.sum(np.diff(hourly_series)**2)
    iv_denominator = (n - 1) * np.sum((hourly_series - overall_mean)**2)
    iv_val = iv_numerator / iv_denominator if iv_denominator != 0 else 0
    
    return {"is": float(is_val), "iv": float(iv_val)}

def generate_non_naive_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts IS, IV, and CA for all window lengths.
    """
    all_results = []
    
    for L in WINDOW_LENGTHS:
        # Note: Using 'all_valid_df' to ensure maximum participants for analysis
        all_valid_df, _ = get_chunks(df, window_days=L)
        
        if all_valid_df.empty:
            continue

        for chunk_id, chunk_data in all_valid_df.groupby("chunk_id"):
            is_iv = calculate_is_iv(chunk_data)
            ca = calculate_ca(chunk_data)
            
            res = {**is_iv, "ca": ca}
            res.update({
                "chunk_id": chunk_id,
                "participant_id": chunk_id.split('_w')[0], # Match utils.py naming
                "window_length": L
            })
            all_results.append(res)
            
    return pd.DataFrame(all_results)