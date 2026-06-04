"""
Calculate semantic association using embeddings from Mamba
"""

from transformers import MambaForCausalLM, AutoTokenizer
import torch
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel


class MambaEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str,
        n_sentences: int | None = None,
        verbose: bool = False,
    ):
        super().__init__(n_sentences, verbose)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = MambaForCausalLM.from_pretrained(model_name)
        self.model_name = model_name

    def get_embedding(self, text: str):
        """get embeddings from last layer of the state space"""
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs, use_cache=True)
        last_layer_state = outputs.cache_params.ssm_states[-1]
        return last_layer_state.flatten()

    # def get_semantic_association(
    #     self,
    #     word: str,
    #     context: str,
    #     similarity_measure: str = "cosine",
    # ):
    #     """
    #     Calculates semantic association between a word and a context
    #     Args:

    #         word: word that the semantic association will be calculated for.
    #         context: context the word should be compared to.
    #         similarity_measure: what measure of similarity is used.
    #     """
    #     word_emb = self.get_embedding(f"{context} {word}")
    #     context_emb = self.get_embedding(context)

    #     assert len(word_emb) == len(context_emb)

    #     semantic_association = self.similarity(
    #         context_emb, word_emb, measure=similarity_measure
    #     )
    #     return semantic_association


if __name__ == "__main__":
    models = [
        (
            "contextualized_bert_word_embedding",
            MambaEmbeddingModel(model_name="state-spaces/mamba-130m-hf"),
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
