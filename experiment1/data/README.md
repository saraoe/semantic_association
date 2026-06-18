# Data for experiment 1

## Kuperberg
The folder ``Kuperberg`` contains linguistic stimuli from the two papers [1] and [2]. The function in ``src/prepare_stimuli.py`` was used to extract target words and their preceding context from the sentences. For a couple of sentences the target verb was not annotated as a verb by SpaCy (i.e., when the verb was "scribble"). These sentences were manually annotated after (which is indicated by the "manually_annotated" column).

The ready stimuli is in the file ``Kuperberg/sentence.xlsx``.

## Delogu (2019)
The file ``delogu_2019_stim.csv`` is the stimuli from the study "Event-related potentials index lexical retrieval (N400) and integration (P600) during language comprehension" by Delogu et al. [3]. The file contains linguistic stimuli (90 sentence frames with each three conditions, i.e., 270 unique sentences). The stimuli was obtained from the appendix of the paper.

## Hoeks
The folder ``Hoeks`` contains the linguistic stimuli from the paper [4]. The file ``sentences.csv`` contains on row for each sentence frame. This is preprocessed in the script ``src/prepare_hoeks_stim.py``, where the file ``stim.csv`` is created, which contains on row for each condition in each sentence frame together with the target and context.

## Michaelov (2024)
The file ``michaelov_2024.csv`` is from the study "Strong Prediction: Language Model Surprisal  Explains Multiple N400 Effects" by Michaelov et al. [5]. The file contains linguistic stimuli (125 sentence frames with each four conditions, i.e., 500 unique sentences) along with the N400 (in different channels) for 50 participants. The file was downloaded from the [OSF repository](https://osf.io/pysbc/files/osfstorage) on 15-04-2026 and was called ``data/N400_data.csv``.

## SUBTLEX-US

SUBTLEX-US was downloaded from https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus on 08-04-2026. The downloaded file is the one under "Zipf values added to the SUBTLEX-US frequencies". When downloaded, the file is named "SUBTLEX-US frequency list with PoS and Zipf information.xlsx", but was manually renamed to "SUBTLEX-US.xlsx".

## References
[1] Kuperberg GR, Sitnikova T, Caplan D, Holcomb PJ. Electrophysiological distinctions in processing conceptual relationships within simple sentences. Cogn Brain Res 2003; 217:117-29.

[2] Kuperberg GR, Kreher DA, Sitnikova T, Caplan D, Holcomb PJ. The role of animacy and thematic relationships in processing active English sentences: Evidence from event-related potentials. Brain and Language 2007; 100: 223-238. 

[3] Delogu, F., Brouwer, H., & Crocker, M. W. (2019). Event-related potentials index lexical retrieval (N400) and integration (P600) during language comprehension. Brain and Cognition, 135, 103569. https://doi.org/10.1016/j.bandc.2019.05.007

[4] Hoeks, J. C. J., Stowe, L. A., & Doedens, G. (2004). Seeing words in context: The interaction of lexical and sentence level information during reading. Cognitive Brain Research, 19(1), 59–73. https://doi.org/10.1016/j.cogbrainres.2003.10.022

[5] Michaelov, J. A., Bardolph, M. D., Van Petten, C. K., Bergen, B. K., & Coulson, S. (2024). Strong Prediction: Language Model Surprisal Explains Multiple N400 Effects. Neurobiology of Language, 5(1), 107–135. https://doi.org/10.1162/nol_a_00105
