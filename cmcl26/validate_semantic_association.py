"""
Using the data from Federmeier & Kutas (1999) to validate measures of semantic association
The code is imported from the error-analysis github repo
"""

from pathlib import Path
import tomllib
import pandas as pd
import matplotlib.pyplot as plt

from src.embedding_model import EmbeddingModel
from src.word_embedding_models import (
    WordEmbeddingModel,
    WordEmbeddingModelContentWord,
    WordEmbeddingModelWeighted,
    WordEmbeddingModelWindowed,
    WordEmbeddingModelContentWordWeighted,
)
from src.sentence_embedding_models import (
    SentenceEmbeddingModel,
    SentenceEmbeddingModelSingleWord,
    SentenceEmbeddingModelSingleWordContentWord,
)
from cmcl26.src.append_to_csv import append_df_to_csv


MODEL_REGISTRY = {
    "SentenceEmbedding": SentenceEmbeddingModel,
    "SentenceEmbeddingSingleWord": SentenceEmbeddingModelSingleWord,
    "SentenceEmbeddingSingleWordContentWord": SentenceEmbeddingModelSingleWordContentWord,
    "WordEmbedding": WordEmbeddingModel,
    "WordEmbeddingContentWord": WordEmbeddingModelContentWord,
    "WordEmbeddingWindowed": WordEmbeddingModelWindowed,
    "WordEmbeddingWeighted": WordEmbeddingModelWeighted,
    "WordEmbeddingContentWordWeighted": WordEmbeddingModelContentWordWeighted,
}


def stream_models(config_path):
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    for model_config in config["models"]:
        model_type = model_config.pop("model_type")
        context = model_config.pop("context")
        language = model_config.pop("language")

        # All remaining keys in model_config get passed to the constructor
        model_class = MODEL_REGISTRY[model_type]
        model = model_class(**model_config)

        # Rebuild the dict with all original config values
        yield {
            "model": model,
            "embedding_model": model_type,
            "context": context,
            "language": language,
            **model_config,  # Include any extra args like n_words
        }


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


if __name__ == "__main__":
    results_path = Path("cmcl26", "results", "federmeier_kutas_validation.csv")
    config_path = Path("cmcl26", "model_configs")
    # remove file if exists
    if results_path.exists():
        results_path.unlink()

    for config in stream_models(config_path / "models_validation_config.toml"):
        print(f"Validating: {config}")

        language = config["language"]
        assert language in ["en", "nl"]
        translated = False if language == "en" else True

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
                    "language": language,
                    "context": context,
                    "n_sentences": model.n_sentences - 1 if model.n_sentences else None,
                    "n_words": config.get("n_words", None),
                },
                path=results_path,
            )
