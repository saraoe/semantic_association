"""
Representational Similarly Analysis (RSA) for word-level embeddings from WE and SE
"""

from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from itertools import combinations
import random

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from src.word_embedding_models import WordEmbeddingModel
from src.sentence_embedding_models import SentenceEmbeddingModel


def get_word_embeddings(words, *models):
    valid_words = []
    all_embeddings = [[] for _ in models]

    def is_valid(embedding):
        return embedding is not np.nan

    for word in words:
        embeddings = [model.get_embedding(word) for model in models]

        if all(is_valid(e) for e in embeddings):
            valid_words.append(word)
            for emb_list, e in zip(all_embeddings, embeddings):
                emb_list.append(e)

    return valid_words, all_embeddings


def calc_similarity_matrix(embeddings: np.array, distance_metric="cosine"):
    """
    calculate the similarity matrix of all the representations
    """
    return squareform(pdist(embeddings, metric=distance_metric))


def plot_similarity_matrix(
    similarity_matrix, tick_names=None, save_path=None, min_max=None
):
    if min_max:
        min_value, max_value = min_max
        plt.imshow(
            similarity_matrix,
            cmap="PiYG",
            interpolation="nearest",
            vmin=min_value,
            vmax=max_value,
        )
    else:
        plt.imshow(similarity_matrix, cmap="PiYG", interpolation="nearest")
    plt.colorbar()

    if tick_names is not None:
        ticks = range(len(tick_names))
        plt.xticks(ticks, tick_names, rotation=90)
        plt.yticks(ticks, tick_names)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


def calc_rsa(sm1, sm2):
    """
    calculates the representational similarity between two similarity matrices (sm1 and sm2) using pearson correlation
    """
    # Extract upper triangular indices (excluding diagonal)
    triu_indices = np.triu_indices_from(sm1, k=1)
    vec1 = sm1[triu_indices]
    vec2 = sm2[triu_indices]
    return pearsonr(vec1, vec2)


def rsa_word_embeddings(model1, model2, words):
    # get word embeddings
    words_with_embeddings, (embeddings1, embeddings2) = get_word_embeddings(
        words, model1, model2
    )

    # similarity matrices
    sm1 = calc_similarity_matrix(embeddings1)
    sm2 = calc_similarity_matrix(embeddings2)

    # plot_similarity_matrix(sm1, words_with_embeddings)
    # plot_similarity_matrix(sm2, words_with_embeddings)

    # rsa
    return calc_rsa(sm1, sm2)


def rsa_multiple_models(words, models, save_plot=False):
    """
    Perform RSA across all pairs of models.

    Args:
        words: List of words to embed.
        models: List of any number of embedding models.
        save_plot: Whether to save per-model similarity matrices.

    Returns:
        corr_df:  DataFrame of Pearson r values.
    """
    n = len(models)
    model_names = [model.model_name for model in models]

    # Get embeddings from models
    words_with_embeddings, all_embeddings = get_word_embeddings(words, *models)
    print(
        f"Ratio of valid words across all models: {len(words_with_embeddings) / len(words)}"
    )

    # Compute similarity matrix per model
    similarity_matrices = []
    for embeddings in all_embeddings:
        sm = calc_similarity_matrix(np.array(embeddings))
        similarity_matrices.append(sm)

    # Compute all pairwise RSA correlations
    corr_matrix = np.eye(n)  # diagonal = 1
    for i, j in combinations(range(n), 2):
        r, _ = calc_rsa(similarity_matrices[i], similarity_matrices[j])
        corr_matrix[i, j] = r
        corr_matrix[j, i] = r  # symmetric

    corr_df = pd.DataFrame(corr_matrix, index=model_names, columns=model_names)

    plot_similarity_matrix(
        corr_df, tick_names=model_names, save_path=save_plot, min_max=(-1, 1)
    )

    return corr_df


if __name__ == "__main__":
    print("Initializing WE model(s)")
    we_models = [
        WordEmbeddingModel("enwiki_20180420_100d"),
        WordEmbeddingModel("enwiki_20180420_300d"),
        WordEmbeddingModel("word2vec-google-news-300"),
    ]
    print("Initializing SE model(s)")
    se_models = [
        SentenceEmbeddingModel("intfloat/multilingual-e5-large"),
        SentenceEmbeddingModel("intfloat/e5-large-v2"),
        SentenceEmbeddingModel("whaleloops/phrase-bert"),
        SentenceEmbeddingModel("BAAI/bge-m3"),
        SentenceEmbeddingModel("Gameselo/STS-multilingual-mpnet-base-v2"),
    ]

    subtlex = pd.read_excel(Path("experiment1", "data", "SUBTLEX-US.xlsx"))
    subtlex = subtlex[subtlex["FREQcount"] > 2]
    words = random.sample(subtlex["Word"].to_list(), 500)

    print("Calculating RSA")
    rsa_multiple_models(
        words, we_models + se_models, save_plot=Path("figs", "rsa_we.png")
    )
