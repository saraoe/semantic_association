# Experiment 2: The influence on context on embedding-based estimation of semantic association

Semantic association is defined as the semantic relation between a word and its preceding context. When using embeddings to define this measure, one must calculate an embedding of the context and the word such that, $$\text{Semantic Associator} = \text{Similarity}(e_{context}, e_{word})$$

where $e_i$ refers to the embedding of element $i$. When using static word embeddings to extract these embeddings, one must decide on how to define the embedding of the context (i.e., how to aggregate the embeddings of the words in the context). This is achieved by averaging the embeddings of either all the words in the preceding context or the embeddings of selected words (e.g., omitting function words). While this approach works for sentence-level stimuli (as seen in [1-4] and shown in experiment 1), when the preceding context grows this naive averaging might eliminate the signal. 
Sentence embedding models are trained for creating aggregations of multiple tokens (sentences or longer documents). As such, one would assume that these represent longer context better than averaged word embeddings.

In this experiment, we want to test the role of context lengths in embedding-based semantic association. We calculate semantic association using word embeddings (WE) and sentence embeddings (SE) on two datasets: 1) ZuCo 2.0 [5], that consists of natural English sentences, and 2) the Alice Datasets [6] which consists of natural English texts with longer contexts (a chapter of Alice in Wonderland). The estimated values of semantic association were subsequently fitted to the N400. 

## Models
| Embeddings | Hugging Face model                              |
| -------------- | --------------------------------------- |
| SE             | intfloat/multilingual-e5-large          |
| SE             | intfloat/e5-large-v2                    |
| SE             | whaleloops/phrase-bert                  |
| WE             | enwiki_20180420_300d                    |
| WE             | word2vec-google-news-300                |
| CWE            | enwiki_20180420_300d                    |
| CWE            | word2vec-google-news-300                |


## References

[1] Ettinger, A., Feldman, N., Resnik, P., & Phillips, C. (2016). Modeling N400 amplitude using vector space models of word representation. Proceedings of the Annual Meeting of the Cognitive Science Society, 38(0). https://escholarship.org/uc/item/35n97456

[2] Frank, S. L., & Willems, R. M. (2017). Word predictability and semantic similarity show distinct patterns of brain activity during language comprehension. Language, Cognition and Neuroscience, 32(9), 1192–1203. https://doi.org/10.1080/23273798.2017.1323109

[3] Broderick, M. P., Anderson, A. J., Liberto, G. M. D., Crosse, M. J., & Lalor, E. C. (2018). Electrophysiological Correlates of Semantic Dissimilarity Reflect the Comprehension of Natural, Narrative Speech. Current Biology, 28(5), 803-809.e3. https://doi.org/10.1016/j.cub.2018.01.080

[4] Xu, H., Nakanishi, M., & Coulson, S. (2024). Revisiting Joke Comprehension with Surprisal and Contextual Similarity: Implication from N400 and P600 Components. Proceedings of the Annual Meeting of the Cognitive Science Society, 46(0). https://escholarship.org/uc/item/01n9j76q

[5] Hollenstein, N., Troendle, M., Zhang, C., & Langer, N. (2020). ZuCo 2.0: A Dataset of Physiological Recordings During Natural Reading and Annotation. In N. Calzolari, F. Béchet, P. Blache, K. Choukri, C. Cieri, T. Declerck, S. Goggi, H. Isahara, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), Proceedings of the Twelfth Language Resources and Evaluation Conference (pp. 138–146). European Language Resources Association. https://aclanthology.org/2020.lrec-1.18

[6] Bhattasali, S., Brennan, J., Luh, W.-M., Franzluebbers, B., & Hale, J. (2020). The Alice Datasets: fMRI & EEG Observations of Natural Language Comprehension. In N. Calzolari, F. Béchet, P. Blache, K. Choukri, C. Cieri, T. Declerck, S. Goggi, H. Isahara, B. Maegaard, J. Mariani, H. Mazo, A. Moreno, J. Odijk, & S. Piperidis (Eds.), Proceedings of the Twelfth Language Resources and Evaluation Conference (pp. 120–125). European Language Resources Association. https://aclanthology.org/2020.lrec-1.15
