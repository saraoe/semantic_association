"""
Extract semantic association from linguistic data
"""

from pathlib import Path
import sys
import pandas as pd
import numpy as np
from functools import cache

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


def extract_semantic_association(
    model: EmbeddingModel,
    implementation_name: str,
    df: pd.DataFrame,
    out_path: Path,
    batch_size: int = None,
):
    """
    Extracts semantic association for targets in df using the embedding model

    Args:
        model: Embedding model used to extract semantic association.
        implementation_name: Name of the implementation (e.g., SE or WE)
        df: dataframe with targets and contexts (as two columns by that name in the df).
        out_path: path for where to save df.
        batch_size: optional argument to set batch size for processing df.
    """
    assert all([(col in df.columns) for col in ["target", "context"]])

    @cache
    def get_association(context, target):
        if pd.isna(context):
            return None
        return model.get_semantic_association(word=target, context=context)

    if batch_size:
        n_batches = len(df) // batch_size
        for i, batch_df in df.groupby(np.arange(len(df)) // batch_size):
            print(f"Batch {i}/{n_batches}")
            batch_df["semantic_association"] = batch_df.apply(
                lambda row: get_association(row["context"], row["target"]), axis=1
            )
            # save output
            append_df_to_csv(
                batch_df,
                path=out_path,
                extra_cols={
                    "implementation": implementation_name,
                    "model": model.model_name,
                },
            )
    else:
        df["semantic_association"] = df.apply(
            lambda row: get_association(row["context"], row["target"]), axis=1
        )
        # save output
        append_df_to_csv(
            df,
            path=out_path,
            extra_cols={
                "implementation": implementation_name,
                "model": model.model_name,
            },
        )


if __name__ == "__main__":
    corpora = [
        # {
        #     "name": "tanner",
        #     "df": pd.read_csv(
        #         Path("experiment2", "data", "Tanner", "stim.csv"), index_col=0
        #     ),
        #     "out_path": Path(
        #         "experiment2", "results", "tanner_semantic_association.csv"
        #     ),
        # },
        {
            "name": "ucl",
            "df": pd.read_csv(
                Path("experiment2", "data", "UCL", "stim.csv"), index_col=0
            ),
            "out_path": Path("experiment2", "results", "ucl_semantic_association.csv"),
        },
        # {
        #     "name": "derco",
        #     "df": pd.read_csv(
        #         Path("experiment2", "data", "DERCo", "stim.csv"), index_col=0
        #     ),
        #     "out_path": Path(
        #         "experiment2", "results", "derco_semantic_association.csv"
        #     ),
        # },
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
            "model_name": "bigscience/sgpt-bloom-7b1-msmarco",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-8B",
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
    # add Sentence(N=1)
    config = config + [
        {
            **entry,
            "implementation": entry["implementation"] + "_sentences1",
            "n_sentences": 1,
        }
        for entry in config
    ]

    print("Extracting semantic association")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        for corpus in corpora:
            # only do Sentence(N=1) for DERCo
            if model.n_sentences and corpus["name"] != "derco":
                continue
            extract_semantic_association(
                df=corpus["df"],
                implementation_name=name,
                model=model,
                out_path=corpus["out_path"],
                batch_size=100,
            )
