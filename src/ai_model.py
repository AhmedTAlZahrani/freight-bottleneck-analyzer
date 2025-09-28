# src/ai_model.py
# ML model for predicting bottleneck severity from freight features.

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def prepare_features(severity_df):
    """Build feature matrix and target from the severity DataFrame.

    Args:
        severity_df: Output of indicators.compute_severity_score(), must
            contain columns: tons, value, throughput_ratio, delay_index,
            severity_score.

    Returns:
        Tuple of (X, y) as numpy arrays.
    """
    feature_cols = ["tons", "value", "throughput_ratio", "delay_index"]
    X = severity_df[feature_cols].values
    y = severity_df["severity_score"].values
    return X, y


def split_data(X, y, test_size=0.25, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_model(X, y, n_estimators=100, random_state=42):
    """Train a RandomForest regressor on freight features.

    Returns:
        Fitted RandomForestRegressor.
    """
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=8,
        random_state=random_state,
    )
    model.fit(X, y)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance.

    Args:
        model: Trained sklearn estimator.
        X_test: Test feature matrix.
        y_test: True target values.

    Returns:
        Dict with r2 and mae.
    """
    preds = model.predict(X_test)
    return {
        "r2": r2_score(y_test, preds),
        "mae": mean_absolute_error(y_test, preds),
    }


def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)


def load_model(path):
    return joblib.load(path)


def get_feature_importance(model, feature_names=None):
    importances = model.feature_importances_
    if feature_names is None:
        feature_names = ["f{}".format(i) for i in range(len(importances))]
    pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
    return pairs


def predict_severity(model, X):
    """Run inference on new data and return predictions."""
    preds = model.predict(X)
    return np.clip(preds, 0, 1)
