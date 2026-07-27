"""
Inspect context embeddings by looking at the words most/least similar
NB: Must run context_embedding.py first!
"""

import ndjson
from pathlib import Path


def ndjson_gen(json_path: Path):
    with open(json_path) as f:
        reader = ndjson.reader(f)
        yield from reader


def print_similar_words(words_path: Path, n: int):
    for row in ndjson_gen(words_path):
        print(f"Model = {row['implementation']}:{row['model']}")
        for context_row in row["similarity_words"]:
            print(context_row["context"])
            n_most_similar = context_row["high"][:n]
            n_least_similar = context_row["low"][:n]
            print(f"Most similar: {[w for (w, _) in n_most_similar]}")
            print(f"Least similar: {[w for (w, _) in n_least_similar]}")
            print("\n")
        print("--------")


if __name__ == "__main__":
    words_path = Path(
        "experiment3", "results", "word_similarity_context_embeddings.ndjson"
    )
    print_similar_words(words_path, n=5)
