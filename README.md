# Semantic association

## Validate semantic association
Multiple definitions of semantic association were validated. First, we tried different embedding models; both word embedding models and sentence embedding models. Secondly, we used different window sizes for the context - i.e., the number of previous words in the context that the word were semantically compared to. Finally, only for the word embedding model, we defined a weighted context embedding, where the weight of each were defined as a forgetting curve.

| Model Name                           | Model type           | Language | Context window |
| ------------------------------------ | -------------------- | -------- | -------------- |
| enwiki_20180420_100d                 | word embedding       | en       | None, 4, 8     |
| word2vec-google-news-300             | word embedding       | en       | None, 4, 8     |
| all-MiniLM-L6-v2                     | sentence embedding   | en       | None, 4, 8     |
| intfloat/multilingual-e5-large       | sentence embedding   | en       | None, 4, 8     |
| nlwiki_20180420_100d                 | word embedding       | nl       | None, 4, 8     |



These models were validated using the data from [Federmeier & Kutas  (1999)](https://doi.org/10.1006/jmla.1999.2660). The resulting plots are in the ``figs/`` folder.