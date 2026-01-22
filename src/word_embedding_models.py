"""
Calculate semantic association using word embeddings
"""

from pathlib import Path
from functools import cache
import numpy as np
import re
from gensim.models import KeyedVectors
import spacy

from src.embedding_model import EmbeddingModel


@cache
def get_word_embedding_model(model_path: Path):
    return KeyedVectors.load_word2vec_format(model_path)


class WordEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        model_path: Path = Path("models"),
        n_sentences: int | None = None,
        verbose: bool = False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = get_word_embedding_model(model_path / f"{model_name}.txt")
        self.model_name = model_name

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        if self.n_sentences:
            text = self.get_n_sentences(text)

        # split text on whitespace, make lower, and remove punctuation
        text_list = text.lower().split(" ")
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        context_embeddings = [
            self.model[word] if word in self.model else np.nan for word in text_list
        ]

        # remove None values
        context_embeddings = [emb for emb in context_embeddings if emb is not np.nan]
        if len(context_embeddings) == 0:
            return np.nan

        return np.mean(context_embeddings, axis=0)


class WordEmbeddingModelContentWord(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        model_path: Path = Path("models"),
        n_sentences: int | None = None,
        spacy_model_name: str = "nl_core_news_sm",
        verbose: bool = False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = get_word_embedding_model(model_path / f"{model_name}.txt")
        self.model_name = model_name
        self.content_pos = ["NOUN", "VERB", "ADJ", "ADV"]
        self.spacy_nlp = spacy.load(spacy_model_name)

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

        context_embeddings = [
            self.model[word] if word in self.model else np.nan for word in text_list
        ]

        # remove None values
        context_embeddings = [emb for emb in context_embeddings if emb is not np.nan]
        if len(context_embeddings) == 0:
            return np.nan

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
        if word in self.model:
            word_emb = self.model[word]
        else:
            return np.nan
        context_emb = self.get_embedding(context)
        if word_emb is np.nan or context_emb is np.nan:
            return np.nan

        assert len(word_emb) == len(context_emb)

        semantic_association = self.similarity(
            context_emb, word_emb, measure=similarity_measure
        )
        return semantic_association


class WordEmbeddingModelWindowed(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_words: int,
        model_path: Path = Path("models"),
        spacy_model_name: str = "nl_core_news_sm",
        verbose: bool = False,
    ):
        n_sentences = None  # you cannot specify number of sentences with this model
        super().__init__(n_sentences, verbose)

        self.model = get_word_embedding_model(model_path / f"{model_name}.txt")
        self.model_name = model_name
        self.content_pos = ["NOUN", "VERB", "ADJ", "ADV"]
        self.spacy_nlp = spacy.load(spacy_model_name)
        self.n_words = n_words

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        # include only content words
        text_content = [
            token.text
            for token in self.spacy_nlp(text)
            if token.pos_ in self.content_pos
        ]

        # make lower, and remove punctuation
        text_list = [str(w).lower() for w in text_content]
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        # include only n_words
        text_list = text_list[-self.n_words :]

        context_embeddings = [
            self.model[word] if word in self.model else np.nan for word in text_list
        ]

        # remove None values
        context_embeddings = [emb for emb in context_embeddings if emb is not np.nan]
        if len(context_embeddings) == 0:
            return np.nan

        return np.mean(context_embeddings, axis=0)


class WordEmbeddingModelWeighted(EmbeddingModel):
    def __init__(
        self, model_name, model_path=Path("models"), n_sentences=None, verbose=False
    ):
        super().__init__(n_sentences, verbose)

        self.model = get_word_embedding_model(model_path / f"{model_name}.txt")
        self.model_name = model_name
        self.half_life = 4

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns a list of embedding"""
        if self.n_sentences:
            text = self.get_n_sentences(text)

        # split text on whitespace, make lower, and remove punctuation
        text_list = text.lower().split(" ")
        text_list = [re.sub(r"\W+", "", w) for w in text_list]

        context_embeddings = [
            self.model[word] if word in self.model else np.nan for word in text_list
        ]

        if len(context_embeddings) == 1:  # if its just the embedding of one word
            return context_embeddings[0]
        return context_embeddings

    def weighted_association(
        self,
        weights: np.ndarray,
        context_embeddings: list[np.ndarray],
        word_emb: np.ndarray,
        similarity_measure: str,
    ):
        for weight, context_emb in zip(weights, context_embeddings):
            if context_emb is np.nan:
                continue
            yield weight * self.similarity(
                word_emb, context_emb, measure=similarity_measure
            )

    def get_semantic_association(
        self,
        word: str,
        context: str,
        similarity_measure: str = "cosine",
    ):
        """
        Calculates semantic association between a word and a context
        Args:
            word_emb: word embedding that the semantic association will be calculated for
            context_emb: context embedding the word should be compared to
            similarity_meassure: what measure of similiarity is used
        """
        word_emb = self.get_embedding(word)
        if word_emb is np.nan:
            return np.nan
        context_embeddings = self.get_embedding(context)
        assert all(
            [
                len(word_emb) == len(context_emb)
                for context_emb in context_embeddings
                if context_emb is not np.nan
            ]
        )

        # calculate weights based on word distances
        distances = np.arange(start=len(context_embeddings), stop=0, step=-1)
        weights = 2 ** (-distances / self.half_life)

        weighted_associations = list(
            self.weighted_association(
                weights, context_embeddings, word_emb, similarity_measure
            )
        )
        if not weighted_associations:
            return np.nan

        return np.sum(weighted_associations, axis=0)


if __name__ == "__main__":
    model_name = "nlwiki_20180420_100d"
    models = [
        ("word_embedding", WordEmbeddingModel(model_name=model_name, verbose=True)),
        (
            "content_words_only",
            WordEmbeddingModelContentWord(model_name=model_name, verbose=True),
        ),
        (
            "windowed",
            WordEmbeddingModelWindowed(
                model_name=model_name,
                n_words=2,
                verbose=True,
            ),
        ),
        ("weighted", WordEmbeddingModelWeighted(model_name=model_name, verbose=True)),
    ]

    # Context from Aurnhammer et al., 2023 (translated to Dutch)
    context = """Een toerist wilde zijn enorme koffer meenemen in het vliegtuig. 
    De koffer was echter zo zwaar dat de vrouw bij de incheckbalie besloot de toerist een toeslag te vragen. 
    Vervolgens opende de toerist zijn koffer en gooide er verschillende dingen uit. 
    De koffer van de vindingrijke toerist woog nu minder dan de maximale 30 kilo. Toen afwijzen de vrouw de"""
    continuations = ["toerist", "koffer", "vogel", "brood"]

    context = re.sub("\n    ", "", context)
    for name, model in models:
        print(name)
        for continuation in continuations:
            sem_association = model.get_semantic_association(
                word=continuation, context=context
            )
            print(
                f"Semantic association of the word '{continuation}' is {sem_association}"
            )
