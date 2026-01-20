"""
Calculate semantic association using word embeddings
"""

from pathlib import Path
import numpy as np
import re
from gensim.models import KeyedVectors
import spacy

from embedding_model import EmbeddingModel

nlp = spacy.load("nl_core_news_sm")


def get_pos(text: str):
    doc = nlp(text)
    return [(t, t.pos_) for t in doc]


class WordEmbeddingModel(EmbeddingModel):
    def __init__(self, model_path: Path, n_sentences: int | None = None, verbose=False):
        super().__init__(n_sentences, verbose)

        self.model = KeyedVectors.load_word2vec_format(model_path)

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

    def __init__(self, ..., spacy_model_name="nl_core_news_sm"):
        super().__init__(...)

        self.spacy_nlp =  spacy.load(spacy_model_name)
    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        # include only content words
        content_pos = ["NOUN", "VERB", "ADJ", "ADV"]
        pos_text = get_pos(text)
        text_content = [word for (word, pos) in pos_text if pos in content_pos]

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


if __name__ == "__main__":
    # model = WordEmbeddingModel(
    #     model_path=Path("models", "nlwiki_20180420_100d.txt"), verbose=True
    # )
    model = WordEmbeddingModelContentWord(
        model_path=Path("models", "nlwiki_20180420_100d.txt"), verbose=True
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
