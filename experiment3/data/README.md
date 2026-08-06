# Data for experiment 3

## DERCo

The data in the folder ``DERCo`` is from the Dublin EEG-based Reading Experiment Corpus (DERCo) [1], which can be downloaded [here](https://doi.org/10.17605/OSF.IO/RKQBU) [2]. The files are the preprocessed EEG files, ordered in the folder structure ``preprocessed_eeg/[subject]/article_[x]/preprocessed_epoch.fif``, where the article is the five fairytales that the participants in the corpus have read.

To obtain capitalization and punctuation of the articles (as the words in the meta data did not include this), the five fairytales were downloaded from the supplementary materials [1] and put in txt-files in the ``articles/`` folder.

## References

[1] Quach, B. M., Gurrin, C., & Healy, G. (2024). DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. Scientific Data, 11(1), 1104. https://doi.org/10.1038/s41597-024-03915-8

[2] Quach, B. M. (2024). DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. OSF https://doi.org/10.17605/OSF.IO/RKQBU