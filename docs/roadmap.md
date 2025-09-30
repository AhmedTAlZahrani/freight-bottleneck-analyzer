# Freight & Logistics Bottleneck Analyzer -- Roadmap

## Phase 0 -- Repo setup
- [x] Create repo and README
- [x] Add `data/raw/sample_bottlenecks.csv`
- [x] Add folder stubs: `src/`, `notebooks/`, `plots/`, `tests/`, `docs/`
- [x] Add `requirements.txt`

## Phase 1 -- Data understanding
- [x] Document the dataset dictionary in `docs/data_notes.md`
- [x] Decide initial scope: Truck mode, year 2022
- [x] Define key indicators (throughput ratio, delay index, severity score)

## Phase 2 -- Minimum Viable Analysis
- [x] `notebooks/01_exploration.py` -- load, reshape, Top 10 OD pairs
- [x] Export results to `plots/top10_value.csv`

## Phase 3 -- Indicators
- [x] `src/indicators.py` -- throughput ratio, delay index, severity score
- [x] `src/load_data.py` -- data loading and cleaning functions

## Phase 4 -- Visualization
- [x] `src/viz.py` -- bar chart for Top 10 OD by value
- [ ] Save chart to `plots/top10_value.png` (run viz.py after exploration)

## Phase 5 -- AI / ML model
- [x] `src/ai_model.py` -- RandomForest severity prediction
- [x] `src/main.py` -- end-to-end pipeline orchestration
- [ ] Notebook `02_ai_prediction.ipynb` -- detailed model exploration

## Phase 6 -- Polish
- [ ] Add `LICENSE` (MIT)
- [ ] Open GitHub Issues and Milestones
