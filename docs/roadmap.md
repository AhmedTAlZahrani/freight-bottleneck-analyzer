# Freight & Logistics Bottleneck Analyzer — Roadmap

## Phase 0 — Repo setup (today)
- [x] Create repo and README
- [x] Add `data/raw/sample_bottlenecks.csv`
- [ ] Add folder stubs: `src/`, `notebooks/`, `plots/`, `tests/`, `docs/`
- [ ] Add `requirements.txt` with placeholders (pandas, numpy, scikit-learn, matplotlib, geopandas [later])

## Phase 1 — Data understanding (non-technical)
- [ ] Document the dataset dictionary (what each column means) in `docs/data_notes.md`
- [ ] Decide initial scope: **one mode** (Truck) and **one year** (e.g., 2022)
- [ ] Define key indicators and formulas:
  - Delay proxy: use travel time / speed fields if available, or start with value/tons by OD as a baseline
  - Vehicle operating cost (VOC) assumption (e.g., $/mile placeholder)
  - CO₂ factor assumption (e.g., kg CO₂ per idling hour per truck as placeholder)
- [ ] Draft a small list of “target questions” (e.g., Top 10 OD state pairs by value/tons in 2022)

## Phase 2 — Minimum Viable Analysis (MVA)
- [ ] Notebook: `notebooks/01_exploration.ipynb`
  - Load **sample_bottlenecks.csv**
  - Show row count, unique origins/destinations, years
  - Produce one simple table: **Top 10 OD pairs by value (one year)**
  - Export that table to `plots/top10_table.csv`
- [ ] README: add a “Quickstart” section explaining how to reproduce the table

## Phase 3 — Indicators (first draft)
- [ ] `src/indicators.py` functions:
  - `top_od_by_value(df, year, n=10)`
  - `top_od_by_tons(df, year, n=10)`
- [ ] Notebook update to call these functions and save outputs (CSV in `plots/`)

## Phase 4 — Visualization (first draft)
- [ ] `src/viz.py`: bar chart for Top 10 OD by value
- [ ] Save chart to `plots/top10_value.png`
- [ ] README: add the image

## Phase 5 — AI/Forecast (stub only)
- [ ] `src/ai_model.py`: create a placeholder `train_baseline_model(df)` that just returns “todo”
- [ ] Notebook `02_ai_prediction.ipynb`: outline features you’ll try later (seasonality, DoW, etc.)

## Phase 6 — Professional polish
- [ ] Add `LICENSE` (MIT)
- [ ] Add “Data Sources” + “Assumptions” sections to README
- [ ] Open GitHub Issues for each task above and group them into Milestones: “MVA”, “Indicators”, “Viz”, “AI”
