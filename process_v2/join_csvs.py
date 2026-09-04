import os

import pandas as pd

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def process_csv_files(input_dir, output_file):
    df_list = []
    date_columns = {}

    for filename in sorted(os.listdir(input_dir)):
        if not filename.endswith(".csv"):
            continue

        date_str = filename.removeprefix("postings-").removesuffix(".csv").replace("-", "_")
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
    output_csv = os.path.join("static_data", "postings_summer_2026.csv")
    process_csv_files(OUTPUTS_DIR, output_csv)
    print(f"Wrote season summary to {output_csv}")
