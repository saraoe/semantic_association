import pandas as pd
from pathlib import Path
import spacy
from spacy.symbols import ORTH


def get_pos(token):
    # hardcode exceptions
    if token.text in ["…", ",", "'", "-", "'s", "’s", "'ve", "’ve", "n't", "n’t"]:
        return "PUNCT"
    return token.pos_


def add_pos_to_stim(stim_path, id_cols, spacy_model="en_core_web_sm"):
    stim_df = pd.read_csv(stim_path)
    stim_df_len = len(stim_df)
    # sort by id and word_n
    stim_df.sort_values(by=id_cols + ["word_n"])

    nlp = spacy.load(spacy_model)
    # manually add tokens with "-"
    special_cases = ["cross-country", "gray-haired", "ill-natured", "by-ways"]
    for word in special_cases:
        nlp.tokenizer.add_special_case(word, [{ORTH: word}])

    pos_col = []
    index_col = []
    for name, group in stim_df.groupby(id_cols):
        text = " ".join(group["target"])
        pos = [get_pos(word) for word in nlp(text) if get_pos(word) != "PUNCT"]

        assert len(group) == len(pos)
        pos_col += pos
        index_col += list(group.index)

    df = pd.DataFrame({"index": index_col, "pos": pos_col})

    stim_df["index"] = stim_df.index
    stim_df = stim_df.merge(df, on="index")
    assert not any(stim_df["pos"].isna())
    assert len(stim_df) == stim_df_len
    stim_df = stim_df.drop(columns=["Unnamed: 0", "index"])

    stim_df.to_csv(stim_path)


if __name__ == "__main__":
    data_path = Path("experiment2", "data")

    datasets = [
        # ("Tanner", ["id"]),
        ("DERCo", ["article_n"])
    ]

    for dataset_folder, ids in datasets:
        add_pos_to_stim(stim_path=data_path / dataset_folder / "stim.csv", id_cols=ids)
