"""
Calculate semantic association using embeddings
"""

import numpy as np
import re
from numpy.linalg import norm


class EmbeddingModel:
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


if __name__ == "__main__":
    model = EmbeddingModel(n_sentences=2, verbose=True)

    # Context from Aurnhammer et al., 2023 (translated to Dutch)
    context = """Een toerist wilde zijn enorme koffer meenemen in het vliegtuig. 
    De koffer was echter zo zwaar dat de vrouw bij de incheckbalie besloot de toerist een toeslag te vragen. 
    Vervolgens opende de toerist zijn koffer en gooide er verschillende dingen uit. 
    De koffer van de vindingrijke toerist woog nu minder dan de maximale 30 kilo. Toen afwijzen de vrouw de"""

    context = re.sub("    ", "", context)
    print(model.get_n_sentences(context))
