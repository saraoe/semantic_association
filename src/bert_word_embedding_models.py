"""
Calculate semantic association using BERT word embeddings
"""

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
import sys
from pathlib import Path
import numpy as np

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel


class ContextualizedBERTWordEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_sentences: int | None = None,
        verbose: bool = False,
    ):
        super().__init__(n_sentences, verbose)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(model_name)
        self.model_name = model_name

    def get_embedding(self, text: str):
        """Get embedding for any amount of words. If there is more than one word, the function returns the average"""
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)

        # extract layer hidden states
        last_hidden_state = outputs.hidden_states[-1]
        # get the embeddings for the tokens (except first and last)
        token_embeddings = last_hidden_state[0, 1:-1, :]

        return token_embeddings.mean(axis=0)


if __name__ == "__main__":
    models = [
        (
            "contextualized_bert_word_embedding",
            ContextualizedBERTWordEmbeddingModel(
                model_name="FacebookAI/xlm-roberta-large"
            ),
        )
    ]

    # Context from Aurnhammer et al., 2023
    context = """A tourist wanted to take his huge suitcase onto the airplane. The suitcase was however so heavy that the woman at the check-in decided to charge the tourist an extra fee. After that, the tourist opened his suitcase and threw several things out. Now, the suitcase of the ingenious tourist weighed less than the maximum of 30 kilograms"""
    continuations = ["tourist", "suitcase", "bird", "bread"]

    for name, model in models:
        print(name)
        for continuation in continuations:
            sem_association = model.get_semantic_association(
                word=continuation, context=context
            )
            print(
                f"Semantic association of the word '{continuation}' is {sem_association}"
            )
