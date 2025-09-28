# 01_exploration — Minimum Viable Analysis (MVA)

import os
import pandas as pd

# ---------- Paths ----------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_RAW = os.path.join(ROOT, "data", "raw", "sample_bottlenecks.csv")
PLOTS_DIR = os.path.join(ROOT, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

print("Project root:", ROOT)
print("Loading:", DATA_RAW)

# ---------- Load ----------
df = pd.read_csv(DATA_RAW)
print("\nColumns:", list(df.columns))
print("\nPreview:")
display(df.head())

# ---------- Try to standardize likely column names ----------
def pick(colnames, candidates):
    for c in candidates:
        if c in colnames:
            return c
    return None

cols = [c.lower() for c in df.columns]
mapper = {c: c.lower() for c in df.columns}  # original -> lower

# Likely candidates in FAF-like files
origin_col = pick(cols, ["orig", "origin", "origin_state", "dms_orig", "o"])
dest_col   = pick(cols, ["dest", "destination", "destination_state", "dms_dest", "d"])
year_col   = pick(cols, ["year", "yr"])
mode_col   = pick(cols, ["mode", "dms_mode"])
value_col  = pick(cols, ["value", "val_milusd", "val", "dollars", "million_dollars"])

needed = {
    "origin": origin_col,
    "dest": dest_col,
    "year": year_col,
    "mode": mode_col,
    "value": value_col,
}
print("\nDetected columns:", needed)

missing = [k for k, v in needed.items() if v is None and k in ["origin","dest","year","value"]]
if missing:
    raise ValueError(f"Missing required columns for quick analysis: {missing}")

# restore original case for selected columns
def orig_case(lower_name):
    for k, v in mapper.items():
        if v == lower_name:
            return k
    return lower_name

origin_col = orig_case(origin_col)
dest_col   = orig_case(dest_col)
year_col   = orig_case(year_col)
value_col  = orig_case(value_col)
mode_col   = orig_case(mode_col) if mode_col else None

# ---------- Basic facts ----------
print("\nBasic facts:")
print("Rows:", len(df))
print("Unique origins:", df[origin_col].nunique())
print("Unique destinations:", df[dest_col].nunique())
print("Years available:", sorted(df[year_col].dropna().unique().tolist()))

# pick a year (use 2022 if present, else most recent)
years = sorted([int(y) for y in df[year_col].dropna().unique()])
target_year = 2022 if 2022 in years else years[-1]
print("Target year for MVA:", target_year)

# optionally filter by truck mode if present
if mode_col and "truck" in set(str(x).lower() for x in df[mode_col].unique()):
    df_year = df[(df[year_col] == target_year) & (df[mode_col].str.lower() == "truck")]
else:
    df_year = df[df[year_col] == target_year]

# ---------- Top 10 OD by value ----------
agg = (
    df_year
    .groupby([origin_col, dest_col], dropna=False)[value_col]
    .sum()
    .reset_index()
    .sort_values(value_col, ascending=False)
    .head(10)
)

# nicer column names for output
agg = agg.rename(columns={
    origin_col: "origin",
    dest_col: "destination",
    value_col: "value_million_usd"
})

print("\nTop 10 OD pairs by value (", target_year, "):", sep="")
display(agg)

# ---------- Save output ----------
out_csv = os.path.join(PLOTS_DIR, "top10_value.csv")
agg.to_csv(out_csv, index=False)
print("\nSaved:", out_csv)
