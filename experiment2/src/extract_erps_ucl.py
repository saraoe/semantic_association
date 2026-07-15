"""
Extract ERPs (N400 and P600) from preprocessed EEG from UCL
"""

from pathlib import Path
import scipy.io as sio
import pandas as pd


def extract_erps(data_path: Path, out_path: Path):
    mat = sio.loadmat(data_path / "stimuli_erp.mat", squeeze_me=True)

    # averaged ERPs for all words for all participants
    # shape: (205,) and then every element (word, participant, erp)
    # The six ERPs are: (0) ELAN, (1) LAN, (2) N400, (3) EPNP, (4) P600, (5) PNP.
    erp = mat["ERP"]
    erp_names = ["ELAN", "LAN", "N400", "EPNP", "P600", "PNP"]

    # sentences
    # shape: (205,) and then every element (word,)
    sentences = mat["sentences"]

    # If an artifact was detected and ERP rejected
    # shape: (205,) and then every element (word, participant)
    artifact = mat["artefact"]
    reject = mat["reject"]

    rows = []

    for sentence_id in range(len(sentences)):  # 205 sentences
        words = sentences[sentence_id]
        erp_sent = erp[sentence_id]
        artifact_sent = artifact[sentence_id]
        reject_sent = reject[sentence_id]

        for word_n, word in enumerate(words):
            for subject in range(erp_sent.shape[1]):  # 24 subjects
                row = {
                    "id": sentence_id + 1,
                    "word": word,
                    "word_n": word_n,
                    "subject": subject + 1,
                    "artifact": artifact_sent[word_n, subject],
                    "reject": reject_sent[word_n, subject],
                }

                # Add ERP components
                for k, name in enumerate(erp_names):
                    row[name] = erp_sent[word_n, subject, k]

                rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(out_path / "mean_amplitude.csv")


if __name__ == "__main__":
    extract_erps(
        data_path=Path("experiment2", "data", "UCL"),
        out_path=Path("experiment2", "data", "UCL"),
    )
