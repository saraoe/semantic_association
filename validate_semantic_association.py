"""
Using the data from Federmeier & Kutas (1999) to validate measures of semantic association
The code is imported from the error-analysis github repo
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.embedding_model import EmbeddingModel
from src.word_embedding_models import (
    WordEmbeddingModel,
    WordEmbeddingModelContentWord,
    WordEmbeddingModelWeighted,
    WordEmbeddingModelWindowed,
)
from src.sentence_embedding_models import SentenceEmbeddingModel


class validation_federmeier_kutas:
    def __init__(
        self,
        model: EmbeddingModel,
        context: str = "original",  # original or longer
        translated: bool = False,
    ):
        self.model = model

        self.context = context
        self.target_cols = ["expected", "within", "between", "unexpected"]

        self.read_data(translated=translated)

    def read_data(self, data_path: Path = Path("data"), translated: bool = False):
        self.data = pd.read_csv(data_path / "federmeier_kutas_1999.csv")
        if translated:
            en_cols = ["context"] + self.target_cols
            self.data = self.data.drop(columns=en_cols)
            self.data = self.data.rename(
                columns={f"translated_{col}": col for col in en_cols}
            )
            self.data = self.data.dropna()

    def semantic_association_targets(self, row):
        """
        Get semantic association for all three target words
        """
        if self.context == "original":
            context = row["context"]
        elif self.context == "long":
            context = f"{row["longer_context"]} {row["context"]}"

        # calculate semantic association to targets
        sem_associations = {}
        for target in self.target_cols:
            word = row[target]
            sem_association = self.model.get_semantic_association(word, context)
            sem_associations[target] = sem_association

        sem_associations["constraint"] = row["constraint"]
        return sem_associations

    def validate(self):
        """
        Calculates the semantic association for all the contexts with all the targets
        """
        validation = []
        for i in range(len(self.data.index)):
            row = self.data.iloc[i]
            validation_dict = self.semantic_association_targets(row)
            validation.append(validation_dict)

        validation_df = pd.DataFrame.from_dict(validation)
        return validation_df


def plot_validation(df: pd.DataFrame, title: str, save_path: Path = None):
    target_cols = ["expected", "within", "between", "unexpected"]
    colors = ["blue", "purple", "red", "orange"]

    plt.figure(figsize=(7, 5))

    # standard deviation
    for constraint, group in df.groupby("constraint"):
        for target, c in zip(target_cols, colors):
            plt.errorbar(
                constraint,  # x position
                group[target].mean(),  # y value
                yerr=group[target].std(),  # error bar
                color=c,
                capsize=5,  # nice little horizontal caps
            )
            # plt.plot(
            #     [constraint for _ in range(len(group))],
            #     group[target],
            #     ".",
            #     color=c,
            #     alpha=0.2,
            # )

    # mean
    for constraint, group in df.groupby("constraint"):
        for target, c in zip(target_cols, colors):
            if constraint == "H":  # to avoid duplicate labels
                plt.plot(constraint, group[target].mean(), "o", color=c, label=target)
            else:
                plt.plot(constraint, group[target].mean(), "o", color=c)

    plt.legend()
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


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


if __name__ == "__main__":
    model_configs = [
        {
            "model": SentenceEmbeddingModel("all-MiniLM-L6-v2"),
            "embedding_model": "SentenceEmbedding",
            "context": ["original", "long"],
        },
        {
            "model": SentenceEmbeddingModel("intfloat/multilingual-e5-large"),
            "embedding_model": "SentenceEmbedding",
            "context": ["original", "long"],
        },
        {
            "model": SentenceEmbeddingModel("all-MiniLM-L6-v2", n_sentences=5),
            "embedding_model": "SentenceEmbedding",
            "context": ["long"],
        },
        {
            "model": SentenceEmbeddingModel(
                "intfloat/multilingual-e5-large", n_sentences=5
            ),
            "embedding_model": "SentenceEmbedding",
            "context": ["long"],
        },
        {
            "model": WordEmbeddingModel("enwiki_20180420_100d"),
            "embedding_model": "WordEmbedding",
            "context": ["original", "long"],
        },
        {
            "model": WordEmbeddingModel("word2vec-google-news-300"),
            "embedding_model": "WordEmbedding",
            "context": ["original", "long"],
        },
        {
            "model": WordEmbeddingModelContentWord("enwiki_20180420_100d"),
            "embedding_model": "WordEmbeddingContentWord",
            "context": ["original", "long"],
        },
        {
            "model": WordEmbeddingModelContentWord("word2vec-google-news-300"),
            "embedding_model": "WordEmbeddingContentWord",
            "context": ["original", "long"],
        },
        {
            "model": WordEmbeddingModel("enwiki_20180420_100d", n_sentences=5),
            "embedding_model": "WordEmbedding",
            "context": ["long"],
        },
        {
            "model": WordEmbeddingModel("word2vec-google-news-300", n_sentences=5),
            "embedding_model": "WordEmbedding",
            "context": ["long"],
        },
        {
            "model": WordEmbeddingModelContentWord(
                "enwiki_20180420_100d", n_sentences=5
            ),
            "embedding_model": "WordEmbeddingContentWord",
            "context": ["long"],
        },
        {
            "model": WordEmbeddingModelContentWord(
                "word2vec-google-news-300", n_sentences=5
            ),
            "embedding_model": "WordEmbeddingContentWord",
            "context": ["long"],
        },
        {
            "model": WordEmbeddingModelWindowed("enwiki_20180420_100d", n_words=1),
            "embedding_model": "WordEmbeddingContentWord",
            "n_words": 1,
            "context": ["original"],
        },
        {
            "model": WordEmbeddingModelWindowed("word2vec-google-news-300", n_words=1),
            "embedding_model": "WordEmbeddingContentWord",
            "n_words": 1,
            "context": ["original"],
        },
        {
            "model": WordEmbeddingModelWindowed("enwiki_20180420_100d", n_words=2),
            "embedding_model": "WordEmbeddingContentWord",
            "n_words": 2,
            "context": ["original"],
        },
        {
            "model": WordEmbeddingModelWindowed("word2vec-google-news-300", n_words=1),
            "embedding_model": "WordEmbeddingContentWord",
            "n_words": 2,
            "context": ["original"],
        },
        {
            "model": WordEmbeddingModelWeighted("enwiki_20180420_100d"),
            "embedding_model": "WordEmbeddingWeighted",
            "context": ["original", "long"],
        },
        {
            "model": WordEmbeddingModelWeighted("word2vec-google-news-300"),
            "embedding_model": "WordEmbeddingWeighted",
            "context": ["original", "long"],
        },
    ]

    results_path = Path("results", "federmeier_kutas_validation.csv")
    # remove file if exists
    if results_path.exists():
        results_path.unlink()

    for config in model_configs:
        print(f"Validating: {config}")

        translated = config.get("translated", False)

        for context in config["context"]:
            model = config["model"]
            val_fk = validation_federmeier_kutas(
                model=model,
                context=context,
                translated=translated,
            )
            validation_df = val_fk.validate()

            # save output
            append_df_to_csv(
                validation_df,
                extra_cols={
                    "embedding_model": config["embedding_model"],
                    "model_name": model.model_name,
                    "language": "nl" if translated else "en",
                    "context": context,
                    "n_sentences": model.n_sentences - 1 if model.n_sentences else None,
                    "n_words": config.get("n_words", None),
                },
                path=results_path,
            )
