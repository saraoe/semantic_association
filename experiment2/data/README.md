# Data for experiment 2

```
├── README.md   
├── Tanner
│   ├── behavioral
|   │   └── ...             <- behavioral results
│   ├── eeg
|   │   └── ...             <- raw EEG (only SPR)
│   ├── mean_amplitude      <- ERPs extracted from epochs
│   └── stim.csv            <- stimuli (target words and context)
├── UCL
│   ├── EEG*.mat            <- raw EEG files
│   ├── stimuli_erp.mat     <- preprocessed ERPs
│   ├── README.txt          <- Original readme file
│   ├── mean_amplitude      <- ERPs extracted from epochs
│   └── stim.csv            <- stimuli (target words and context)
├── DERCo
│   ├── preprocessed_eeg
|   │   └── ...             <- Preprocessed EEG from OSF data repo
│   ├── articles
|   │   └── ...             <- Raw articles
│   ├── mean_amplitude      <- ERPs extracted from epochs
|   └── stim.csv            <- stimuli (target words and context)

```

## Tanner

The data in the folder ``Tanner`` is from the paper "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach" [1] and can be downloaded [here](https://dataverse.harvard.edu/dataverse/AgreementIndiff). The two subfolders, ``behavioral`` [2] and ``eeg`` [3], contains the behavioral results for all participants and the EEG signal only in the SPR condition respectively. The file ``Stimuli.xlsx`` [4] is from the public data repository and contains information on the stimuli. The file ``stim.csv`` is created from the behavioral signal (see ``src/prepare_stimuli_tanner.r``) and contains all stimuli from the SPR condition.

## UCL

The data in the folder ``UCL`` is from the EEG data from the UCL corpus by Frank et al. [5]. Our analysis relies on the already preprocessed EEG in the file ``stimuli_erp.mat``. The data was downloaded from Frank's [website](https://cls.ru.nl/~sfrank/publications.html).  


## DERCo

The data in the folder ``DERCo`` is from the Dublin EEG-based Reading Experiment Corpus (DERCo) [6], which can be downloaded [here](https://doi.org/10.17605/OSF.IO/RKQBU) [7]. The files are the preprocessed EEG files, ordered in the folder structure ``preprocessed_eeg/[subject]/article_[x]/preprocessed_epoch.fif``, where the article is the five fairytales that the participants in the corpus have read.

To obtain capitalization and punctuation of the articles (as the words in the meta data did not include this), the five fairytales were downloaded from the supplementary materials [5] and put in txt-files in the ``articles/`` folder.

## References

[1] Tanner, D. (2019). Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach. Cortex, 111, 210–237. https://doi.org/10.1016/j.cortex.2018.10.011

[2] Tanner, Darren, 2018, "Raw behavioral data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/LHKN5R, Harvard Dataverse, V1, UNF:6:06PXKca/O6XuIPsvxnqtAw== [fileUNF] 

[3] Tanner, Darren, 2019, "Raw EEG data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/K5EDB4, Harvard Dataverse, V1  

[4] Tanner, Darren, 2018, "General files for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/DKEKBH, Harvard Dataverse, V2, UNF:6:kR65EZcASvphkjPneR7xqA== [fileUNF]

[5] Frank, S. L., Otten, L. J., Galli, G., & Vigliocco, G. (2015). The ERP response to the amount of information conveyed by words in sentences. Brain and Language, 140, 1–11. https://doi.org/10.1016/j.bandl.2014.10.006

[6] Quach, B. M., Gurrin, C., & Healy, G. (2024). DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. Scientific Data, 11(1), 1104. https://doi.org/10.1038/s41597-024-03915-8

[7] Quach, B. M. (2024). DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. OSF https://doi.org/10.17605/OSF.IO/RKQBU

