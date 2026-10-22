# Experiment 3: The influence of context on embedding-based estimation of semantic association

Semantic association is defined as the semantic relation between a word and its preceding context. When using embeddings to define this measure, one must calculate an embedding of the context and the word such that, 
$$\text{Semantic Associator} = \text{Similarity}(E_{context}, E_{word})$$

where $E_i$ refers to the embedding of element $i$. When using static word embeddings to extract these embeddings, one must decide on how to define the embedding of the context (i.e., how to aggregate the embeddings of the words in the context). This was achieved by averaging the embeddings of either all the words in the preceding context or the embeddings of selected words (e.g., omitting function words). While this approach can work for sentence-level stimuli (as seen in [1-4] and shown in experiment 1 and 2), when the preceding context grows this naive averaging might eliminate the signal. 
Sentence embedding models are trained for creating aggregations of multiple tokens. As such, one would assume that these represent longer context better than averaged word embeddings.

In this experiment, we wanted to test the role of context lengths in embedding-based semantic association. We calculated semantic association using word embeddings (WE) and sentence embeddings (SE) on data from DERCo [5] and TiNT [6-7] which both consist of natural stimuli exceeding a few sentences in length; DERCo consists of five Grimm fairytales and TiNT of eight medium-length documents. The estimated values of semantic association were subsequently fitted to the N400. 

## Models
| Model | Embeddings | Language | Architecture |
|---|---|---|---|
| Word2vec/enwiki_20180420_300d | WE, CWE | English | Skip-gram |
| Word2vec/word2vec-google-news-300 | WE, CWE | English | Skip-gram |
| Word2vec/nlwiki_20180420_300d | WE, CWE | Dutch | Skip-gram |
| Qwen/Qwen3-Embedding-0.6B | SE | Multilingual | Decoder |
| Qwen/Qwen3-Embedding-8B | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-small | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-nano | SE | Multilingual | Encoder |
| intfloat/multilingual-e5-large | SE | Multilingual | Encoder |
| BAAI/bge-m3 | SE | English | Encoder |
| intfloat/e5-large-v2 | SE | English | Encoder |
| clips/e5-large-trm-nl | SE | Dutch | Encoder |


## References

[1] Ettinger, A., Feldman, N., Resnik, P., & Phillips, C. (2016). Modeling N400 amplitude using vector space models of word representation. Proceedings of the Annual Meeting of the Cognitive Science Society, 38(0). https://escholarship.org/uc/item/35n97456

[2] Frank, S. L., & Willems, R. M. (2017). Word predictability and semantic similarity show distinct patterns of brain activity during language comprehension. Language, Cognition and Neuroscience, 32(9), 1192–1203. https://doi.org/10.1080/23273798.2017.1323109

[3] Broderick, M. P., Anderson, A. J., Liberto, G. M. D., Crosse, M. J., & Lalor, E. C. (2018). Electrophysiological Correlates of Semantic Dissimilarity Reflect the Comprehension of Natural, Narrative Speech. Current Biology, 28(5), 803-809.e3. https://doi.org/10.1016/j.cub.2018.01.080

[4] Xu, H., Nakanishi, M., & Coulson, S. (2024). Revisiting Joke Comprehension with Surprisal and Contextual Similarity: Implication from N400 and P600 Components. Proceedings of the Annual Meeting of the Cognitive Science Society, 46(0). https://escholarship.org/uc/item/01n9j76q

[5] Quach, B. M., Gurrin, C., & Healy, G. (2024). DERCo: A Dataset for Human Behaviour in Reading Comprehension Using EEG. Scientific Data, 11(1), 1104. https://doi.org/10.1038/s41597-024-03915-8

[6] Østergaard, S. M., Lichtenberg, L. D., Boon, L., & Nicenboim, B. (2026). A Corpus of Joint EEG and Self-Paced Reading of Natural Dutch Texts. 11260–11271. https://doi.org/10.63317/49tvxys2q4zc

[7] Østergaard, Sara Møller; Lichtenberg, Lenneke; Boon, Laura; Nicenboim, Bruno, 2026, "EEG and Self-Paced Reading of Natural, Dutch Texts (Towards a computational model of reading (TCMR))", https://doi.org/10.34894/0O5XQ7, DataverseNL
