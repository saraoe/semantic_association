"""
Using the data from Federmeier & Kutas (1999) to validate meassures of semantic association
The code is imported from the error-analysis github repo
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

from src.embedding_model import WordEmbeddingModel, SentenceEmbeddingModel, get_pos


class validation_federmeier_kutas:
    def __init__(
        self,
        embedding_model: str,
        model_name: str,
        include_pos: list = [],
        context_length: int = None,
        translated: bool = False,
    ):
        if embedding_model == "word_embedding":
            self.model = WordEmbeddingModel(Path("models", f"{model_name}.txt"))
        elif embedding_model == "sentence_embedding":
            self.model = SentenceEmbeddingModel(model_name)
        else:
            raise ValueError(f"No model matching {embedding_model}!")

        self.include_pos = include_pos
        self.context_length = context_length
        self.target_cols = ["expected", "within", "between", "unexpected"]

        self.read_data(translated=translated)

    def read_data(self, data_path: Path = Path("data"), translated: bool = False):
        self.data = pd.read_excel(data_path / "federmeier_kutas_1999.xlsx")
        if translated:
            en_cols = ["context"] + self.target_cols
            self.data = self.data.drop(columns=en_cols)
            self.data = self.data.rename(
                columns={f"translated_{col}": col for col in en_cols}
            )
            self.data = self.data.dropna()

    def update_include_pos(self, include_pos: list):
        self.include_pos = include_pos

    def update_context_length(self, context_length: int):
        self.context_length = context_length

    def prepare_context(self, context):
        """Returns context, with only word with POS tags from include_pos and a length of context_length"""
        if not self.include_pos and not self.context_length:
            return context

        context_list = context.split(" ")
        if self.include_pos:
            context_list = [
                w
                for w in context_list
                if get_pos(re.sub(r"\W+", "", w)) in self.include_pos
            ]
        if self.context_length:
            context_list = context_list[-self.context_length :]
        return " ".join(context_list)

    def get_semantic_association(self, row):
        """
        Get semantic association for all three target words
        """
        # get embedding for context
        context = row["context"]
        context = self.prepare_context(context)
        context_emb = self.model.get_embedding(context)

        if (
            context_emb is np.nan
        ):  # if all the words in the context are not included in the model
            sem_associations = {target: np.nan for target in self.target_cols}
            sem_associations["constraint"] = row["constraint"]
            return sem_associations

        # calculate semantic association to targets
        sem_associations = {}
        for target in self.target_cols:
            # get word embedding of the target
            word = row[target]
            word_emb = self.model.get_embedding(word)

            # if the target doesn't have an embedding
            if word_emb is np.nan:
                print(f"{word} not in embedding model!")
                sem_associations[target] = np.nan
                continue

            # calculate semantic association to context embedding
            sem_association = self.model.semantic_association_context(
                word_emb, context_emb
            )
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
            tmp = self.get_semantic_association(row)
            validation.append(tmp)

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
    model_configs = [
        {
            "embedding_model": "word_embedding",
            "model_name": "enwiki_20180420_100d",
            "language": "en",
            "include_pos": ["all", "content"],
            "context_lengths": [None, 4, 8],
        },
        {
            "embedding_model": "word_embedding",
            "model_name": "word2vec-google-news-300",
            "language": "en",
            "include_pos": ["all", "content"],
            "context_lengths": [None, 4, 8],
        },
        {
            "embedding_model": "sentence_embedding",
            "model_name": "all-MiniLM-L6-v2",
            "language": "en",
            "include_pos": ["all"],
            "context_lengths": [None, 4, 8],
        },
        {
            "embedding_model": "sentence_embedding",
            "model_name": "intfloat/multilingual-e5-large",
            "language": "en",
            "include_pos": ["all"],
            "context_lengths": [None, 4, 8],
        },
        # {
        #     "embedding_model": "word_embedding",
        #     "model_name": "nlwiki_20180420_100d",
        #     "language": "nl",
        #     "context_lengths": [None, 4, 8],
        # },
    ]

    for config in model_configs:
        print(f"Validation: {config}")

        translated = True if config["language"] == "nl" else False

        val_fk = validation_federmeier_kutas(
            embedding_model=config["embedding_model"],
            model_name=config["model_name"],
            translated=translated,
        )
        for pos in config["include_pos"]:
            print(f">> validate include pos {pos}")
            if config["embedding_model"] == "word_embedding":
                if pos == "all":
                    include_pos = []
                elif pos == "content":
                    include_pos = ["NOUN", "VERB", "ADJ", "ADV"]
                val_fk.update_include_pos(include_pos)
            if pos != "all" and config["embedding_model"] == "sentence_embedding":
                raise ValueError(
                    "It's not possible to include on some POS tags for sentence embedding models!"
                )

            for c_len in config["context_lengths"]:
                print(f">> validate context length {c_len}")

                val_fk.update_context_length(c_len)

                validation_df = val_fk.validate()

                # name the saved output
                if re.search("/", config["model_name"]):
                    model_name = re.split("/", config["model_name"])[-1]
                else:
                    model_name = config["model_name"]
                base_name = f"{config["language"]}_context_{c_len}_pos_{pos}_{config["embedding_model"]}_{model_name}"

                validation_df.to_csv(
                    Path("results", "federmeier_kutas", f"{base_name}.csv")
                )
                plot_validation(
                    validation_df,
                    title=f"Context length = {c_len}, included words = {pos}",
                    save_path=Path(
                        "figs",
                        f"{base_name}.png",
                    ),
                )
