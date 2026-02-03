from pathlib import Path
import pandas as pd
from typing import List, Dict

# Constants
WINDOW_LENGTHS = [2, 3, 5, 7, 14]
MINUTES_PER_DAY = 1440
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
    """
    Check whether a calendar day meets the completeness threshold
    (at least 80% of expected minutes, i.e. ≥1152 out of 1440).
    """
    return minute_count >= DAILY_COMPLETENESS_THRESHOLD
