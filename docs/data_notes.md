# Data Notes (FAF5 State OD)

**Source:** FAF5.7.1 State database 2018-2024
**Link:** https://faf.ornl.gov/faf5/Data/FAF5.7.1/faf5.7.1_od_state_2018_2024.csv.zip

## Column Dictionary

| Column | Description |
|--------|-------------|
| `fr_orig` | Origin state abbreviation (e.g., CA, TX). Blank for intra-state flows. |
| `dms_origst` | Origin state FIPS code (numeric). |
| `dms_destst` | Destination state FIPS code (numeric). |
| `fr_dest` | Destination state abbreviation. Blank for intra-state flows. |
| `fr_inmode` | Inbound transport mode code. |
| `dms_mode` | Primary transport mode (1=Truck, 2=Rail, 4=Air, 5=Multiple modes, 6=Pipeline). |
| `fr_outmode` | Outbound transport mode code. |
| `sctg2` | Standard Classification of Transported Goods, 2-digit code. |
| `trade_type` | 1=Domestic, 2=Import, 3=Export. |
| `dist_band` | Distance band category (1=under 100mi, 2=100-249mi, etc.). |
| `tons_YYYY` | Thousands of tons shipped in year YYYY. |
| `value_YYYY` | Millions of USD (constant 2017 dollars) in year YYYY. |
| `current_value_YYYY` | Millions of USD (current-year dollars) in year YYYY. |
| `tmiles_YYYY` | Millions of ton-miles in year YYYY. |

Years available: 2018, 2019, 2020, 2021, 2022, 2023, 2024.

## Scope (current analysis)

- **Mode:** Truck (dms_mode = 1)
- **Year:** 2022
- **Sample size:** 50 rows in `data/raw/sample_bottlenecks.csv`
- Full dataset (87 MB) available at the link above

## Notes

- Some rows have blank `fr_orig`/`fr_dest` fields; these represent intra-state
  or aggregated flows and can be identified by their FIPS codes instead.
- The `current_value` columns are nominal dollars; the `value` columns are
  inflation-adjusted to 2017 base year.
