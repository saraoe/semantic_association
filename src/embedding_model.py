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

    def similarity(self, w1, w2, meassure):
        """Similarity between embedding of w1 and w2"""
        if meassure == "cosine":
            return np.dot(w1, w2) / (norm(w1) * norm(w2))
        if meassure == "pearson":
            return np.corrcoef(w1, w2)
        if meassure == "euclidian":
            return 1 - norm(w1 - w2)

    def semantic_association_context(
        self, word_emb, context_emb, similarity_meassure="cosine"
    ):
        """
        Calculates semantic association of a word to a context embedding
        Args:
            word_emb (np.array): word embedding that the semantic association will be calculated for
            context_emb (np.array): context embedding the word should be compared to
            similarity_meassure (str): what meassure of similiarity is used
        """
        # make sure the word embedding and context embedding is of the same length
        assert len(word_emb) == len(context_emb)

        semantic_association = self.similarity(
            context_emb, word_emb, meassure=similarity_meassure
        )
        return semantic_association


class WordEmbeddingModel(EmbeddingModel):
    def __init__(self, model_path: Path, include_pos: list = [], verbose=False):
        super().__init__(verbose)

        self.model = KeyedVectors.load_word2vec_format(model_path)
        self.include_pos = include_pos

    def update_include_pos(self, include_pos: list):
        self.include_pos = include_pos

    def get_embedding(self, text: str):
        """Get embedding for any amount of words."""
        # split text on whitespace, make lower, and remove punctuation
        text_list = text.lower().split(" ")
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        # get either word embedding (if text is a word) or context embedding (if text is multiple words)
        if len(text_list) == 1:
            return self.get_word_embedding(text_list[0])
        else:
            return self.get_context_embedding(text_list)

    def get_word_embedding(self, word):
        try:
            return self.model[word]
        except KeyError:
            if self.verbose:
                print(f"{word} not in model!")
            return np.nan

    def get_context_embedding(self, context: list):
        """
        Calculates semantic association of a word to a context embedding
        Args:
            context (List[str]): words in the context
        """
        if self.include_pos:
            # if only certain pos tags should be included in the embedding
            context = [w for w in context if get_pos(w) in self.include_pos]

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
