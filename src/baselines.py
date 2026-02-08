import numpy as np
import pandas as pd


def shuffle_within_window(
    df_window: pd.DataFrame,
    activity_col: str = "activity",
    random_state: int | None = None
) -> pd.DataFrame:
    """
    Randomly permute minute-level activity values within a window,
    destroying temporal order while preserving the value distribution.

    Parameters
    ----------
    df_window : pd.DataFrame
        Data for a single window (must already be sorted by time).
    activity_col : str
        Column containing minute-level activity values.
    random_state : int or None
        Optional random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Copy of df_window with shuffled activity values.
    """
    if activity_col not in df_window.columns:
        raise ValueError(f"'{activity_col}' column not found")

    df_window = df_window.copy()

    rng = np.random.default_rng(random_state)
    shuffled = df_window[activity_col].values.copy()
    rng.shuffle(shuffled)

    df_window[activity_col] = shuffled
    return df_window
