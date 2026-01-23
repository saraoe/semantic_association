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
    df: pd.DataFrame, model: EmbeddingModel, model_name: str
):
    id_cols = [
        "document_id",
        "paragraph_n",
        "word_n",
        "number_word",
        "word",
        "story_name",
    ]
    sem_col = f"semantic_association_{model_name}"
    output_dict = {col: [] for col in id_cols + [sem_col]}
    for doc_id, doc_df in df.groupby("document_id"):
        print(f"Document_id {doc_id}")

        context = ""
        paragraph_number = 0
        for _, row in doc_df.groupby(id_cols):
            assert len(row) == 1

            word = row["word"].iloc[0]
            if not context:
                semantic_association = np.nan
            else:
                semantic_association = model.get_semantic_association(word, context)

            # save output
            output_dict[sem_col].append(float(semantic_association))
            for col in id_cols:
                output_dict[col].append(row[col].iloc[0])

            # update context
            if row["paragraph_n"].iloc[0] > paragraph_number:
                context += f"{word} \n"
                paragraph_number = row["paragraph_n"].iloc[0]
            else:
                context += f"{word} "
    return pd.DataFrame.from_dict(output_dict)


if __name__ == "__main__":
    stim_path = Path("data", "tint_stim.csv")
    df = pd.read_csv(stim_path)
    df = df[df["document_id"] < 10]  # remove practice texts

    semantic_association_df = extract_semantic_association(
        df=df,
        model=SentenceEmbeddingModel("clips/e5-large-trm-nl"),
        model_name="SentenceEmbedding",
    )

    semantic_association_df.to_csv(
        Path("results", "tint_semantic_association.csv"), index=False
    )
