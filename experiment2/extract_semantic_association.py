"""
Extract semantic association from linguistic data
"""

from pathlib import Path
import sys
import pandas as pd

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

    def get_association(row):
        if pd.isna(row["context"]):
            return None
        return model.get_semantic_association(
            word=row["target"], context=row["context"]
        )

    df["semantic_association"] = df.apply(get_association, axis=1)
    return df


def extract_for_corpus(df: pd.DataFrame, model: EmbeddingModel, out_path: Path):
    """
    extracts semantic association for data in corpus
    """
    assert [col in df.columns for col in ["target", "context"]]

    df_sem = extract_semantic_association(model, df)

    # save output
    append_df_to_csv(
        df_sem,
        path=out_path,
        extra_cols={"implementation": name, "model": model.model_name},
    )


if __name__ == "__main__":
    corpora = [
        {
            "df": pd.read_csv(
                Path("experiment2", "data", "Tanner", "stim.csv"), index_col=0
            ),
            "out_path": Path(
                "experiment2", "results", "tanner_semantic_association.csv"
            ),
        },
    ]

    config = [
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "intfloat/multilingual-e5-large",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "intfloat/e5-large-v2",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "whaleloops/phrase-bert",
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
            "model_name": "enwiki_20180420_300d",
            "spacy_model_name": "en_core_web_sm",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "word2vec-google-news-300",
            "spacy_model_name": "en_core_web_sm",
        },
    ]

    print("Extracting semantic association")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        for corpus in corpora:
            extract_for_corpus(
                df=corpus["df"], model=model, out_path=corpus["out_path"]
            )
