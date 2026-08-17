"""
Extract semantic association from (English) linguistic data
"""

from pathlib import Path
import sys
import pandas as pd

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from experiment2.extract_semantic_association import *

from src.word_embedding_models import WordEmbeddingModel, WordEmbeddingModelContentWord
from src.sentence_embedding_models import SentenceEmbeddingModel

MODEL_REGISTRY = {
    "SentenceEmbedding": SentenceEmbeddingModel,
    "WordEmbedding": WordEmbeddingModel,
    "WordEmbeddingContentWord": WordEmbeddingModelContentWord,
}

if __name__ == "__main__":
    corpora = [
        {
            "name": "derco",
            "df": pd.read_csv(
                Path("experiment3", "data", "DERCo", "stim.csv"), index_col=0
            ),
            "out_path": Path(
                "experiment3", "results", "derco_semantic_association.csv"
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
            "model_name": "BAAI/bge-m3",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-8B",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-0.6B",
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
    # add Sentence(N=10), Sentence(N=1) and entire context for Qwen models
    config = [
        {
            **entry,
            "implementation": entry["implementation"],
            "n_sentences": 10,
        }
        for entry in config
    ] + [
        {
            **entry,
            "implementation": entry["implementation"] + "_sentences1",
            "n_sentences": 1,
        }
        for entry in config
    ] + [
        {
            "implementation": "SE_all",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-8B",
        },
        {
            "implementation": "SE_all",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-0.6B",
        }
    ]

    print("Extracting semantic association")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        for corpus in corpora:
            extract_semantic_association(
                df=corpus["df"],
                implementation_name=name,
                model=model,
                out_path=corpus["out_path"],
                batch_size=100,
            )
        del model  # unload model
