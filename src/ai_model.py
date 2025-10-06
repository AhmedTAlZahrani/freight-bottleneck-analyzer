# src/ai_model.py
# Predict freight value using a simple AI regression model (scikit-learn)

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT, "data", "raw", "sample_bottlenecks.csv")

print("📦 Loading data from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

# --- Select numeric features for modeling ---
features = ["tons_2022", "dist_band", "tmiles_2022"]  # adjust if needed
target = "value_2022"

# Drop missing values
df = df.dropna(subset=features + [target])
X = df[features]
y = df[target]

# --- Split and train ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"✅ Model trained: R²={r2:.3f}, MAE={mae:.2f}")
print("Example predictions:")
for i in range(5):
    print(f" Predicted={y_pred[i]:.2f} | Actual={y_test.iloc[i]:.2f}")

# --- Save model output ---
OUT_PATH = os.path.join(ROOT, "plots", "ai_predictions.csv")
pd.DataFrame({"actual": y_test.values, "predicted": y_pred}).to_csv(OUT_PATH, index=False)
print("💾 Saved predictions to:", OUT_PATH)
