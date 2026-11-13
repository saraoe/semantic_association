"""
Calculate semantic association by prompting an LLM
"""

from abc import ABC, abstractmethod
from openai import OpenAI
import math


class LLMPrompting(ABC):
    def __init__(self, association_prompt: str | None = None):
        if not association_prompt:
            self.prompt = "Semantic association is a measure of how semantically associated or semantic related a context and a word is. For example, the words 'egg' and 'breakfast' are very semantically associated, and similarly are the context 'For breakfast the eggs would' and the word 'eat' semantically associated. Please indicate how semantically associated you think the following pair of context and word are on a scale from 1 (completely unassociated) to 7 (strongly associated). Only answer a number from 1 to 7. Please limit your answer to numbers."
        else:
            self.prompt = association_prompt

    @abstractmethod
    def get_probabilities(self, prompt: str):
        pass

    def get_semantic_association(
        self, word: str, context: str, method: str = "weighted_mean"
    ):
        """
        Calculates semantic association between a word and a context
        Args:

            word: word that the semantic association will be calculated for.
            context: context the word should be compared to.
            method: methods for extracting semantic association. Either 'weighted_mean' (default) or 'most_likely'. Based on methods described in Brysbaert et al. (2024).
        """
        full_prompt = (
            self.prompt
            + f"\n\nThe context is: '{context}'"
            + f"\nThe word is: '{word}'"
            + "\n\nRating: "
        )

        probs = self.get_probabilities(full_prompt)

        if method == "most_likely":
            return max(probs, key=probs.get)
        if method == "weighted_mean":
            return sum(k * p for k, p in probs.items())


class OpenAIModel(LLMPrompting):
    def __init__(
        self,
        api_key: str,
        model_name: str,
        association_prompt=None,
    ):
        super().__init__(association_prompt)
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def get_probabilities(self, prompt: str):
        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
            temperature=0,
            top_logprobs=10,
            include=["message.output_text.logprobs"],
        )

        first_token = response.output[0].content[0].logprobs[0]

        probs = {}
        for alt in first_token.top_logprobs:
            tok = alt.token.strip()
            if tok in {"1", "2", "3", "4", "5", "6", "7"}:
                probs[int(tok)] = probs.get(int(tok), 0) + math.exp(alt.logprob)
        return probs


if __name__ == "__main__":
    # you might need to run unset SSL_CERT_FILE in the terminal before this script!
    with open("openai_api_key.txt") as f:
        api_key = f.read()

    model = OpenAIModel(
        api_key=api_key,
        model_name="gpt-4.1",
    )

    # Context from Aurnhammer et al., 2023
    context = """A tourist wanted to take his huge suitcase onto the airplane. The suitcase was however so heavy that the woman at the check-in decided to charge the tourist an extra fee. After that, the tourist opened his suitcase and threw several things out. Now, the suitcase of the ingenious tourist weighed less than the maximum of 30 kilograms"""
    continuations = ["tourist", "suitcase", "bird", "bread"]

    for continuation in continuations:
        sem_association = model.get_semantic_association(
            word=continuation, context=context
        )
        print(f"Semantic association of the word '{continuation}' is {sem_association}")
