"""
Extracting semantic association for the TiNT data (data/tint_stim.csv)
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel
from src.sentence_embedding_models import SentenceEmbeddingModel
from src.word_embedding_models import (
    WordEmbeddingModel,
    WordEmbeddingModelContentWord,
    WordEmbeddingModelWindowed,
    WordEmbeddingModelWeighted,
)


def extract_semantic_association(
    df: pd.DataFrame, model: EmbeddingModel, implementation_name: str
) -> pd.DataFrame:
    """Extract semantic association scores for each word given its context."""
    id_cols = [
        "document_id",
        "paragraph_n",
        "word_n",
        "number_word",
        "word",
        "story_name",
    ]
    association_col = f"semantic_association_{implementation_name}"

    results = []

    for doc_id, doc_df in df.groupby("document_id"):
        print(f"Processing document_id {doc_id}")
        doc_df = doc_df.sort_values(["paragraph_n", "word_n"])

        context = ""
        current_paragraph = 0

        for idx, row in doc_df.iterrows():
            word = row["word"]

            # Compute semantic association (NaN for first word)
            semantic_association = (
                model.get_semantic_association(word, context) if context else np.nan
            )

            # Store result
            result = {col: row[col] for col in id_cols}
            result[association_col] = float(semantic_association)
            results.append(result)

            # Update context
            if row["paragraph_n"] > current_paragraph:
                context += f"{word} \n"
                current_paragraph = row["paragraph_n"]
            else:
                context += f"{word} "

    return pd.DataFrame(results)


if __name__ == "__main__":
    stim_path = Path("data", "tint_stim.csv")
    df = pd.read_csv(stim_path)
    df = df[df["document_id"] < 10]  # remove practice texts

    semantic_association_df = extract_semantic_association(
        df=df,
        model=SentenceEmbeddingModel("clips/e5-large-trm-nl"),
        implementation_name="SentenceEmbedding",
    )

    semantic_association_df.to_csv(
        Path("results", "tint_semantic_association.csv"), index=False
    )
