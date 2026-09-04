# ma-dcr-beaches

Tracking current public beach postings in Massachusetts.

> The water quality at public beaches in Massachusetts is required to be monitored. When the water quality is unsafe, the beach is required to be “posted” with a sign that indicates swimming is unsafe and may cause illness. 
Source: [DCR](https://www.mass.gov/info-details/interactive-beach-water-quality-dashboard)

## Setup

```
pip install -r requirements.txt
```

## Usage

- `python process_v2/scrape_postings.py` — pulls the current statewide beach postings from the [DPH Beach Water Quality Dashboard](https://datavisualization.dph.mass.gov/views/BeachWaterQualityDashboard/Closures), writes `Beach_Status_List.csv`, and archives a dated copy to `process_v2/outputs/postings-YYYY-MM-DD.csv`. This is what `.github/workflows/update.yml` runs daily to keep both up to date.
- `python process_v2/join_csvs.py [--year YYYY]` — combines the accumulated daily snapshots for one year (default: the current year) into one wide season table, `static_data/postings_summer_YYYY.csv` (one row per beach, one column per date). Run automatically weekly by `.github/workflows/update-season-summary.yml`; you can also run it by hand any time.
- `python process/scrape_csvs.py` / `python process/join_csvs.py` — legacy scripts that built the 2023 season archive (`static_data/postings_summer_2023.csv`) from mass.gov's old daily CSV files, which mass.gov has since discontinued in favor of the dashboard above.

Based on and inspired by https://github.com/simonw/sf-tree-history 🙌
