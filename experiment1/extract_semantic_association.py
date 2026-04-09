"""
Extract semantic association from linguistic data from Kuperberg et al. (2003)
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel
from src.word_embedding_models import WordEmbeddingModel, WordEmbeddingModelContentWord
from src.sentence_embedding_models import SentenceEmbeddingModel
from src.append_to_csv import append_df_to_csv


def extract_semantic_association(
    model: EmbeddingModel, df: pd.DataFrame, model_name: str = ""
):
    """
    Extracts semantic association for targets in df using the embedding model

    Args:
        model: Embedding model used to extract semantic association
        df: dataframe with targets and contexts (as two columns by that name in the df)
        model_name: name of the embedding model. Used as subfix in naming the column.
    """
    assert all([(col in df.columns) for col in ["target", "context"]])

    df = df[df["target"].notna()]

    df[f"semantic_association_{model_name}"] = df.apply(
        lambda row: model.get_semantic_association(
            word=row["target"], context=row["context"]
        ),
        axis=1,
    )
    return df


def plot_semantic_association(df: pd.DataFrame, title: str, save_path: Path = None):
    plt.figure(figsize=(7, 5))

    # standard deviation
    for cond, group in df.groupby("cond"):
        plt.errorbar(
            cond,
            group["semantic_association"].mean(),
            yerr=group["semantic_association"].std(),  # error bar
            capsize=5,  # horizontal caps
            color="black",
        )

    # mean
    for cond, group in df.groupby("cond"):
        plt.plot(cond, group["semantic_association"].mean(), "o", color="black")

    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "Kuperberg", "sentences.xlsx")
    df = pd.read_excel(data_path)

    print("Initializing model")
    # model = SentenceEmbeddingModel("all-MiniLM-L6-v2")
    # model = WordEmbeddingModel("enwiki_20180420_100d")
    model = WordEmbeddingModelContentWord(
        "enwiki_20180420_100d", spacy_model_name="en_core_web_sm"
    )

    print("extracting semantic association")
    df = extract_semantic_association(model, df)

    print("plotting semantic association")
    plot_semantic_association(
        df,
        title="CWE",
        save_path=Path("experiment1", "figs", "semantic_association_kuperberg_CWE.png"),
    )
