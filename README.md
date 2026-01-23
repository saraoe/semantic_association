# Semantic association

## Validate semantic association
All the implementations of semantic association (see ``src/word_embedding_models.py`` and ``src/sentence_embedding_models.py``) were validated using the data from [Federmeier & Kutas  (1999)](https://doi.org/10.1006/jmla.1999.2660). Below you can see what models were validated and on which language (Dutch and/or English).

| Model Name                           | Model type           | Language | 
| ------------------------------------ | -------------------- | -------- | 
| enwiki_20180420_100d                 | word embedding       | en       | 
| word2vec-google-news-300             | word embedding       | en       | 
| all-MiniLM-L6-v2                     | sentence embedding   | en       | 
| intfloat/multilingual-e5-large       | sentence embedding   | en, nl   | 
| clips/e5-large-trm-nl                | sentence embedding   | nl       | 
| nlwiki_20180420_100d                 | word embedding       | nl       | 

The validation was run using the code in ``validate_semantic_association.py``. Code for the plotting the validation is in ``notebooks/validation_plots.rmd`` and the plots are in the ``figs/`` folder.