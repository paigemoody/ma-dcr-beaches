import argparse
import os
from datetime import date

import pandas as pd

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def process_csv_files(input_dir, output_file, year):
    df_list = []
    date_columns = {}

    for filename in sorted(os.listdir(input_dir)):
        if not filename.endswith(".csv"):
            continue

        file_year, month, day = filename.removeprefix("postings-").removesuffix(".csv").split("-")
        if file_year != str(year):
            continue
        date_str = f"{month}_{day}"
        new_column_name = f"posting_reason_{date_str}"

        df = pd.read_csv(os.path.join(input_dir, filename))
        df.rename(columns={"Posting Reason": new_column_name}, inplace=True)
        df.set_index(["Municipality", "Beach"], inplace=True)

        date_columns[date_str] = new_column_name
        df_list.append(df)

    merged_df = pd.concat(df_list, axis=1, join="outer")
    merged_df.reset_index(inplace=True)
    merged_df.sort_values(by="Municipality", inplace=True)

    sorted_columns = ["Municipality", "Beach"] + [date_columns[d] for d in sorted(date_columns.keys())]
    merged_df = merged_df[sorted_columns]

    merged_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=date.today().year)
    args = parser.parse_args()

    output_csv = os.path.join("static_data", f"postings_summer_{args.year}.csv")
    process_csv_files(OUTPUTS_DIR, output_csv, args.year)
    print(f"Wrote season summary to {output_csv}")
