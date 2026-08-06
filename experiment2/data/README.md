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


## References

[1] Tanner, D. (2019). Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach. Cortex, 111, 210–237. https://doi.org/10.1016/j.cortex.2018.10.011

[2] Tanner, Darren, 2018, "Raw behavioral data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/LHKN5R, Harvard Dataverse, V1, UNF:6:06PXKca/O6XuIPsvxnqtAw== [fileUNF] 

[3] Tanner, Darren, 2019, "Raw EEG data for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/K5EDB4, Harvard Dataverse, V1  

[4] Tanner, Darren, 2018, "General files for "Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach"", https://doi.org/10.7910/DVN/DKEKBH, Harvard Dataverse, V2, UNF:6:kR65EZcASvphkjPneR7xqA== [fileUNF]

[5] Frank, S. L., Otten, L. J., Galli, G., & Vigliocco, G. (2015). The ERP response to the amount of information conveyed by words in sentences. Brain and Language, 140, 1–11. https://doi.org/10.1016/j.bandl.2014.10.006

