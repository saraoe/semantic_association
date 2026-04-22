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


def plot_similarity_matrix(similarity_matrix, words=None):
    plt.imshow(similarity_matrix, cmap="viridis", interpolation="nearest")
    plt.colorbar()

    if words is not None:
        ticks = range(len(words))
        plt.xticks(ticks, words, rotation=90)
        plt.yticks(ticks, words)

    plt.tight_layout()
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

    plot_similarity_matrix(sm1, words_with_embeddings)
    plot_similarity_matrix(sm2, words_with_embeddings)

    # rsa
    return calc_rsa(sm1, sm2)


if __name__ == "__main__":
    print("Initializing WE model")
    we_model = WordEmbeddingModel("enwiki_20180420_100d")
    print("Initializing SE model")
    se_model = SentenceEmbeddingModel("intfloat/multilingual-e5-large")

    # words = ["dragon", "nomad", "house", "chair", "fish", "horse", "water", "sea"]
    subtlex = pd.read_excel(Path("experiment1", "data", "SUBTLEX-US.xlsx"))
    words = subtlex["Word"].to_list()[:100]

    print("Calculating RSA")
    r, p_value = rsa_word_embeddings(model1=we_model, model2=se_model, words=words)
    print(f"Pearson r: {r:.4f}, p-value: {p_value:.4e}")
