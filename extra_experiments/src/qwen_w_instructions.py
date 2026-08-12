"""
Extract semantic association from DERCo using Qwen-Embedding-8B with instructions
"""

from pathlib import Path
import sys
import pandas as pd
from functools import cache


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from src.embedding_model import EmbeddingModel
from src.sentence_embedding_models import SentenceEmbeddingModel
from src.append_to_csv import append_df_to_csv


def extract_semantic_association(
    model: EmbeddingModel,
    implementation_name: str,
    df: pd.DataFrame,
    out_path: Path,
    instructions: dict,
):
    """
    Extracts semantic association for targets in df using the embedding model

    Args:
        model: Embedding model used to extract semantic association.
        implementation_name: Name of the implementation (e.g., SE or WE)
        df: dataframe with targets and contexts (as two columns by that name in the df).
        out_path: path for where to save df.
        instructions: dictionary with instruction for target and context
    """
    assert all([(col in df.columns) for col in ["target", "context"]])

    @cache
    def get_association(context, target, target_inst, context_inst):
        if pd.isna(context):
            return None
        target_w_inst = f"{target_inst} {target}"
        context_w_inst = f"{context_inst} {context}"
        return model.get_semantic_association(
            word=target_w_inst, context=context_w_inst
        )

    df["semantic_association"] = df.apply(
        lambda row: get_association(
            row["context"],
            row["target"],
            target_inst=instructions["target"],
            context_inst=instructions["context"],
        ),
        axis=1,
    )
    # save output
    append_df_to_csv(
        df,
        path=out_path,
        extra_cols={
            "implementation": implementation_name,
            "model": model.model_name,
            "target_instructions": instructions["target"],
            "context_instructions": instructions["context"],
        },
    )


if __name__ == "__main__":
    instructions = {
        "target": "The semantic meaning of this word:",
        "context": "The semantic meaning of this text:",
    }
    corpora = [
        {
            "name": "derco",
            "df": pd.read_csv(
                Path("experiment3", "data", "DERCo", "stim.csv"), index_col=0
            ),
            "out_path": Path(
                "extra_experiments",
                "results",
                "qwen_instructions_semantic_association.csv",
            ),
        },
    ]

    models = ["Qwen/Qwen3-Embedding-0.6B", "Qwen/Qwen3-Embedding-8B"]

    for model_name in models:
        print("Read model")
        model = SentenceEmbeddingModel(model_name)

        print("Extracting semantic association")
        for corpus in corpora:
            extract_semantic_association(
                df=corpus["df"],
                implementation_name="SE_all",
                model=model,
                out_path=corpus["out_path"],
                instructions=instructions,
            )
        del model
