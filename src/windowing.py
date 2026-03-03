from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple

# Constants
WINDOW_LENGTHS = [2, 3, 5, 7, 14]
MINUTES_PER_DAY = 1440
# 80% threshold: 1152 minutes
DAILY_COMPLETENESS_THRESHOLD = int(0.8 * MINUTES_PER_DAY)

def add_day_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a calendar-day column derived from timestamps.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a 'timestamp' column (datetime64)

    Returns
    -------
    pd.DataFrame
        Copy of df with an added 'day' column representing
        calendar days (00:00 of each date).
    """
    if "timestamp" not in df.columns:
        raise ValueError("DataFrame must contain a 'timestamp' column")

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day"] = df["timestamp"].dt.normalize() # Sets time to 00:00:00
    return df

# Helper function to get unique days (= #calendar days the recording touches at least once)
def get_unique_days(df: pd.DataFrame) -> pd.Series:
    """
    Return sorted unique calendar days present in the data.
    """
    if "day" not in df.columns:
        raise ValueError("DataFrame must contain a 'day' column")

    return pd.Series(df["day"].unique()).sort_values().reset_index(drop=True)


def daily_minute_counts(df: pd.DataFrame) -> pd.Series:
    """
    Count the number of recorded minutes per calendar day.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain 'day' and 'timestamp' columns.

    Returns
    -------
    pd.Series
        Indexed by day, with values equal to the number of
        minute-level observations recorded on that day.
    """
    if "day" not in df.columns or "timestamp" not in df.columns:
        raise ValueError("DataFrame must contain 'day' and 'timestamp' columns")

    return df.groupby("day")["timestamp"].count()

# Helper function to check day completeness
def is_day_complete(minute_count: int) -> bool:
    """Check if a day meets the 80% threshold."""
    return minute_count >= DAILY_COMPLETENESS_THRESHOLD


def get_chunks(df: pd.DataFrame, window_days: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Slice the data into non-overlapping blocks based on calendar days.
    
    Returns:
        all_valid_chunks: Every chunk passing the threshold (for Group Analysis)
        icc_ready_chunks: Chunks only for users with 2+ valid blocks (for Reliability)
    """
    all_chunks_list = []
    icc_chunks_list = []
    
    # Ensure day column exists
    if "day" not in df.columns:
        df = add_day_column(df)
        
    for user_id, user_data in df.groupby("participant_id"):
        user_data = user_data.sort_values("timestamp")
        unique_days = sorted(user_data["day"].unique())
        
        user_valid_chunks = []
        
        # Greedy non-overlapping windowing
        # We move in steps of 'window_days' to ensure independence
        for i in range(0, len(unique_days) - window_days + 1, window_days):
            current_window_days = unique_days[i : i + window_days]
            chunk = user_data[user_data["day"].isin(current_window_days)].copy()
            
            day_counts = chunk.groupby("day")["timestamp"].count()
            
            # A chunk is valid ONLY if EVERY day in it is complete
            # This is stricter and safer for circadian modeling
            if all(is_day_complete(count) for count in day_counts) and len(day_counts) == window_days:
                chunk["chunk_id"] = f"{user_id}_w{window_days}_c{i//window_days}"
                user_valid_chunks.append(chunk)
        
        # Store for Group Analysis
        if user_valid_chunks:
            all_chunks_list.extend(user_valid_chunks)
            
            # Store for ICC only if 2+ independent windows exist
            if len(user_valid_chunks) >= 2:
                icc_chunks_list.extend(user_valid_chunks)
                
    all_valid_df = pd.concat(all_chunks_list) if all_chunks_list else pd.DataFrame()
    icc_ready_df = pd.concat(icc_chunks_list) if icc_chunks_list else pd.DataFrame()
    
    return all_valid_df, icc_ready_df