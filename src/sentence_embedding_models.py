"""
Calculate semantic association using sentence embeddings
"""

import sys
from pathlib import Path
import re
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
