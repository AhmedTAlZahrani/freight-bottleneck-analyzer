# tests/test_indicators.py

import pytest
import pandas as pd
from src.indicators import compute_throughput_ratio, compute_delay_index, compute_severity_score


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "dms_origst": [1, 1, 2],
        "dms_destst": [2, 3, 3],
        "dms_mode": [1, 1, 1],
        "sctg2": [1, 1, 1],
        "tons_2022": [100.0, 50.0, 200.0],
        "value_2022": [500.0, 300.0, 400.0],
        "tmiles_2022": [1000.0, 250.0, 800.0],
    })


def test_throughput_ratio_values(sample_df):
    result = compute_throughput_ratio(sample_df, year=2022)
    row = result[result["dms_destst"] == 2].iloc[0]
    assert row["throughput_ratio"] == pytest.approx(5.0, rel=1e-3)


def test_delay_index_positive(sample_df):
    result = compute_delay_index(sample_df, year=2022)
    assert (result["delay_index"] > 0).all()


@pytest.mark.skip("need larger dataset")
def test_severity_distribution(sample_df):
    result = compute_severity_score(sample_df, year=2022)
    assert result["severity_score"].between(0, 1).all()
