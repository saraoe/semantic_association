"""
Extract target words and preceding contexts from sentences from Kuperberg, 2003 and 2007
"""

"""
Extract semantic association from linguistic data from Kuperberg et al. (2003)
"""

from pathlib import Path
import sys
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def get_context_and_target(sentence: str):
    doc = nlp(sentence)
    # get index of target, i.e., last verb
    verb_idxs = [token.i for token in doc if token.pos_ == "VERB"]
    if len(verb_idxs) == 0:
        return None, None
    target_idx = verb_idxs[-1]

    context = doc[:target_idx].text
    target = doc[target_idx].text
    return context, target


def write_context_target(data_path: Path):
    df = pd.read_excel(data_path)
    df[["context", "target"]] = df["sentences"].apply(
        lambda x: pd.Series(get_context_and_target(x))
    )
    df.to_excel(data_path, index=False)


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "Kuperberg", "sentences.xlsx")
    write_context_target(data_path)
