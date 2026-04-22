# Experiment 1: Embedding-based semantic association for capturing effects of semantic illusions

Studies of semantic illusions show that semantic association affects online word processing beyond effects of word predictability. Experiment 1 investigates whether an embedding-based measure of semantic association can capture similar patterns as seen in ERP studies of semantic illusions.

We use two data sources: linguistic stimuli from Kuperberg et al. [1-2] and both stimuli and neural signal (N400) from Michaelov et al. [3]. For more information see ``data/README.md``.

We extract embedding-based semantic association using multiple embedding-models - both sentence embedding (SE) models, word embedding (WE) models, content word embeddings (CWE; same models as the WE, but only including embeddings of content words for the context embedding - see [4] for more information), and contextualized word embeddings from BERT (BERTWE). 

We find semantic association extracted from all embeddings models except BERTWE capture patterns in semantic illusions similar to those found in humans. Thus, it seems that the choice of embedding model plays an insignificant role when estimating semantic association in handcrafted sentence-level stimuli.

## Models
| Embeddings | Hugging Face model                              |
| -------------- | --------------------------------------- |
| SE             | intfloat/multilingual-e5-large          |
| SE             | BAAI/bge-m3                             |
| SE             | Gameselo/STS-multilingual-mpnet-base-v2 |
| SE             | intfloat/e5-large-v2                    |
| SE             | whaleloops/phrase-bert                  |
| WE             | enwiki_20180420_100d                    |
| WE             | enwiki_20180420_300d                    |
| WE             | word2vec-google-news-300                |
| CWE            | enwiki_20180420_100d                    |
| CWE            | enwiki_20180420_300d                    |
| CWE            | word2vec-google-news-300                |
| BERTWE         | FacebookAI/xlm-roberta-large            |


## References
[1] Kuperberg GR, Sitnikova T, Caplan D, Holcomb PJ. Electrophysiological distinctions in processing conceptual relationships within simple sentences. Cogn Brain Res 2003; 217:117-29.

[2] Kuperberg GR, Kreher DA, Sitnikova T, Caplan D, Holcomb PJ. The role of animacy and thematic relationships in processing active English sentences: Evidence from event-related potentials. Brain and Language 2007; 100: 223-238. 

[3] Michaelov, J. A., Bardolph, M. D., Van Petten, C. K., Bergen, B. K., & Coulson, S. (2024). Strong Prediction: Language Model Surprisal Explains Multiple N400 Effects. Neurobiology of Language, 5(1), 107–135. https://doi.org/10.1162/nol_a_00105

[4] Østergaard, S. M., Enevoldsen, K., Alishahi, A., & Nicenboim, B. (2026). Modeling semantic association in self-paced reading with language model embeddings. Proceedings of the 15th Workshop on Cognitive Modeling and Computational Linguistics.