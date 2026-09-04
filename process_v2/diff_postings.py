import argparse

import pandas as pd

# csv-diff's --key only accepts a single column, but Beach names aren't unique
# across municipalities (e.g. "Sandy Beach" in both Danvers and Swansea), so a
# plain --key=Beach can misattribute changes between rows. This adds a
# combined Municipality+Beach key column to keyed copies of each file, which
# csv-diff can then use as a real unique row identifier.


def add_key(path):
    df = pd.read_csv(path)
    df.insert(0, "Key", df["Municipality"] + " - " + df["Beach"])
    keyed_path = path.replace(".csv", "-keyed.csv")
    df.to_csv(keyed_path, index=False)
    return keyed_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("old")
    parser.add_argument("new")
    args = parser.parse_args()

    print(add_key(args.old))
    print(add_key(args.new))
