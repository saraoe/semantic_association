# Data for experiment 2

```
├── README.md   
├── Tanner
│   ├── behavioral
|   │   └── ...                     <- behavioral results
│   ├── eeg
|   │   └── ...                     <- raw EEG (only SPR)
│   ├── mean_amplitude.csv          <- ERPs extracted from epochs
│   └── stim.csv                    <- stimuli (target words and context)
├── UCL
│   ├── EEG*.mat                    <- raw EEG files
│   ├── stimuli_erp.mat             <- preprocessed ERPs
│   ├── README.txt                  <- Original readme file
│   ├── mean_amplitude.csv          <- ERPs extracted from epochs
│   └── stim.csv                    <- stimuli (target words and context)
├── Stone
│   ├── prepro_eeg
|   │   └── ...                     <- preprocessed EEG
│   ├── experimental_stimuli.tsv    <- Original stimuli file from the OSF repo
│   ├── mean_amplitude.csv          <- ERPs extracted from epochs
│   └── stim.csv                    <- stimuli (incl. target words and context)
├── RaCCooNS
│   ├── N400.tsv                    <- Original stimuli file from the OSF repo
│   ├── words.tsv                   <- Original stimuli file from the OSF repo
│   ├── mean_amplitude.csv          <- ERPs extracted from epochs
│   └── stim.csv                    <- stimuli (incl. target words and context)

```

## Tanner

The data in the folder ``Tanner/`` is from the paper "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach" [1] and can be downloaded [here](https://dataverse.harvard.edu/dataverse/AgreementIndiff). The two subfolders, ``behavioral`` [2] and ``eeg`` [3], contains the behavioral results for all participants and the EEG signal only in the SPR condition respectively. The file ``Stimuli.xlsx`` [4] is from the public data repository and contains information on the stimuli. The file ``stim.csv`` is created from the behavioral signal (see ``src/prepare_stimuli_tanner.r``) and contains all stimuli from the SPR condition.

## UCL

The data in the folder ``UCL/`` is the EEG data from the UCL corpus by Frank et al. [5]. Our analysis relies on the already preprocessed EEG in the file ``stimuli_erp.mat``. The data was downloaded from Frank's [website](https://cls.ru.nl/~sfrank/publications.html).  

## Stone

The data in the folder ``Stone/`` is from the paper "Understanding the Effects of Constraint and Predictability in ERP" [6]. The preprocessed EEG data in the folder ``prepro_eeg/`` was downloaded from zenodo [here](https://zenodo.org/records/7334782) [7]. The stimuli file is downloaded from the OSF repository [here](https://osf.io/fndk5/files/osfstorage).

## RaCCooNS

The data in the folder ``RaCCooNS/`` is data from the Radboud Coregistration Corpus of Narrative Sentences (RaCCooNS) [8]. The files ``N400.tsv`` and ``words.tsv`` were downloaded from the online data repository [here](https://doi.org/10.34973/3g69-ha39) [9]. The files contain the preprocessed N400 and the words for the linguistic stimuli.  


## References

[1] Tanner, D. (2019). Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach. Cortex, 111, 210–237. https://doi.org/10.1016/j.cortex.2018.10.011

[2] Tanner, Darren, 2018, "Raw behavioral data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/LHKN5R, Harvard Dataverse, V1, UNF:6:06PXKca/O6XuIPsvxnqtAw== [fileUNF] 

[3] Tanner, Darren, 2019, "Raw EEG data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/K5EDB4, Harvard Dataverse, V1  

[4] Tanner, Darren, 2018, "General files for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/DKEKBH, Harvard Dataverse, V2, UNF:6:kR65EZcASvphkjPneR7xqA== [fileUNF]

[5] Frank, S. L., Otten, L. J., Galli, G., & Vigliocco, G. (2015). The ERP response to the amount of information conveyed by words in sentences. Brain and Language, 140, 1–11. https://doi.org/10.1016/j.bandl.2014.10.006

[6] Kate Stone, Bruno Nicenboim, Shravan Vasishth, Frank Rösler; Understanding the Effects of Constraint and Predictability in ERP. Neurobiology of Language 2023; 4 (2): 221–256. doi: https://doi.org/10.1162/nol_a_00094

[7] Stone, K., Nicenboim, B., Vasishth, S., & Rösler, F. (2022). Preprocessed EEG data for the experiment reported in "Understanding the effects of constraint and predictability in ERP" (Version 2) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.7334782

[8] Frank, S. L., & Aumeistere, A. (2024). An eye-tracking-with-EEG coregistration corpus of narrative sentences. Language Resources and Evaluation, 58(2), 641–657. https://doi.org/10.1007/s10579-023-09684-x

[9] Frank, S.L., Aumeistere, A. (2022): EEG+ET sentence reading. Version 1. Radboud University. (dataset). https://doi.org/10.34973/3g69-ha39

