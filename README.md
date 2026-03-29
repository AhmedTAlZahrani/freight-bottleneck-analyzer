# Freight Bottleneck Analyzer

![CI Pipeline](https://github.com/AhmedTAlZahrani/freight-bottleneck-analyzer/actions/workflows/ci.yml/badge.svg)

A research tool for identifying and quantifying freight transport bottlenecks
across U.S. state-to-state corridors using the FAF5.7.1 dataset (2018-2024).

## Methodology

The analysis follows three stages:

1. **Indicator computation.** We derive three corridor-level metrics from the
   FAF5 origin-destination data: a throughput ratio (value per ton), a delay
   index (ton-miles per ton, as a proxy for routing inefficiency), and a
   composite severity score that combines both.

2. **Bottleneck ranking.** Corridors are ranked by severity score to surface
   the state pairs where congestion has the greatest economic impact relative
   to freight volume.

3. **Predictive model.** A Random Forest regressor is trained on the indicator
   features to predict severity scores, enabling what-if analysis on new or
   projected freight flows.

## Data

- **Sample (included):** `data/raw/sample_bottlenecks.csv` -- 50 rows from FAF5.7.1
- **Full dataset:** [FAF5.7.1 State OD 2018-2024](https://faf.ornl.gov/faf5/Data/FAF5.7.1/faf5.7.1_od_state_2018_2024.csv.zip) (87 MB)

Column definitions are documented in `docs/data_notes.md`.

## Repository Structure

    src/
        load_data.py       Load and validate the FAF5 CSV
        indicators.py      Throughput ratio, delay index, severity score
        ai_model.py        RandomForest training, evaluation, persistence
        viz.py             Bar chart generation
        main.py            End-to-end pipeline
    notebooks/
        01_exploration.py  Data exploration and Top-10 OD extraction
    tests/
        test_indicators.py Unit tests for indicator functions
    docs/
        data_notes.md      Dataset column dictionary
        roadmap.md         Project phases and status
    data/raw/              Source CSV
    plots/                 Generated charts and model artifacts

## Quickstart

```bash
pip install -r requirements.txt

# Run the exploration script
python notebooks/01_exploration.py

# Run the full pipeline (indicators + model)
python src/main.py

# Run tests
pytest tests/
```

## Current Scope

- Transport mode: Truck (FAF mode code 1)
- Analysis year: 2022
- Geography: U.S. state-level origin-destination pairs

## Limitations

- The delay index is a proxy derived from ton-miles/tons, not from actual
  travel time or GPS data. Real congestion measurement would require
  additional data sources (e.g., NPMRDS, ATRI truck GPS).
- The sample dataset (50 rows) is too small for robust model training;
  results on the full FAF5 dataset will differ.
- Severity scores are normalized within the dataset and are not comparable
  across different data subsets without re-calibration.

## References

- Bureau of Transportation Statistics, Freight Analysis Framework v5
  (https://faf.ornl.gov/faf5/)
- FHWA Freight Bottleneck Reporting Guidebook, 2018
