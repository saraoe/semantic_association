"""
Extract ERPs (N400 and P600) from preprocessed EEG from DERCo
"""

from pathlib import Path
import sys
import mne

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    sys.path.insert(0, str(project_root))

from src.append_to_csv import append_df_to_csv


def calc_erp_per_epoch(epoch, channels, tmin, tmax):
    epochs_erp = epoch.copy().crop(tmin=tmin, tmax=tmax)
    epochs_erp.pick_channels(channels)
    data = epochs_erp.get_data()  # in Volts
    erp_per_epoch = data.mean(axis=2).mean(axis=1) * 1e6  # convert to µV
    return erp_per_epoch


def extract_erps(data_folder: Path):
    """
    Extract N400 and P600 from preprocessed fif-files from DERCo
    """
    # define channels
    n400_channels = [
        "Cz",
        "Pz",
        "C4",
        "CP6",
        "P4",
        "P3",
        "CP5",
        "C3",
        "P8",
        "P7",
    ]
    p600_channels = [
        "Cz",
        "CP2",
        "Pz",
        "CP1",
        "C4",
        "CP6",
        "P4",
        "P3",
        "CP5",
        "C3",
        "T8",
        "P8",
        "P7",
        "T7",
    ]

    # calculate ERPs
    eeg_folder = data_folder / "preprocessed_eeg"
    for subject_folder in eeg_folder.iterdir():
        subject = subject_folder.parts[-1]
        print("Subject:", subject)
        for article_folder in subject_folder.iterdir():
            epoch = mne.read_epochs(article_folder / "preprocessed_epoch.fif")
            epoch.apply_baseline((-0.2, 0))  # baseline correct

            results = epoch.metadata.copy()  # if you have metadata
            results["n400"] = calc_erp_per_epoch(
                epoch, channels=n400_channels, tmin=0.3, tmax=0.5
            )
            results["p600"] = calc_erp_per_epoch(
                epoch, channels=p600_channels, tmin=0.5, tmax=0.7
            )

            append_df_to_csv(
                results,
                Path(data_folder, "mean_amplitude.csv"),
                extra_cols={"subject": subject, "article": article_folder.parts[-1]},
            )


if __name__ == "__main__":
    data_folder = Path("experiment3", "data", "DERCo")
    extract_erps(data_folder)
