import pandas as pd
from pathlib import Path


def append_df_to_csv(
    df: pd.DataFrame,
    path: Path,
    extra_cols: dict = {},
):
    for col_name, values in extra_cols.items():
        df[col_name] = values
    if not path.exists():
        print(f"creating df {path}")
        df.to_csv(path)
    else:
        print(f"appending df to {path}")
        df.to_csv(path, mode="a", header=False)
