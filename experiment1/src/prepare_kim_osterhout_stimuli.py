"""
Extract target words and preceding contexts from sentences from Kim and Osterhout, 2005
"""

from pathlib import Path
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def get_context_and_target(sentence: str):
    doc = nlp(sentence)
    # get index of target, i.e., first verb
    verb_idxs = [token.i for token in doc if token.pos_ == "VERB"]
    if len(verb_idxs) == 0:
        return None, None
    target_idx = verb_idxs[0]

    # fix that the adjective is occasionally recognized as a verb
    if target_idx <= 3 and (len(verb_idxs)) > 1:
        target_idx = verb_idxs[1]

    context = doc[:target_idx].text
    target = doc[target_idx].text
    return context, target


def write_context_target(data_path: Path):
    df = pd.read_csv(data_path)
    df[["context", "target"]] = df["sentence"].apply(
        lambda x: pd.Series(get_context_and_target(x))
    )
    df.to_csv(data_path, index=False)


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "kim_osterhout_2005_stim.csv")
    write_context_target(data_path)
