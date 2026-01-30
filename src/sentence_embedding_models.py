"""
Calculate semantic association using sentence embeddings
"""

import sys
from pathlib import Path
from functools import cache
import re
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel


class SentenceEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_sentences: int | None = None,
        verbose=False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def get_embedding(self, text: str):
        """Get embedding for any amount of words."""
        if self.n_sentences:
            text = self.get_n_sentences(text)
        return self.model.encode(text)


class SentenceEmbeddingModelSingleWord(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_sentences: int | None = None,
        verbose=False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    @cache
    def get_word_embedding(self, word: str):
        """Get embedding for one words."""
        return self.model.encode(word)

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        if self.n_sentences:
            text = self.get_n_sentences(text)

        # split text on whitespace, make lower, and remove punctuation
        text_list = text.lower().split(" ")
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        context_embeddings = [self.get_word_embedding(word) for word in text_list]

        return np.mean(context_embeddings, axis=0)


class SentenceEmbeddingModelSingleWordContentWord(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_sentences: int | None = None,
        spacy_model_name: str = "nl_core_news_sm",
        verbose=False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.content_pos = ["NOUN", "VERB", "ADJ", "ADV"]
        self.spacy_nlp = spacy.load(spacy_model_name)

    @cache
    def get_word_embedding(self, word: str):
        """Get embedding for one words."""
        return self.model.encode(word)

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        if self.n_sentences:
            text = self.get_n_sentences(text)

        # include only content words
        text_content = [
            token.text
            for token in self.spacy_nlp(text)
            if token.pos_ in self.content_pos
        ]

        # make lower, and remove punctuation
        text_list = [str(w).lower() for w in text_content]
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        context_embeddings = [self.get_word_embedding(word) for word in text_list]

        return np.mean(context_embeddings, axis=0)

    def get_semantic_association(
        self,
        word: str,
        context: str,
        similarity_measure: str = "cosine",
    ):
        """
        Calculates semantic association between a word and a context
        Args:

            word_emb: word that the semantic association will be calculated for.
            context_emb: context the word should be compared to.
            similarity_meassure: what measure of similiarity is used.
        """
        # make lower, and remove punctuation
        word = word.lower()
        word = re.sub(r"\W+", "", word)
        word_emb = self.model.encode(word)
        context_emb = self.get_embedding(context)

        assert len(word_emb) == len(context_emb)

        semantic_association = self.similarity(
            context_emb, word_emb, measure=similarity_measure
        )
        return semantic_association


if __name__ == "__main__":
    model = SentenceEmbeddingModel("all-MiniLM-L6-v2")

    # Context from Aurnhammer et al., 2023 (translated to Dutch)
    context = """Een toerist wilde zijn enorme koffer meenemen in het vliegtuig. 
    De koffer was echter zo zwaar dat de vrouw bij de incheckbalie besloot de toerist een toeslag te vragen. 
    Vervolgens opende de toerist zijn koffer en gooide er verschillende dingen uit. 
    De koffer van de vindingrijke toerist woog nu minder dan de maximale 30 kilo. Toen afwijzen de vrouw de"""
    continuations = ["toerist", "koffer", "vogel", "brood"]

    context = re.sub("\n    ", "", context)
    for continuation in continuations:
        sem_association = model.get_semantic_association(
            word=continuation, context=context
        )
        print(f"Semantic association of the word '{continuation}' is {sem_association}")
