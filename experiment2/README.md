# Experiment 2: Natural sentences

In experiment 1, we applied embedding-based semantic association to stimuli from semantic illusions, which were hand-crafted sentences with targets in predefined conditions (semantically related or unrelated to the preceding context). In this experiment, we want to apply the metric to natural sentences (i.e. sentences with no experimental manipulation). This type of experimental data represents a key use case for embedding-based semantic association, as the metric allows semantic relationships to be quantified in natural stimuli without requiring predefined target words or experimentally manipulated conditions. Semantic association was extracted for all content words in the sentences and used as a predictor for the N400. 

For this experiment we used the UCL corpus [1] which consist of natural English sentences.

## Models
| Hugging Face reference | Embeddings | Language | Architecture |
|---|---|---|---|
| Word2vec/enwiki_20180420_300d | WE, CWE | English | Skip-gram |
| Word2vec/word2vec-google-news-300 | WE, CWE | English | Skip-gram |
| Qwen/Qwen3-Embedding-0.6B | SE | Multilingual | Decoder |
| Qwen/Qwen3-Embedding-8B | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-small | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-nano | SE | Multilingual | Encoder |
| intfloat/multilingual-e5-large | SE | Multilingual | Encoder |
| BAAI/bge-m3 | SE | English | Encoder |
| intfloat/e5-large-v2 | SE | English | Encoder |
| whaleloops/phrase-bert | SE | English | Encoder |


## References

[1] Frank, S. L., Otten, L. J., Galli, G., & Vigliocco, G. (2015). The ERP response to the amount of information conveyed by words in sentences. Brain and Language, 140, 1–11. https://doi.org/10.1016/j.bandl.2014.10.006