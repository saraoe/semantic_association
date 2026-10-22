# Experiment 1: Embedding-based semantic association for capturing effects of semantic illusions

Studies of semantic illusions show that semantic association affects online word processing beyond effects of word predictability. Experiment 1 investigates whether an embedding-based measure of semantic association can capture similar patterns as seen in ERP studies of semantic illusions.

We use three corpora: linguistic stimuli from Kuperberg et al. [1-2] and Kim & Osterhout [3] as well as both stimuli and neural signal (N400) from Delogu et al. [4]. For more information see ``data/README.md``.

We extract embedding-based semantic association using multiple embedding-models -- both sentence embedding (SE) models, word embedding (WE) models, and content word embeddings (CWE; same models as the WE, but only including embeddings of content words for the context embedding - see [5] for more information). 

## Models
| Hugging Face reference | Embeddings | Language | Architecture |
|---|---|---|---|
| Word2vec/enwiki_20180420_100d | WE, CWE | English | Skip-gram |
| Word2vec/enwiki_20180420_300d | WE, CWE | English | Skip-gram |
| Word2vec/word2vec-google-news-300 | WE, CWE | English | Skip-gram |
| Word2vec/dewiki_20180420_100d | WE, CWE | German | Skip-gram |
| Word2vec/dewiki_20180420_300d | WE, CWE | German | Skip-gram |
| Qwen/Qwen3-Embedding-0.6B | SE | Multilingual | Decoder |
| Qwen/Qwen3-Embedding-8B | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-small | SE | Multilingual | Decoder |
| jinaai/jina-embeddings-v5-text-nano | SE | Multilingual | Encoder |
| intfloat/multilingual-e5-large | SE | Multilingual | Encoder |
| BAAI/bge-m3 | SE | English | Encoder |
| intfloat/e5-large-v2 | SE | English | Encoder |
| whaleloops/phrase-bert | SE | English | Encoder |
| aari1995/German_Semantic_STS_V2 | SE | German | Encoder |


## References
[1] Kuperberg GR, Sitnikova T, Caplan D, Holcomb PJ. Electrophysiological distinctions in processing conceptual relationships within simple sentences. Cogn Brain Res 2003; 217:117-29.

[2] Kuperberg GR, Kreher DA, Sitnikova T, Caplan D, Holcomb PJ. The role of animacy and thematic relationships in processing active English sentences: Evidence from event-related potentials. Brain and Language 2007; 100: 223-238. 

[3] Kim, A., & Osterhout, L. (2005). The independence of combinatory semantic processing: Evidence from event-related potentials. Journal of Memory and Language, 52(2), 205–225. https://doi.org/10.1016/j.jml.2004.10.002

[4] Delogu, F., Brouwer, H., & Crocker, M. W. (2019). Event-related potentials index lexical retrieval (N400) and integration (P600) during language comprehension. Brain and Cognition, 135, 103569. https://doi.org/10.1016/j.bandc.2019.05.007

[5] Østergaard, S. M., Enevoldsen, K., Alishahi, A., & Nicenboim, B. (2026). Modeling semantic association in self-paced reading with language model embeddings. Proceedings of the 15th Workshop on Cognitive Modeling and Computational Linguistics.