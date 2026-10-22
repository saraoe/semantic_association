# Semantic association

This repository contains code for estimating semantic association using language model (LM) embeddings. The semantic association between a target word and its preceding context is implemented as as the cosine similarity between the embedding of the context, $E_{context}$, and the embedding of the target, $E_{target}$. 
$$
    \text{Semantic Association} = \cos(E_{context}, E_{target})
$$

The embeddings were extracted from a number of embedding models, which fell into two categories: Uncontextualized word embeddings and contextualized sentence embeddings.

## CMCL 26

The folder ``cmcl26/`` contains code for the paper "Modeling semantic association in self-paced reading with language model embeddings"[1] which was presented at The 15th Workshop on Cognitive Modeling and Computational Linguistics (CMCL). The original code for this paper (before additional experiments were run) is in the ``cmcl26`` branch.

## Experiments

The folders ``experiment1``, ``experiment2``, and ``experiment3`` contains the code for the experiments run to validate and explore the embedding-based formalization of additional EEG corpora besides the Tilburg corpus of Natural, Dutch Texts (TiNT) [2-3] used for the CMCL 2026 paper [2].

- ``experiment1`` contains code for extracting and analyzing embedding-based semantic association in semantic illusions. 
- ``experiment2`` contains code for extracting and analyzing embedding-based semantic association in EEG experiments using natural sentences as stimuli.
- ``experiment3`` contains code for extracting and analyzing embedding-based semantic association in EEG experiments with stimuli consisting of natural texts exceeding a few sentences in length.

## Virtual environments

The code to reproduce the results relies on both R and Python. There are two separate virtual environments for the two.

### Python
The dependencies for the Python code is in the file ``requirements.txt``. To install run:
```
pip install -r requirements.txt
```

### R
The dependencies for the R code is in the file ``environment.yml``. To install run:
```
conda env create -f environment.yml
```

Additionally, to install the R package [pangoling](https://github.com/ropensci/pangoling) (which is used to extract word probabilities from LLMs) you need to run:
```
Rscript install_pangoling.r
```

*NB: Do this when the R environment is activated!*


## References
[1] Østergaard, S. M., Enevoldsen, K., Alishahi, A., & Nicenboim, B. (2026). Modeling semantic association in self-paced reading with language model embeddings. Proceedings of the 15th Workshop on Cognitive Modeling and Computational Linguistics. https://doi.org/10.63317/5hz52qgp2gdn

[2] Østergaard, S. M., Lichtenberg, L. D., Boon, L., & Nicenboim, B. (2026). A Corpus of Joint EEG and Self-Paced Reading of Natural Dutch Texts. 11260–11271. https://doi.org/10.63317/49tvxys2q4zc

[3] Østergaard, Sara Møller; Lichtenberg, Lenneke; Boon, Laura; Nicenboim, Bruno, 2026, "EEG and Self-Paced Reading of Natural, Dutch Texts (Towards a computational model of reading (TCMR))", https://doi.org/10.34894/0O5XQ7, DataverseNL