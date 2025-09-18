# src/main.py
# Orchestrates the full analysis pipeline:
#   load data -> compute indicators -> train model -> save results

# TODO: add CLI arguments

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.load_data import load_bottleneck_data, clean_data, filter_by_mode
from src.indicators import compute_severity_score
from src.ai_model import prepare_features, split_data, train_model, evaluate_model, save_model


def main():
    data_path = os.path.join(ROOT, "data", "raw", "sample_bottlenecks.csv")
    model_path = os.path.join(ROOT, "plots", "severity_model.joblib")

    print("Loading data from {}".format(data_path))
    df = load_bottleneck_data(data_path)

    print("Cleaning data...")
    df = clean_data(df)

    print("Filtering to truck mode (mode=1)")
    df = filter_by_mode(df, mode_code=1)
    print("Rows after filter: {}".format(len(df)))

    print("Computing severity scores...")
    severity = compute_severity_score(df, year=2022)
    print("Corridors scored: {}".format(len(severity)))

    print("Preparing features and training model...")
    X, y = prepare_features(severity)
    X_train, X_test, y_train, y_test = split_data(X, y)

    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    print("Model R2: {:.4f}  MAE: {:.4f}".format(metrics["r2"], metrics["mae"]))

    save_model(model, model_path)
    print("Model saved to", model_path)

    # Save severity table
    out_csv = os.path.join(ROOT, "plots", "severity_scores.csv")
    severity.to_csv(out_csv, index=False)
    print("Severity scores saved to", out_csv)

    print("Done.")


if __name__ == "__main__":
    main()
