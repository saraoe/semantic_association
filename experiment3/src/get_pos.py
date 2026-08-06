import pandas as pd
import sys
from pathlib import Path
import spacy
from spacy.symbols import ORTH

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from experiment2.src.get_pos import add_pos_to_stim


if __name__ == "__main__":
    data_path = Path("experiment3", "data")

    datasets = [("DERCo", ["article_n"])]

    for dataset_folder, ids in datasets:
        add_pos_to_stim(stim_path=data_path / dataset_folder / "stim.csv", id_cols=ids)
