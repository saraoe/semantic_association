"""
Calculate semantic association using word embeddings
"""

from pathlib import Path
from functools import cache
import numpy as np
import re
from gensim.models import KeyedVectors
import spacy

from embedding_model import EmbeddingModel


@cache
def get_word_embedding_model(model_path: Path):
    return KeyedVectors.load_word2vec_format(model_path)


class WordEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_path: Path,
        n_sentences: int | None = None,
        verbose: bool = False,
    ):
        super().__init__(n_sentences, verbose)

        self.model = get_word_embedding_model(model_path)

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


class WordEmbeddingModelContentWord(WordEmbeddingModel):
    def __init__(
        self,
        model_path: Path,
        n_sentences: int | None = None,
        spacy_model_name: str = "nl_core_news_sm",
        verbose: bool = False,
    ):
        super().__init__(model_path, n_sentences, verbose)

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


class WordEmbeddingModelWindowed(WordEmbeddingModelContentWord):
    def __init__(
        self,
        model_path: Path,
        n_words: int,
        spacy_model_name: str = "nl_core_news_sm",
        verbose: bool = False,
    ):
        n_sentences = None  # you cannot specify number of sentences with this model
        super().__init__(model_path, n_sentences, spacy_model_name, verbose)

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


if __name__ == "__main__":
    # model = WordEmbeddingModel(
    #     model_path=Path("models", "nlwiki_20180420_100d.txt"), verbose=True
    # )
    # model = WordEmbeddingModelContentWord(
    #     model_path=Path("models", "nlwiki_20180420_100d.txt"), verbose=True
    # )
    model = WordEmbeddingModelWindowed(
        model_path=Path("models", "nlwiki_20180420_100d.txt"), n_words=2, verbose=True
    )

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
