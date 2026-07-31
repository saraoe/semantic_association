"""
Create df to plot words similar to the context embedding
NB: Must run context_embedding.py first!
"""

import ndjson
from pathlib import Path
import pandas as pd
from heapq import nlargest, nsmallest


def ndjson_gen(json_path: Path):
    with open(json_path) as f:
        reader = ndjson.reader(f)
        yield from reader


def print_similar_words(words_path: Path, n: int):
    for row in ndjson_gen(words_path):
        print(f"Model = {row['implementation']}:{row['model']}")
        for context_row in row["similarity_words"]:
            if context_row["word_n"] % 100 != 0:
                continue
            # print(context_row["context"])
            print("word_n =", context_row["word_n"])
            if "high" in context_row:
                n_most_similar = context_row["high"][:n]
                n_least_similar = context_row["low"][:n]
            else:
                n_most_similar = nlargest(n, context_row["all"], lambda x: x[1])
                n_least_similar = nsmallest(n, context_row["all"], lambda x: x[1])
            print(f"Most similar: {[w for w in n_most_similar]}")
            print(f"Least similar: {[w for w in n_least_similar]}")
            print("\n")
        print("--------")


def create_top_n_df(words_path: Path, out_path: Path, n: int):
    """
    creating csv with top_n most/least similar words to the context
    """
    cols = [
        "model",
        "implementation",
        "id",
        "word_n",
        "context",
        "word",
        "cosine_similarity",
        "similarity_level",
    ]
    df_data = {col: [] for col in cols}
    for row in ndjson_gen(words_path):
        for context_row in row["similarity_words"]:
            # columns from general row
            for col in ["model", "implementation"]:
                df_data[col] += [row[col]] * (n * 2)
            # columns for context_row
            for col in ["id", "word_n", "context"]:
                df_data[col] += [context_row[col]] * (n * 2)

            if "high" in context_row:
                n_most_similar = context_row["high"][:n]
                n_least_similar = context_row["low"][:n]
            else:
                n_most_similar = nlargest(n, context_row["all"], lambda x: x[1])
                n_least_similar = nsmallest(n, context_row["all"], lambda x: x[1])

            for word, similarity in n_most_similar:
                df_data["word"].append(word)
                df_data["cosine_similarity"].append(similarity)
                df_data["similarity_level"].append("high")
            for word, similarity in n_least_similar:
                df_data["word"].append(word)
                df_data["cosine_similarity"].append(similarity)
                df_data["similarity_level"].append("low")

    df = pd.DataFrame(df_data)
    df.to_csv(out_path)


def create_word_similarity_df(words_path: Path, out_path: Path):
    """
    creating csv with similarity of specific words to the context
    """
    # word list
    word_list = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [  # words related to story
            "wolf",
            "fox",
            "lambs",
            "sheep",
            "farmer",
            "pancakes",
            "meat",
            "cellar",
            "wood",
            "hole",
            "tub",
            "cudgel",
            "greed",
            "food",
            "danger",
            "eat",
            "hungry",
            "kill",
            "greedy",
            "threaten",
            "fetch",
            "steal",
            "attack",
            # word related to the three food topics (lamb, pancakes, meat)
            "shepherd",
            "wool",
            "waffle",
            "bakery",
            "butcher",
            "steak",
        ],
    }
    cols = [
        "model",
        "implementation",
        "id",
        "word_n",
        "context",
        "word",
        "cosine_similarity",
    ]
    df_data = {col: [] for col in cols}
    for row in ndjson_gen(words_path):
        for context_row in row["similarity_words"]:
            # get the words from the specific document id
            doc_id = context_row["id"]
            words_id = word_list[doc_id]

            if "high" in context_row:
                word_sims = context_row["row"]
            else:
                word_sims = context_row["all"]

            n = 0
            for word, similarity in word_sims:
                if word in words_id:
                    n += 1
                    df_data["word"].append(word)
                    df_data["cosine_similarity"].append(similarity)

            # columns from general row
            for col in ["model", "implementation"]:
                df_data[col] += [row[col]] * n
            # columns for context_row
            for col in ["id", "word_n", "context"]:
                df_data[col] += [context_row[col]] * n

    df = pd.DataFrame(df_data)
    df.to_csv(out_path)


if __name__ == "__main__":
    words_path = Path(
        "experiment3", "results", "word_similarity_context_embeddings.ndjson"
    )
    out_path = Path("experiment3", "results", "word_similarity_context_embeddings.csv")
    # print_similar_words(words_path, n=5)
    create_top_n_df(
        words_path=words_path,
        n=5,
        out_path=Path(
            "experiment3", "results", "top_n_context_embedding_similarities.csv"
        ),
    )
    create_word_similarity_df(
        words_path=words_path,
        out_path=Path(
            "experiment3", "results", "words_context_embedding_similarities.csv"
        ),
    )
