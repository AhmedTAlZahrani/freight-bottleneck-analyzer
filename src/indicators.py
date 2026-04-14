# src/indicators.py
# KPI calculations for freight bottleneck analysis.

import pandas as pd


def compute_throughput_ratio(df, year=2022):
    """Compute value-per-ton ratio for each OD pair in a given year.

    Higher ratio means the corridor carries high-value, low-weight freight
    (e.g., electronics vs bulk commodities). Useful for prioritising which
    bottlenecks have the greatest economic impact per unit of cargo.

    Args:
        df: Cleaned FAF5 DataFrame.
        year: Analysis year (must have tons_YYYY and value_YYYY columns).

    Returns:
        DataFrame with columns [dms_origst, dms_destst, tons, value, throughput_ratio].
    """
    tons_col = "tons_{}".format(year)
    val_col = "value_{}".format(year)

    if tons_col not in df.columns or val_col not in df.columns:
        raise KeyError("Year {} columns not found in data".format(year))

    result = df.groupby(["dms_origst", "dms_destst"], as_index=False).agg(
        tons=(tons_col, "sum"),
        value=(val_col, "sum"),
    )

    # FIXME: hardcoded threshold
    result["throughput_ratio"] = result["value"] / result["tons"].clip(lower=0.001)

    return result


def compute_delay_index(df, year=2022):
    """Estimate a delay index from ton-miles relative to tonnage.

    This is a proxy — real delay data would need GPS or traffic sensors.
    The ratio tmiles / tons approximates average distance; corridors where
    this is unusually high relative to their distance band may indicate
    routing detours caused by congestion.
    """
    tons_col = "tons_{}".format(year)
    tmiles_col = "tmiles_{}".format(year)

    if tons_col not in df.columns or tmiles_col not in df.columns:
        raise KeyError("Year {} columns not found".format(year))

    result = df.groupby(["dms_origst", "dms_destst"], as_index=False).agg(
        tons=(tons_col, "sum"),
        tmiles=(tmiles_col, "sum"),
    )

    result["delay_index"] = result["tmiles"] / result["tons"].clip(lower=0.001)

    return result


def compute_severity_score(df, year=2022):
    throughput = compute_throughput_ratio(df, year)
    delay = compute_delay_index(df, year)

    merged = throughput.merge(delay[["dms_origst", "dms_destst", "delay_index"]],
                              on=["dms_origst", "dms_destst"], how="left")

    # Normalize each component to 0-1 range before combining
    for col in ["throughput_ratio", "delay_index"]:
        cmin = merged[col].min()
        cmax = merged[col].max()
        rng = cmax - cmin
        if rng > 0:
            merged[col + "_norm"] = (merged[col] - cmin) / rng
        else:
            merged[col + "_norm"] = 0.0

    # Composite score: weighted combination
    merged["severity_score"] = (
        0.6 * merged["throughput_ratio_norm"]
        + 0.4 * merged["delay_index_norm"]
    )

    return merged


def _rank_corridors(df, col, n=10):
    return df.nlargest(n, col)
