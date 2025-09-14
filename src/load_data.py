# src/load_data.py
# Functions for loading and preprocessing the FAF5 bottleneck dataset.

import pandas as pd


def load_bottleneck_data(path):
    """Load the FAF5 bottleneck CSV and perform basic validation.

    Args:
        path: Path to the CSV file.

    Returns:
        pd.DataFrame with the raw data.

    Raises:
        FileNotFoundError: If the CSV does not exist.
        ValueError: If required columns are missing.
    """
    df = pd.read_csv(path)

    required = ["dms_origst", "dms_destst", "dms_mode", "sctg2"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: {}".format(", ".join(missing)))

    # Check that we have at least some tonnage columns
    ton_cols = [c for c in df.columns if c.startswith("tons_")]
    if len(ton_cols) == 0:
        raise ValueError("No tonnage year columns found (expected tons_YYYY)")

    return df


def clean_data(df):
    """Drop rows with missing origin/dest codes and fill NaN numerics with 0."""
    df = df.copy()
    df = df.dropna(subset=["dms_origst", "dms_destst"])

    # Fill numeric NaNs
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Ensure state codes are integers
    df["dms_origst"] = df["dms_origst"].astype(int)
    df["dms_destst"] = df["dms_destst"].astype(int)

    return df


def get_year_columns(df, prefix="value"):
    year_cols = {}
    for c in df.columns:
        if c.startswith(prefix + "_20"):
            try:
                yr = int(c.split("_")[-1])
                year_cols[yr] = c
            except ValueError:
                continue
    return year_cols


def filter_by_mode(df, mode_code=1):
    """Filter to a single transport mode (default 1 = Truck)."""
    return df[df["dms_mode"] == mode_code].copy()
