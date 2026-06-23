"""
Extract semantic association from linguistic data from Dutch corpora
"""

from pathlib import Path
import sys
import pandas as pd

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from experiment1.src.extract_semantic_association import (
    stream_models,
    extract_for_corpus,
)


if __name__ == "__main__":
    corpora = [
        {
            "df": pd.read_excel(Path("experiment1", "data", "Hoeks", "stim.csv")),
            "out_path": Path(
                "experiment1", "results", "hoeks_semantic_association.csv"
            ),
        },
    ]

    config = [
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "clips/e5-large-trm-nl",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "intfloat/multilingual-e5-large",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Gameselo/STS-multilingual-mpnet-base-v2",
        },
        {
            "implementation": "SE",
            "model_type": "SentenceEmbedding",
            "model_name": "Qwen/Qwen3-Embedding-8B",
        },
        {
            "implementation": "WE",
            "model_type": "WordEmbedding",
            "model_name": "nlwiki_20180420_100d",
        },
        {
            "implementation": "WE",
            "model_type": "WordEmbedding",
            "model_name": "nlwiki_20180420_300d",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "nlwiki_20180420_100d",
            "spacy_model_name": "nl_core_news_sm",
        },
        {
            "implementation": "CWE",
            "model_type": "WordEmbeddingContentWord",
            "model_name": "nlwiki_20180420_300d",
            "spacy_model_name": "nl_core_news_sm",
        },
    ]

    print("Extracting semantic association")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        for corpus in corpora:
            extract_for_corpus(
                df=corpus["df"],
                model=model,
                implementation_name=name,
                out_path=corpus["out_path"],
            )
            del model  # unload model
