"""
Calculate semantic association using embeddings
"""

from pathlib import Path
import numpy as np
import re
from numpy.linalg import norm
from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer
import spacy

nlp = spacy.load("nl_core_news_sm")


def get_pos(word):
    doc = nlp(word)
    assert len([t for t in doc]) == 1  # check there is ony one token
    return doc[0].pos_


class EmbeddingModel:
    def __init__(self, n_sentences: int | None, verbose=False):
        self.n_sentences = n_sentences + 1  # plus one as we also want the current
        self.verbose = verbose

    def similarity(self, w1: np.ndarray, w2: np.ndarray, measure: str):
        """Similarity between embedding of w1 and w2"""
        if measure == "cosine":
            return np.dot(w1, w2) / (norm(w1) * norm(w2))
        if measure == "pearson":
            return np.corrcoef(w1, w2)
        if measure == "euclidian":
            return 1 - norm(w1 - w2)

    def get_n_sentences(self, text: str):
        """Returns n_sentences from the text."""
        sentences = text.split(".")
        return ".".join(sentences[-(self.n_sentences) :]).lstrip(" ")

    def semantic_association_context(
        self,
        word_emb: np.ndarray,
        context_emb: np.ndarray,
        similarity_measure: str = "cosine",
    ):
        """
        Calculates semantic association of a word to a context embedding
        Args:
            word_emb: word embedding that the semantic association will be calculated for
            context_emb: context embedding the word should be compared to
            similarity_meassure: what measure of similiarity is used
        """
        # make sure the word embedding and context embedding is of the same length
        assert len(word_emb) == len(context_emb)

        semantic_association = self.similarity(
            context_emb, word_emb, measure=similarity_measure
        )
        return semantic_association
