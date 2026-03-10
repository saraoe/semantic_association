# Semantic association

This repository contains code for the paper "Modeling semantic association in self-paced reading with language model embeddings"[1] which has been submitted to The 15th Workshop on Cognitive Modeling and Computational Linguistics (CMCL).

## Implementations of semantic association
Ten different implementations of semantic association was used to extract semantic association from the Tilburg corpus of Natural Dutch Texts (TiNT)[2]. The implementations varied in embedding model (word embeddings and sentence embeddings) and in context lengths. 


| **Name** | **Embedding model** | **Context** | **Words** |
| --- | --- | --- | --- |
| SE, All | Sentence Embeddings | All preceding words | All |
| SE, Sentence(N=1) | Sentence Embeddings | One sentence before the target sentence | All |
| WE, All | Word Embeddings | All preceding words | All |
| WE, Sentence(N=1) | Word Embeddings | One sentence before the target sentence | All |
| WE, Weighted | Word Embeddings | All preceding words (weighted) | All |
| CWE, All | Word Embeddings | All preceding words | Content words |
| CWE, Sentence(N=1) | Word Embeddings | One sentence before the target sentence | Content words |
| CWE, Weighted | Word Embeddings | All preceding words (weighted) | Content words |
| CWE, Windowed(N=2) | Word Embeddings | One content word preceding the target | Content words |
| CWE, Windowed(N=2) | Word Embeddings | Two content word preceding the target | Content words |

The word embedding model was *Word2vec/nlwiki_20180420_300d* and the sentence embeddings model was *clips/e5-large-trm-nl*.

## Inital exploration
Before fitting the implementations of semantic association (see ``src/word_embedding_models.py`` and ``src/sentence_embedding_models.py``) to the data from the TiNT corpus, all the implementations were validated using the data from [Federmeier & Kutas  (1999)](https://doi.org/10.1006/jmla.1999.2660). Below you can see what models were validated and on which language (Dutch and/or English).

| Model Name                           | Model type           | Language | 
| ------------------------------------ | -------------------- | -------- | 
| enwiki_20180420_100d                 | word embedding       | en       | 
| word2vec-google-news-300             | word embedding       | en       | 
| all-MiniLM-L6-v2                     | sentence embedding   | en       | 
| intfloat/multilingual-e5-large       | sentence embedding   | en, nl   | 
| clips/e5-large-trm-nl                | sentence embedding   | nl       | 
| nlwiki_20180420_100d                 | word embedding       | nl       | 

The validation was run using the code in ``src/validate_semantic_association.py``. Code for the plotting the validation is in ``notebooks/validation_plots.rmd`` and the plots are in the ``figs/`` folder.

OpenAI's GPT-5.2 model was used to generate longer contexts for the stimuli of Federmeier and Kutas (1999) and translating the stimuli to Dutch. The code for this is in ``src/add_context_and_translate.py``.

## References
[1] *reference coming*,
[2] Østergaard, Sara Møller; Lichtenberg, Lenneke; Boon, Laura; Nicenboim, Bruno, 2026, "EEG and Self-Paced Reading of Natural, Dutch Texts (Towards a computational model of reading (TCMR))", https://doi.org/10.34894/0O5XQ7, DataverseNL