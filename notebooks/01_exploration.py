# notebooks/01_exploration.py
# Minimum Viable Analysis (MVA) for the Freight & Logistics Bottleneck Analyzer
# - Loads data/raw/sample_bottlenecks.csv
# - Normalizes FAF-style wide year columns (value_YYYY / current_value_YYYY) to long form
# - Computes Top 10 Origin→Destination pairs by value for target year (2022 if present, else latest)
# - Saves results to plots/top10_value.csv
#
# Run from repo root (or inside Codespaces):
#   python notebooks/01_exploration.py

import os
import re
import sys
import pandas as pd

# ---------- Paths ----------
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA_RAW = os.path.join(ROOT, "data", "raw", "sample_bottlenecks.csv")
PLOTS_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

print("Project root:", ROOT)
print("Loading CSV:", DATA_RAW)
if not os.path.exists(DATA_RAW):
    print("ERROR: sample_bottlenecks.csv not found at:", DATA_RAW, file=sys.stderr)
    sys.exit(1)

# ---------- Load ----------
df = pd.read_csv(DATA_RAW)
print("\nColumns:", list(df.columns))

# Utility: case-insensitive column matcher
def find_col(candidates):
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None

# Likely column names in FAF5 extracts
origin_col = find_col(["fr_orig", "orig", "origin", "origin_state", "dms_orig", "dms_origst", "o"])
dest_col   = find_col(["fr_dest", "dest", "destination", "destination_state", "dms_dest", "dms_destst", "d"])
mode_col   = find_col(["dms_mode", "fr_inmode", "mode"])

# Wide year columns (e.g., value_2018, current_value_2024)
value_year_cols = []
for c in df.columns:
    lc = c.lower()
    if re.search(r"(^|_)value_20\d{2}$", lc) or re.search(r"(^|_)current_value_20\d{2}$", lc):
        value_year_cols.append(c)

if not value_year_cols:
    print("\nWARNING: No year-specific value columns found (e.g., value_2022 / current_value_2022).")
    print("This sample may not include value fields. Exiting gracefully.")
    sys.exit(0)

print("\nDetected value-year columns:", value_year_cols[:8], "..." if len(value_year_cols) > 8 else "")

# Parse the year from column names, prefer "current_value_YYYY" over "value_YYYY" when both exist
def parse_year(colname: str) -> int | None:
    m = re.search(r"(?:^|_)(20\d{2})(?:$|_)", colname)
    return int(m.group(1)) if m else None

# Build a preference dict: for each year, pick the best column (current_value_YYYY > value_YYYY)
year_to_col = {}
for c in value_year_cols:
    yr = parse_year(c)
    if yr is None:
        continue
    old = year_to_col.get(yr)
    # prefer 'current_value_' when both present
    if old is None or (c.lower().startswith("current_value_") and not old.lower().startswith("current_value_")):
        year_to_col[yr] = c

years_detected = sorted(year_to_col.keys())
if not years_detected:
    print("\nERROR: Could not infer any years from value columns.")
    sys.exit(1)

print("Years detected:", years_detected)

# ---------- Reshape to long ----------
# Keep only the columns we need to compute OD-by-value per year
keep_cols = [c for c in [origin_col, dest_col, mode_col] if c is not None]
wide = df[keep_cols + list(year_to_col.values())].copy()

# Melt to long format: origin, dest, mode, year, value
long = wide.melt(
    id_vars=keep_cols,
    value_vars=list(year_to_col.values()),
    var_name="value_col",
    value_name="value_million_usd"
)

# Extract year from the melted column name
long["year"] = long["value_col"].apply(parse_year)
long.drop(columns=["value_col"], inplace=True)

# Clean types
if mode_col:
    long[mode_col] = long[mode_col].astype(str)

# Pick target year: 2022 if available, else latest
target_year = 2022 if 2022 in years_detected else years_detected[-1]
print("\nTarget year:", target_year)

# Optional filter to Truck mode when present
if mode_col and any(str(x).lower() == "truck" for x in long[mode_col].dropna().unique()):
    mask = (long["year"] == target_year) & (long[mode_col].str.lower() == "truck")
else:
    mask = (long["year"] == target_year)

subset = long.loc[mask].copy()

# If origin/dest missing, try alternative fallbacks (rare, but defensive)
if origin_col is None or dest_col is None:
    print("\nERROR: Could not find origin/destination columns in the data.")
    print("Looked for columns like fr_orig/dms_origst and fr_dest/dms_destst.")
    sys.exit(1)

# Aggregate value by OD pair
agg = (
    subset
    .groupby([origin_col, dest_col], dropna=False, as_index=False)["value_million_usd"]
    .sum()
    .sort_values("value_million_usd", ascending=False)
    .head(10)
)

# Rename to clean, readable names for output
agg = agg.rename(columns={
    origin_col: "origin",
    dest_col: "destination"
})

print("\nTop 10 OD by value (million USD) —", target_year)
print(agg.to_string(index=False))

# ---------- Save ----------
out_csv = os.path.join(PLOTS_DIR, "top10_value.csv")
agg.to_csv(out_csv, index=False)
print("\nSaved:", out_csv)
