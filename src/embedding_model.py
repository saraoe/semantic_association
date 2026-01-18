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
    def __init__(self, verbose=False):
        self.verbose = verbose

    def similarity(self, w1: np.ndarray, w2: np.ndarray, measure: str):
        """Similarity between embedding of w1 and w2"""
        if measure == "cosine":
            return np.dot(w1, w2) / (norm(w1) * norm(w2))
        if measure == "pearson":
            return np.corrcoef(w1, w2)
        if measure == "euclidian":
            return 1 - norm(w1 - w2)

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


class WordEmbeddingModel(EmbeddingModel):
    def __init__(self, model_path: Path, verbose=False):
        super().__init__(verbose)

        self.model = KeyedVectors.load_word2vec_format(model_path)

    def get_word_embedding(self, word):
        # self.model.get(word, np.nan) -> maybe move to function below
        try:
            return self.model[word]
        except KeyError:
            if self.verbose:
                print(f"{word} not in model!")
            return np.nan

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        # split text on whitespace, make lower, and remove punctuation
        text_list = text.lower().split(" ")
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        context_embeddings = [self.get_word_embedding(w) for w in context]

        # remove None values
        context_embeddings = [emb for emb in context_embeddings if emb is not np.nan]
        if len(context_embeddings) == 0:
            return np.nan

        return np.mean(context_embeddings, axis=0)


class SentenceEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name: str, verbose=False):
        super().__init__(verbose)

        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text: str):
        """Get embedding for any amount of words."""
        return self.model.encode(text)


if __name__ == "__main__":
    only_cotent_words = True
    # model = WordEmbeddingModel(
    #     model_path=Path("models", "nlwiki_20180420_100d.txt"), verbose=True
    # )
    model = SentenceEmbeddingModel("all-MiniLM-L6-v2")

    # Context from Aurnhammer et al., 2023 (translated to Dutch)
    context = """Een toerist wilde zijn enorme koffer meenemen in het vliegtuig. 
    De koffer was echter zo zwaar dat de vrouw bij de incheckbalie besloot de toerist een toeslag te vragen. 
    Vervolgens opende de toerist zijn koffer en gooide er verschillende dingen uit. 
    De koffer van de vindingrijke toerist woog nu minder dan de maximale 30 kilo. Toen afwijzen de vrouw de"""
    continuations = ["toerist", "koffer", "vogel", "brood"]

    context = re.sub("\n    ", "", context)
    context_emb = model.get_embedding(context)
    for continuation in continuations:
        word_emb = model.get_embedding(continuation)
        sem_association = model.semantic_association_context(
            word_emb=word_emb, context_emb=context_emb
        )
        print(f"Semantic association of the word '{continuation}' is {sem_association}")
