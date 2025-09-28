# src/viz.py
# Turn plots/top10_value.csv into a bar chart image: plots/top10_value.png

import os
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IN_CSV = os.path.join(ROOT, "plots", "top10_value.csv")
OUT_IMG = os.path.join(ROOT, "plots", "top10_value.png")

df = pd.read_csv(IN_CSV)

# Build a nice label like "CA → TX"
df["od"] = df["origin"].astype(str) + " \u2192 " + df["destination"].astype(str)

# Sort descending just in case
df = df.sort_values("value_million_usd", ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(df["od"], df["value_million_usd"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Value (million USD)")
plt.title("Top 10 State OD Pairs by Freight Value")
plt.tight_layout()
plt.savefig(OUT_IMG, dpi=150)
print("Saved:", OUT_IMG)
