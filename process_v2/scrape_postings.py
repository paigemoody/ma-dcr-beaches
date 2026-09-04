import argparse
import os
from datetime import date

from tableauscraper import TableauScraper as TS

DASHBOARD_URL = "https://datavisualization.dph.mass.gov/views/BeachWaterQualityDashboard/Closures"
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def fetch_postings():
    ts = TS()
    ts.loads(DASHBOARD_URL)
    workbook = ts.getWorkbook()
    closure_table = next((w for w in workbook.worksheets if w.name == "ClosureTable"), None)
    if closure_table is None:
        raise RuntimeError('Worksheet "ClosureTable" not found in dashboard workbook')
    df = closure_table.data.rename(
        columns={
            "Town-alias": "Municipality",
            "Beach-alias": "Beach",
            "Posting Reason-alias": "Posting Reason",
        }
    )[["Municipality", "Beach", "Posting Reason"]]
    return df.sort_values(["Municipality", "Beach"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="Beach_Status_List.csv")
    args = parser.parse_args()

    postings = fetch_postings()
    postings.to_csv(args.output, index=False)
    print(f"Wrote {len(postings)} postings to {args.output}")

    # Archive today's snapshot so join_csvs.py can later fold it into a season
    # summary, the same way process/outputs/ fed process/join_csvs.py.
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    snapshot_path = os.path.join(OUTPUTS_DIR, f"postings-{date.today().strftime('%m-%d')}.csv")
    postings.to_csv(snapshot_path, index=False)
    print(f"Archived snapshot to {snapshot_path}")
