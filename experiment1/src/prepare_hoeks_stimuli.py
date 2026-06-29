"""
Extract target words and preceding contexts from sentences from Hoeks, 2004
"""

from pathlib import Path
import pandas as pd
import re


def extract_stim(row):
    pattern = re.compile(
        r"^(?P<np1>.+?)(?=\s+werd(?:en)?)\s+"  # up until werd/werden
        r"(?P<passive>werd(?:en)?(?:\s+\w+)*)\s*/\s*"
        r"(?P<active>heeft|hebben)\s+"
        r"(?P<np2>.+?)\s+"
        r"(?P<goodverb>\S+)\s*/\s*"
        r"(?P<poorverb>\S+)\.$"
    )

    m = pattern.match(row["sentences"])

    if not m:
        return []

    np1 = m.group("np1")
    passive = m.group("passive").strip()
    active = m.group("active")
    np2 = m.group("np2")
    goodverb = m.group("goodverb")
    poorverb = m.group("poorverb")

    return [
        {
            "item": row["item"],
            "condition": "goodFit_strongConstraint",
            "sentence": f"{np1} {passive} {np2} {goodverb}.",
            "target": goodverb,
            "context": f"{np1} {passive} {np2}",
            "translation": row["translation"],
        },
        {
            "item": row["item"],
            "condition": "goodFit_weakConstraint",
            "sentence": f"{np1} {active} {np2} {goodverb}.",
            "target": goodverb,
            "context": f"{np1} {active} {np2}",
            "translation": row["translation"],
        },
        {
            "item": row["item"],
            "condition": "badFit_strongConstraint",
            "sentence": f"{np1} {passive} {np2} {poorverb}.",
            "target": poorverb,
            "context": f"{np1} {passive} {np2}",
            "translation": row["translation"],
        },
        {
            "item": row["item"],
            "condition": "badFit_weakConstraint",
            "sentence": f"{np1} {active} {np2} {poorverb}.",
            "target": poorverb,
            "context": f"{np1} {active} {np2}",
            "translation": row["translation"],
        },
    ]


def write_stim(data_path: Path, out_path: Path):
    sentences_df = pd.read_csv(data_path)
    rows = []
    for _, row in sentences_df.iterrows():
        rows.extend(extract_stim(row))

    stim_df = pd.DataFrame(rows)
    stim_df.to_csv(out_path)


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "Hoeks", "sentences.csv")
    out_path = Path("experiment1", "data", "Hoeks", "stim.csv")
    write_stim(data_path, out_path)
