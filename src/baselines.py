import numpy as np
import pandas as pd
import statsmodels.api as sm
from typing import Dict
from src.windowing import get_chunks, WINDOW_LENGTHS

def fit_cosinor(
    df_window: pd.DataFrame, 
    activity_col: str = "activity"
) -> Dict[str, float]:
    """
    Fit a 24-hour Cosinor model to the windowed activity data.
    The model form is: x(t) = M + A cos(2πt/24 + φ) + ε.

    Parameters
    ----------
    df_window : pd.DataFrame
        Data for a single window. Must contain a 'timestamp' column.
    activity_col : str
        The column name for minute-level activity counts.

    Returns
    -------
    Dict[str, float]
        A dictionary containing:
        - mesor (M): The rhythm-adjusted mean activity level.
        - amplitude (A): Half the peak-to-trough range of the rhythm.
        - acrophase (phi): The timing of the peak activity (in hours).
        - r_squared: The goodness of fit (model fit quality).
    """
    if activity_col not in df_window.columns:
        raise ValueError(f"'{activity_col}' column not found")
    
    # 1. Prepare time variables (t = hours from midnight)
    t = df_window["timestamp"].dt.hour + df_window["timestamp"].dt.minute / 60.0
    
    # Use log-transformation (log(y+1)) to handle activity spikes and normalize variance
    y = np.log1p(df_window[activity_col].values)
    
    # 2. Linearize the model: y = M + beta1*cos(2πt/24) + beta2*sin(2πt/24)
    x1 = np.cos(2 * np.pi * t / 24)
    x2 = np.sin(2 * np.pi * t / 24)
    
    # Add intercept for Mesor (M)
    X = np.column_stack([np.ones(len(t)), x1, x2])
    
    # 3. Fit Ordinary Least Squares
    model = sm.OLS(y, X).fit()
    beta0, beta1, beta2 = model.params
    
    # 4. Extract non-linear parameters
    mesor = beta0
    amplitude = np.sqrt(beta1**2 + beta2**2)
    # Acrophase in radians, then converted to hours of day (0-24)
    phi_rad = np.arctan2(-beta2, beta1)
    acrophase = (phi_rad * 24 / (2 * np.pi)) % 24
    
    return {
        "mesor": float(mesor),
        "amplitude": float(amplitude),
        "acrophase": float(acrophase),
        "r_squared": float(model.rsquared)
    }

def generate_naive_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes all window lengths and extracts Cosinor features.
    Used for both Group Separation and ICC analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Full dataset containing 'participant_id', 'timestamp', and 'activity'.

    Returns
    -------
    pd.DataFrame
        DataFrame where each row is a chunk, including user IDs, 
        window lengths, and extracted Cosinor parameters.
    """
    all_results = []

    for L in WINDOW_LENGTHS:
            # 1. Get all valid chunks for this window length
            all_valid_df, _ = get_chunks(df, window_days=L)
            
            if all_valid_df.empty:
                continue

            # 2. Extract features for each chunk
            for chunk_id, chunk_data in all_valid_df.groupby("chunk_id"):
                
                # CRITICAL: Skip windows with zero variance to avoid RuntimeWarnings/NaNs
                # This happens if a subject has 0 activity for the entire window length
                if chunk_data["activity"].std() == 0:
                    continue
                    
                features = fit_cosinor(chunk_data)
                features["chunk_id"] = chunk_id
                
                # Updated to match participant_id naming convention from utils.py
                features["participant_id"] = chunk_id.split('_w')[0] 
                features["window_length"] = L
                all_results.append(features)

    return pd.DataFrame(all_results)

def calculate_non_parametric_features(df_window: pd.DataFrame) -> Dict[str, float]:
    """
    Calculates IS, IV, and Relative Amplitude for a window.
    """
    # Ensure activity is present
    y = df_window['activity'].values
    n = len(y)
    p = 1440 # Minutes in a day
    
    # 1. Interdaily Stability (IS)
    # Ratio of variance of average 24h profile to total variance
    hourly_avg = df_window.groupby(df_window['timestamp'].dt.hour)['activity'].mean()
    mean_total = np.mean(y)
    
    numerator = p * np.sum((hourly_avg - mean_total)**2)
    denominator = n * np.sum((y - mean_total)**2)
    is_val = numerator / denominator if denominator != 0 else 0
    
    # 2. Intradaily Variability (IV)
    # Ratio of mean squares of successive differences to total variance
    numerator_iv = n * np.sum(np.diff(y)**2)
    denominator_iv = (n - 1) * np.sum((y - mean_total)**2)
    iv_val = numerator_iv / denominator_iv if denominator_iv != 0 else 0
    
    # 3. Relative Amplitude (RA)
    # (M10 - L5) / (M10 + L5)
    # Simplified: Top 10 hours vs Bottom 5 hours
    hourly_means = df_window.groupby(df_window['timestamp'].dt.hour)['activity'].mean()
    m10 = hourly_means.sort_values(ascending=False).head(10).mean()
    l5 = hourly_means.sort_values(ascending=True).head(5).mean()
    ra_val = (m10 - l5) / (m10 + l5) if (m10 + l5) != 0 else 0
    
    return {
        "is": float(is_val),
        "iv": float(iv_val),
        "ra": float(ra_val)
    }