"""
Calculate semantic association using embeddings
"""

import numpy as np
from numpy.linalg import norm
from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    def __init__(
        self,
        n_sentences: int | None,
        verbose: bool = False,
    ):
        self.n_sentences = (
            n_sentences + 1 if isinstance(n_sentences, int) else n_sentences
        )  # plus one as we also want the current
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

    @abstractmethod
    def get_embedding(self, text):
        pass

    def get_semantic_association(
        self,
        word: str,
        context: str,
        similarity_measure: str = "cosine",
    ):
        """
        Calculates semantic association between a word and a context
        Args:

            word: word that the semantic association will be calculated for.
            context: context the word should be compared to.
            similarity_meassure: what measure of similiarity is used.
        """
        word_emb = self.get_embedding(word)
        context_emb = self.get_embedding(context)
        if word_emb is np.nan or context_emb is np.nan:
            return np.nan

        assert len(word_emb) == len(context_emb)

        semantic_association = self.similarity(
            context_emb, word_emb, measure=similarity_measure
        )
        return semantic_association
