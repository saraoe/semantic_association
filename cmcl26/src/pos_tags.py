import pandas as pd
from pathlib import Path
import spacy

data_path = Path("cmcl26", "data")
tint_df = pd.read_csv(data_path / "tint.csv")
tint_df = tint_df.drop(columns=["pos", "content_word"])
tint_df_len = len(tint_df)
stim_df = pd.read_csv(data_path / "tint_stim.csv")
stim_df = stim_df.drop(columns=["pos"])
stim_df_len = len(stim_df)

nlp = spacy.load("nl_core_news_sm")


def get_pos(token):
    # hardcode exceptions
    if token.text in ["…", ",", "°", "C"]:
        return "PUNCT"
    return token.pos_


pos_col = []
index_col = []
for name, group in stim_df.groupby(["document_id", "paragraph_n"]):
    paragraph = " ".join(group["word"])
    pos = [get_pos(word) for word in nlp(paragraph) if get_pos(word) != "PUNCT"]

    assert len(group) == len(pos)
    pos_col += pos
    index_col += list(group.index)

df = pd.DataFrame({"index": index_col, "pos": pos_col})

stim_df["index"] = stim_df.index
stim_df = stim_df.merge(df, on="index")
assert not any(stim_df["pos"].isna())
assert len(stim_df) == stim_df_len
stim_df = stim_df.drop(columns=["Unnamed: 0", "index"])

tint_df = tint_df.merge(stim_df, how="left")
assert not any(tint_df["pos"].isna())
assert len(tint_df) == tint_df_len
tint_df = tint_df.drop(columns=["Unnamed: 0"])

tint_df.to_csv(data_path / "tint.csv")
stim_df.to_csv(data_path / "tint_stim.csv")
