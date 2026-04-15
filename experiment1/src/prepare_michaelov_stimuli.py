"""
Extract target words and preceding contexts from sentences from Michaelov, 2024
"""

from pathlib import Path
import pandas as pd


def get_context(target: str, sentence: str):
    words = sentence.split(" ")

    # remove sentence-final word
    assert words[-1] == target
    context = " ".join(words[:-1])

    return context


def write_context_target(data_path: Path, out_path: Path):
    df = pd.read_csv(data_path)
    # get only stimuli
    df = df.drop(columns=["Subject", "N400", "Electrode"])
    df = df.drop_duplicates()

    # create target and row columns
    df = df.rename(columns={"TargetWord": "target"})
    df["context"] = df.apply(
        lambda row: get_context(target=row["target"], sentence=row["Sentence"]),
        axis=1,
    )

    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "michaelov_2024.csv")
    out_path = Path("experiment1", "data", "michaelov_2024_stim.csv")
    write_context_target(data_path, out_path)
