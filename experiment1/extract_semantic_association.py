"""
Extract semantic association from linguistic data from Kuperberg et al. (2003)
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


def plot_semantic_association(
    df: pd.DataFrame, model_names: list, title: str = "", save_path: Path = None
):
    plt.figure(figsize=(7, 5))
    colors = ["blue", "purple", "red", "orange"]

    conds = sorted(df["cond"].unique())
    n_conds = len(conds)

    # Dodge offset: spread conditions evenly around 0
    dodge_range = 0.3
    offsets = np.linspace(-dodge_range / 2, dodge_range / 2, n_conds)
    dodge = {cond: offset for cond, offset in zip(conds, offsets)}
    x_positions = {model: i for i, model in enumerate(model_names)}

    for model_name in model_names:
        for cond, group in df.groupby("cond"):
            x = x_positions[model_name] + dodge[cond]
            sem_mean = group[f"semantic_association_{model_name}"].mean()
            sem_std = group[f"semantic_association_{model_name}"].std()
            color = colors[int(cond) - 1]

            # standard deviation
            plt.errorbar(x, sem_mean, yerr=sem_std, capsize=5, color=color)
            # mean
            if model_name == model_names[0]:  # avoiding duplicate labels
                plt.plot(x, sem_mean, "o", color=color, label=int(cond))
            else:
                plt.plot(x, sem_mean, "o", color=color)

    # model names as ticks
    plt.xticks(ticks=range(len(model_names)), labels=model_names)

    plt.legend()
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "Kuperberg", "sentences.xlsx")
    df = pd.read_excel(data_path)

    print("Initializing model(s)")
    models = {
        "SE": SentenceEmbeddingModel("all-MiniLM-L6-v2"),
        "WE": WordEmbeddingModel("enwiki_20180420_100d"),
        "CWE": WordEmbeddingModelContentWord(
            "enwiki_20180420_100d", spacy_model_name="en_core_web_sm"
        ),
    }

    print("extracting semantic association")
    for name, model in models.items():
        df = extract_semantic_association(model, df, model_name=name)

    print("plotting semantic association")
    plot_semantic_association(
        df,
        model_names=list(models.keys()),
        save_path=Path("experiment1", "figs", "semantic_association_kuperberg.png"),
    )
