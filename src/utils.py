from pathlib import Path
import pandas as pd

def load_subject_csv(path: Path) -> pd.DataFrame:
    """
    Load a single DEPRESJON subject CSV.

    Parameters
    ----------
    path : Path
        Path to a CSV file named condition_<n>.csv or control_<n>.csv

    Returns
    -------
    pd.DataFrame
        Columns:
        - participant_id
        - group
        - timestamp
        - activity
    """
    pid = path.stem  # e.g. "condition_7" or "control_14"

    # Infer group from filename
    if pid.startswith("condition_"):
        group = "condition"
    elif pid.startswith("control_"):
        group = "control"
    else:
        raise ValueError(f"Unexpected filename: {pid}")

    # Load CSV
    df = pd.read_csv(path)

    # Parse timestamp (minute-level, naive datetime)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Drop invalid timestamps (rare, but safe)
    df = df.dropna(subset=["timestamp"])

    # Activity: 0 is valid, MUST NOT drop zeros
    df["activity"] = pd.to_numeric(df["activity"], errors="coerce")

    # Attach identifiers
    df["participant_id"] = pid
    df["group"] = group

    # Drop redundant column
    df = df.drop(columns=["date"], errors="ignore")

    # Sort chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df


def load_all_subjects(raw_root: Path) -> pd.DataFrame:
    """
    Load all DEPRESJON actigraphy CSVs.

    Parameters
    ----------
    raw_root : Path
        Path to data/raw/

    Returns
    -------
    pd.DataFrame
        Concatenated actigraphy data for ALL subjects.
    """
    dfs = []

    for subdir in ["condition", "control"]:
        dir_path = raw_root / subdir
        if not dir_path.exists(): # Just to be safe
            raise FileNotFoundError(f"Missing directory: {dir_path}")

        for path in sorted(dir_path.glob("*.csv")):
            dfs.append(load_subject_csv(path))

    if not dfs:
        raise RuntimeError("No subject files found.")

    return pd.concat(dfs, ignore_index=True)


def load_scores(path: Path) -> pd.DataFrame:
    """
    Load subject-level metadata and MADRS scores.

    Parameters
    ----------
    path : Path
        Path to scores.csv

    Returns
    -------
    pd.DataFrame
        One row per subject.
    """
    df = pd.read_csv(path)

    # Rename for consistency with actigraphy loaders
    df = df.rename(columns={"number": "participant_id"})

    # Ensure string IDs
    df["participant_id"] = df["participant_id"].astype(str)

    return df
