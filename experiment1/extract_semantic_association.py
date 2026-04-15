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

MODEL_REGISTRY = {
    "SentenceEmbedding": SentenceEmbeddingModel,
    "WordEmbedding": WordEmbeddingModel,
    "WordEmbeddingContentWord": WordEmbeddingModelContentWord,
}


def stream_models(config):
    for model_config in config:
        model_type = model_config.pop("model_type")
        implementation = model_config.pop("implementation")

        model_class = MODEL_REGISTRY[model_type]
        model = model_class(**model_config)

        yield (implementation, model)


def extract_semantic_association(model: EmbeddingModel, df: pd.DataFrame):
    """
    Extracts semantic association for targets in df using the embedding model

    Args:
        model: Embedding model used to extract semantic association
        df: dataframe with targets and contexts (as two columns by that name in the df)
        model_name: name of the embedding model. Used as subfix in naming the column.
    """
    assert all([(col in df.columns) for col in ["target", "context"]])

    df = df[df["target"].notna()]

    df["semantic_association"] = df.apply(
        lambda row: model.get_semantic_association(
            word=row["target"], context=row["context"]
        ),
        axis=1,
    )
    return df


def plot_semantic_association(
    df: pd.DataFrame, title: str = "", save_path: Path = None
):
    plt.figure(figsize=(7, 5))
    colors = ["blue", "purple", "red", "orange"]

    # Dodge offset: spread conditions evenly around 0
    conds = sorted(df["cond"].unique())
    n_conds = len(conds)
    implementations = df["implementation"].unique()
    dodge_range = 0.3
    offsets = np.linspace(-dodge_range / 2, dodge_range / 2, n_conds)
    dodge = {cond: offset for cond, offset in zip(conds, offsets)}
    x_positions = {model: i for i, model in enumerate(implementations)}

    for (implementation, cond), group in df.groupby(["implementation", "cond"]):
        x = x_positions[implementation] + dodge[cond]
        sem_mean = group["semantic_association"].mean()
        sem_std = group["semantic_association"].std()
        color = colors[int(cond) - 1]

        # standard deviation
        plt.errorbar(x, sem_mean, yerr=sem_std, capsize=5, color=color)
        # mean
        if implementation == implementations[0]:  # avoiding duplicate labels
            plt.plot(x, sem_mean, "o", color=color, label=int(cond))
        else:
            plt.plot(x, sem_mean, "o", color=color)

    # model names as ticks
    plt.xticks(ticks=range(len(implementations)), labels=implementations)

    plt.legend()
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


if __name__ == "__main__":
    data_path = Path("experiment1", "data", "Kuperberg", "sentences.xlsx")
    out_path = Path("experiment1", "results", "kuperberg_semantic_association.csv")
    df = pd.read_excel(data_path)

    config = [
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "intfloat/multilingual-e5-large",
        },
        # {
        #     "implementation": "SE",
        #     "model_type": "SentenceEmbedding",
        #     "model_name": "jinaai/jina-embeddings-v5-text-small",
        # },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "BAAI/bge-m3",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Gameselo/STS-multilingual-mpnet-base-v2",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "intfloat/e5-large-v2",
        },
        {
            "implementation": "WE",
            "model_type": "WordEmbedding",
            "model_name": "enwiki_20180420_100d",
        },
        {
            "implementation": "WE",
            "model_type": "WordEmbedding",
            "model_name": "enwiki_20180420_300d",
        },
        {
            "implementation": "WE",
            "model_type": "WordEmbedding",
            "model_name": "word2vec-google-news-300",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "enwiki_20180420_100d",
            "spacy_model_name": "en_core_web_sm",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "enwiki_20180420_300d",
            "spacy_model_name": "en_core_web_sm",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "word2vec-google-news-300",
            "spacy_model_name": "en_core_web_sm",
        },
        {
            "implementation": "BERTWE",
            "model_type": "SentenceEmbedding",
            "model_name": "FacebookAI/xlm-roberta-large",
        },
    ]

    print("Extracting semantic association")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        df_sem = extract_semantic_association(model, df)

        # save output
        append_df_to_csv(
            df_sem,
            path=out_path,
            extra_cols={"implementation": name, "model": model.model_name},
        )

    # print("Plotting semantic association")
    # df_results = pd.read_csv(out_path)
    # plot_semantic_association(
    #     df_results,
    #     save_path=Path("experiment1", "figs", "semantic_association_kuperberg.png"),
    # )
