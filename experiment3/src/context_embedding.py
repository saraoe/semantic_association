"""
Exploring the context embedding of the different embedding models
"""

from pathlib import Path
import sys
import pandas as pd
import numpy as np
from heapq import nlargest, nsmallest
import json

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
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


def high_low_similarity_words(
    model: EmbeddingModel,
    context_embedding: np.ndarray,
    word_embeddings: list[tuple],
    n: int,
):
    """
    Get N highest and N lowest similarity words
    """
    if n < 1:
        raise ValueError("n must be positive")
    if n > len(word_embeddings):
        raise ValueError("N larger than number of words!")

    similarities = [
        (
            word,
            float(
                model.similarity(context_embedding, word_embedding, measure="cosine")
            ),
        )
        for word, word_embedding in word_embeddings
    ]

    return {
        "high": nlargest(n, similarities, lambda x: x[1]),
        "low": nsmallest(n, similarities, lambda x: x[1]),
    }


def load_subtlex_vocab(path: Path):
    """Get list of content words from SUBTLEX-US"""
    df = pd.read_excel(path, keep_default_na=False, na_values=["", "NA", "NaN"])

    # include only content words
    pos_include = ["Noun", "Verb", "Adjective", "Adverb"]
    df = df[df["Dom_PoS_SUBTLEX"].isin(pos_include)]

    # keep only higher frequency words (higher than average)
    df = df[df["Zipf-value"] > df["Zipf-value"].mean()]
    return df["Word"].to_list()


def load_word2vec_vocab(path):
    with open(path, encoding="utf-8") as f:
        next(f)  # Skip header
        return [line.split(" ", 1)[0] for line in f]


def extract_words_similar_to_context_embeddings(
    model: EmbeddingModel,
    implementation_name: str,
    corpus_df: pd.DataFrame,
    out_path: Path,
    word_list: list[str] | None = None,
):
    """
    Inspects context embeddings of a corpus by finding words that have highest and lowest similarity.
    Writes results to ndjson-file (out_path).
    A specific list of words can be given (word_list). If not, the content words in the corpus_df (word_clean) will be used.
    """
    assert all(
        [col in corpus_df.columns for col in ["context", "id", "target", "word_n"]]
    )

    print(">> Getting word embeddings")
    if not word_list:
        corpus_df_cw = corpus_df[corpus_df["pos"].isin(["NOUN", "VERB", "ADJ", "ADV"])]
        word_list = corpus_df_cw["word_clean"].drop_duplicates().tolist()
    assert all([isinstance(word, str) for word in word_list])
    word_embeddings = [
        (word, np.asarray(model.get_embedding(word))) for word in word_list
    ]

    print(">> Calculating similarities")
    results = []
    for row in corpus_df.itertuples(index=False):
        # get context embedding
        context = row.context
        context_embedding = model.get_embedding(context)
        context_embedding = np.asarray(context_embedding)

        # calculate similarities
        similarity_words = high_low_similarity_words(
            model=model,
            context_embedding=context_embedding,
            word_embeddings=word_embeddings,
            n=10,
        )

        # add extra columns
        similarity_words["context"] = context
        similarity_words["id"] = row.id
        similarity_words["word_n"] = row.word_n
        similarity_words["target"] = row.target
        results.append(similarity_words)

    model_results = {
        "model": model.model_name,
        "implementation": implementation_name,
        "similarity_words": results,
    }

    with open(out_path, "a") as f:
        f.write(json.dumps(model_results) + "\n")


if __name__ == "__main__":
    # whether to overwrite the output file (if false, it appends to the file)
    overwrite = True

    # read df
    derco_df = pd.read_csv(Path("experiment2", "data", "DERCo", "stim.csv"))
    derco_df = derco_df.rename(columns={"article_n": "id"})
    derco_df = derco_df.dropna(subset=["context"])

    config = [
        # {
        #     "implementation": "SE",
        #     "model_type": "SentenceEmbedding",
        #     "model_name": "intfloat/multilingual-e5-large",
        # },
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
        # {
        #     "implementation": "SE",
        #     "model_type": "SentenceEmbedding",
        #     "model_name": "Gameselo/STS-multilingual-mpnet-base-v2",
        # },
        # {
        #     "implementation": "SE",
        #     "model_type": "SentenceEmbedding",
        #     "model_name": "bigscience/sgpt-bloom-7b1-msmarco",
        # },
        # {
        #     "implementation": "SE",
        #     "model_type": "SentenceEmbedding",
        #     "model_name": "Qwen/Qwen3-Embedding-8B",
        # },
        # {
        #     "implementation": "WE",
        #     "model_type": "WordEmbedding",
        #     "model_name": "enwiki_20180420_300d",
        # },
        # {
        #     "implementation": "WE",
        #     "model_type": "WordEmbedding",
        #     "model_name": "word2vec-google-news-300",
        # },
        # {
        #     "implementation": "CWE",
        #     "model_type": "WordEmbeddingContentWord",
        #     "model_name": "enwiki_20180420_300d",
        #     "spacy_model_name": "en_core_web_sm",
        # },
        # {
        #     "implementation": "CWE",
        #     "model_type": "WordEmbeddingContentWord",
        #     "model_name": "word2vec-google-news-300",
        #     "spacy_model_name": "en_core_web_sm",
        # },
    ]

    # creating out path
    out_path = Path(
        "experiment3", "results", "word_similarity_context_embeddings.ndjson"
    )
    out_folder = out_path.parent
    out_folder.mkdir(parents=True, exist_ok=True)

    if overwrite:
        out_path.unlink(missing_ok=True)  # delete out_path if exists

    print("Extracting words similar to contexts")
    for name, model in stream_models(config):
        print(f"{name}: {model.model_name}")
        extract_words_similar_to_context_embeddings(
            model=model,
            implementation_name=name,
            corpus_df=derco_df,
            out_path=out_path,
            # word_list=words,
        )
        del model  # unload model
