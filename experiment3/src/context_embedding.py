"""
Exploring the context embedding of the different embedding models
"""

from pathlib import Path
import sys
import pandas as pd
import numpy as np
from functools import cache
from heapq import nlargest, nsmallest

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel

# from src.word_embedding_models import WordEmbeddingModel, WordEmbeddingModelContentWord
from src.sentence_embedding_models import SentenceEmbeddingModel
from src.append_to_csv import append_df_to_csv

# MODEL_REGISTRY = {
#     "SentenceEmbedding": SentenceEmbeddingModel,
#     "WordEmbedding": WordEmbeddingModel,
#     "WordEmbeddingContentWord": WordEmbeddingModelContentWord,
# }


# def stream_models(config):
#     for model_config in config:
#         model_type = model_config.pop("model_type")
#         implementation = model_config.pop("implementation")

#         model_class = MODEL_REGISTRY[model_type]
#         model = model_class(**model_config)

#         yield (implementation, model)


def high_low_similarity_words(
    model: EmbeddingModel, context: str, words: list[str], N: int
):
    """
    Get N highest and N lowest similarity words
    """
    if N > len(words):
        raise ValueError("N larger than number of words!")

    similarities = [
        (word, model.get_semantic_association(word=word, context=context))
        for word in words
    ]

    return {
        "high": nlargest(N, similarities, key=lambda x: x[1]),
        "low": nsmallest(N, similarities, key=lambda x: x[1]),
    }


def get_word_list(path: Path):
    """Get list of content words from SUBTLEX-US"""
    df = pd.read_excel(path)
    pos_include = ["Noun", "Verb", "Adjective", "Adverb"]
    df = df[df["Dom_PoS_SUBTLEX"].isin(pos_include)]
    df = df[df["Zipf-value"] > df["Zipf-value"].mean()]
    return df["Word"].to_list()


if __name__ == "__main__":
    context = "A wolf and a fox once lived together. The fox, who was the weaker of the two, had to do all the hard work, which made him anxious to leave his companion."

    print("Loading Models")
    models = [
        SentenceEmbeddingModel("intfloat/e5-large-v2"),
        SentenceEmbeddingModel("BAAI/bge-m3"),
        SentenceEmbeddingModel("whaleloops/phrase-bert"),
    ]
    print("Making word list")
    # words = get_word_list(Path("experiment1", "data", "SUBTLEX-US.xlsx"))
    words = [
        "fox",
        "wolf",
        "pancake",
        "eat",
        "sheep",
        "whale",
        "door",
        "book",
        "run",
        "drive",
        "tree",
        "house",
        "computer",
        "tall",
        "fluffy",
        "red",
        "blue",
    ]
    print("Calculating similarities")
    for model in models:
        print(model.model_name)
        print(high_low_similarity_words(model=model, context=context, words=words, N=3))
