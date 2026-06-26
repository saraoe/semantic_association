# Semantic association

This repository contains code for estimating semantic association using language model (LM) embeddings. 

## CMCL 26

The folder ``cmcl26/`` contains code for the paper "Modeling semantic association in self-paced reading with language model embeddings"[1] which will be presented at The 15th Workshop on Cognitive Modeling and Computational Linguistics (CMCL). The original code for this paper (before additional experiment were run) is in the ``cmcl26`` branch.

## Virtual environments

The code to reproduce the results relies on both R and python. There are two separate virtual environments for the two.

### Python
The dependencies for the python code is in the file ``requirements.txt``. To install run:
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
[1] *reference coming*