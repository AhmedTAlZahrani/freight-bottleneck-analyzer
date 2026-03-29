# tests/test_ai_model.py

import pytest
import numpy as np
import pandas as pd
import os
import tempfile

from src.ai_model import (
    prepare_features,
    split_data,
    train_model,
    evaluate_model,
    save_model,
    load_model,
    get_feature_importance,
    predict_severity,
)
from src.load_data import load_bottleneck_data, clean_data, get_year_columns, filter_by_mode


@pytest.fixture
def severity_df():
    np.random.seed(7)
    n = 40
    return pd.DataFrame({
        "dms_origst": np.random.randint(1, 10, n),
        "dms_destst": np.random.randint(1, 10, n),
        "tons": np.random.uniform(10, 500, n),
        "value": np.random.uniform(100, 5000, n),
        "throughput_ratio": np.random.uniform(0.5, 20, n),
        "delay_index": np.random.uniform(1, 50, n),
        "severity_score": np.random.uniform(0, 1, n),
    })


@pytest.fixture
def trained_model(severity_df):
    X, y = prepare_features(severity_df)
    return train_model(X, y)


# --- prepare_features ---

def test_prepare_features_shapes(severity_df):
    X, y = prepare_features(severity_df)
    assert X.shape == (40, 4)
    assert y.shape == (40,)


def test_prepare_features_returns_numpy(severity_df):
    X, y = prepare_features(severity_df)
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)


# --- split_data ---

def test_split_data_sizes(severity_df):
    X, y = prepare_features(severity_df)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.25)
    assert len(X_train) + len(X_test) == 40
    assert len(X_test) == 10


def test_split_data_deterministic(severity_df):
    X, y = prepare_features(severity_df)
    _, X1, _, _ = split_data(X, y)
    _, X2, _, _ = split_data(X, y)
    np.testing.assert_array_equal(X1, X2)


# --- train_model ---

def test_train_model_returns_fitted(severity_df):
    X, y = prepare_features(severity_df)
    model = train_model(X, y, n_estimators=10)
    preds = model.predict(X[:2])
    assert preds.shape == (2,)


# --- evaluate_model ---

def test_evaluate_model_keys(trained_model, severity_df):
    X, y = prepare_features(severity_df)
    metrics = evaluate_model(trained_model, X, y)
    assert "r2" in metrics
    assert "mae" in metrics


def test_evaluate_model_mae_nonneg(trained_model, severity_df):
    X, y = prepare_features(severity_df)
    metrics = evaluate_model(trained_model, X, y)
    assert metrics["mae"] >= 0


# --- save / load model ---

def test_save_and_load_model(trained_model, severity_df):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sub", "model.joblib")
        save_model(trained_model, path)
        assert os.path.isfile(path)

        loaded = load_model(path)
        X, _ = prepare_features(severity_df)
        np.testing.assert_array_equal(
            trained_model.predict(X[:3]),
            loaded.predict(X[:3]),
        )


# --- get_feature_importance ---

def test_feature_importance_length(trained_model):
    pairs = get_feature_importance(trained_model)
    assert len(pairs) == 4


def test_feature_importance_with_names(trained_model):
    names = ["tons", "value", "throughput_ratio", "delay_index"]
    pairs = get_feature_importance(trained_model, feature_names=names)
    returned_names = [p[0] for p in pairs]
    assert set(returned_names) == set(names)


def test_feature_importance_sorted_desc(trained_model):
    pairs = get_feature_importance(trained_model)
    vals = [p[1] for p in pairs]
    assert vals == sorted(vals, reverse=True)


# --- predict_severity ---

def test_predict_severity_clipped(trained_model):
    X = np.array([[9999, 9999, 9999, 9999], [0, 0, 0, 0]])
    preds = predict_severity(trained_model, X)
    assert (preds >= 0).all()
    assert (preds <= 1).all()


def test_predict_severity_shape(trained_model, severity_df):
    X, _ = prepare_features(severity_df)
    preds = predict_severity(trained_model, X)
    assert preds.shape == (40,)


# --- load_data module ---

def test_load_bottleneck_data_missing_file():
    with pytest.raises(FileNotFoundError):
        load_bottleneck_data("/nonexistent/path.csv")


def test_load_bottleneck_data_missing_columns(tmp_path):
    csv = tmp_path / "bad.csv"
    csv.write_text("col_a,col_b\n1,2\n")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_bottleneck_data(str(csv))


def test_load_bottleneck_data_no_tons_columns(tmp_path):
    csv = tmp_path / "notonnage.csv"
    csv.write_text("dms_origst,dms_destst,dms_mode,sctg2\n1,2,1,1\n")
    with pytest.raises(ValueError, match="No tonnage year columns"):
        load_bottleneck_data(str(csv))


def test_load_bottleneck_data_valid(tmp_path):
    csv = tmp_path / "ok.csv"
    csv.write_text("dms_origst,dms_destst,dms_mode,sctg2,tons_2022\n1,2,1,1,100\n")
    df = load_bottleneck_data(str(csv))
    assert len(df) == 1


def test_clean_data_fills_nan():
    df = pd.DataFrame({
        "dms_origst": [1.0, None, 2.0],
        "dms_destst": [2.0, 3.0, 3.0],
        "tons_2022": [100.0, np.nan, 200.0],
    })
    cleaned = clean_data(df)
    assert len(cleaned) == 2  # row with None origst dropped
    assert cleaned["tons_2022"].isna().sum() == 0


def test_get_year_columns():
    df = pd.DataFrame({"value_2020": [1], "value_2022": [2], "other": [3]})
    yc = get_year_columns(df, prefix="value")
    assert yc == {2020: "value_2020", 2022: "value_2022"}


def test_filter_by_mode():
    df = pd.DataFrame({"dms_mode": [1, 2, 1], "x": [10, 20, 30]})
    filtered = filter_by_mode(df, mode_code=1)
    assert len(filtered) == 2
    assert (filtered["dms_mode"] == 1).all()
