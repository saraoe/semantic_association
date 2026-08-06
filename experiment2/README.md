# Experiment 2: Natural sentences

Semantic association is defined as the semantic relation between a word and its preceding context. When using embeddings to define this measure, one must calculate an embedding of the context and the word such that, $$\text{Semantic Associator} = \text{Similarity}(e_{context}, e_{word})$$

where $e_i$ refers to the embedding of element $i$. The results of experiment 1 shows that this method can capture known patterns from semantic illusions - both when applying word embeddings (WE), content word embeddings (CWE), and sentence embeddings (SE). In this experiment, we want to test the method when applied to natural sentences (i.e. sentences with no experimental manipulation). Semantic association is extracted for all content words in the sentences and used as a predictor for the N400. 

We use two datasets: 1) Tanner et al. [1] and 2) The UCL corpus [2] which both consist of English sentences.

## Models
| Embeddings | Hugging Face model                          |
| -------------- | --------------------------------------- |
| SE             | intfloat/multilingual-e5-large          |
| SE             | intfloat/e5-large-v2                    |
| SE             | whaleloops/phrase-bert                  |
| SE             | BAAI/bge-m3                             |
| SE             | bigscience/sgpt-bloom-7b1-msmarco       |
| SE             | Qwen/Qwen3-Embedding-0.6B               |
| SE             | Qwen/Qwen3-Embedding-8B                 |
| WE             | enwiki_20180420_300d                    |
| WE             | word2vec-google-news-300                |
| CWE            | enwiki_20180420_300d                    |
| CWE            | word2vec-google-news-300                |


## References

[1] Tanner, D. (2019). Robust neurocognitive individual differences in grammatical agreement processing: A latent variable approach. Cortex, 111, 210–237. https://doi.org/10.1016/j.cortex.2018.10.011

[2] Frank, S. L., Otten, L. J., Galli, G., & Vigliocco, G. (2015). The ERP response to the amount of information conveyed by words in sentences. Brain and Language, 140, 1–11. https://doi.org/10.1016/j.bandl.2014.10.006