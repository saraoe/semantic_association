# Data

# Tilburg corpus of Natural Dutch Texts (TiNT)
The data in the file ``tint.csv`` is from the Tilburg corpus of Natural Dutch Texts (TiNT). The code for data preprocessing is in the ``natural-stories-dutch`` repository. The data is read from the ``natural-stories-dutch`` repository in the file ``src/read_tint.r``.

Descriptions of variables:
| Variable Name                 | Type  | Description                                                       |
|-------------------------------|-------|-------------------------------------------------------------------
| n400                          | float | The N400 ERP component (in microvolt). The average amplitude between 300-500 ms after the onset of the word in centroparietal electrodes.|
| p600                          | float | The P600 ERP component (in microvolt). The average amplitude between 500-700 ms after the onset of the word in centroparietal electrodes.|
| rt                            | float | Reading time (in ms). Calculated as the time between EEG triggers. |
| story_name                    | str   | Name of the story/document |
| document_id                   | int   | ID of the story/document |
| trial                         | int   | Trial number (order in which the documents were read) |
| word_n                        | int   | Word number within a paragraph |
| paragraph_n                   | int   | Paragraph number |
| number_word                   | int   | Word number within the entire text |
| participant_number            | int   | Unique number for the participant |
| gender                        | str   | Gender of the participant |
| age                           | int   | Age of the participant |
| word                          | str   | Word being read on the screen |
| word_rm_punct                 | str   | Word in lower case and with all punctuation removed |
| pos                           | str   | POS tag of the word |
| content_word                  | boolean | Whether the word is a content word or not (i.e., if the pos tag of the word is either noun, verb, adjective, or adverb. |
| zipf_freq                     | float | Zipf frequency of the word (from the the SUBTLEX-NL corpus) |
| zero_freq                     | boolean | Word that didn't have a frequency in the SUBTLEX-NL corpus |
| lp                            | float | Log-probability of the word (averaged over probabilities extracted from four GPT-models) |
| wl                            | int   | Word length |
| s_lp                          | float | Scaled log-probability |
| s_wl                          | float | Scaled word length |
| s_freq                        | float | Scaled zipf frequency |
| s_lp1, s_lp2, s_lp3           | float | Scaled log-probability with lag 1, 2, and 3 |
| s_wl1, s_wl2, s_wl3           | float | Scaled word length with lag 1, 2, and 3 |
| s_freq1, s_freq2, s_freq3     | float | Scaled zipf frequency with lag 1, 2, and 3 |


## Federmeier & Kutas (1999)
The data in the file ``federmeier_kutas_1999.csv`` is from [A Rose by Any Other Name: Long-Term Memory Structure and Sentence Processing](https://doi.org/10.1006/jmla.1999.2660) by Federmeier & Kutas (1999). The data includes two sentence contexts with a sentence-final target word that is either *expected*, *within category*, or *between category*. An example would be: *"Checkmate," Rosaline announced with glee. She was getting to be really good at chess/ monopoly/football.* Additionally, the stimuli is divided into two levels of contraint - high constraining and low constraining - where the high constraining context had a high cloze probability of the expected target and low constraining contexts had a low cloze probability of the expected target (divided by median split). The original study included 132 stimuli - in the file ``federmeier_kutas_1999.csv`` are only the 40 examples provided in the paper.

On top of the original stimuli, an extra sentence-final target were added. This was an unexpected target, i.e., a target that did not make sense it the context. The unexpected target corresponded to an expected target word in one of the previous contexts. Additionally, a longer context of approx. 100 words that could come before the original two-sentence context and the expected target were added in a new column ("longer context"). The longer context was generated using GPT-5. Finally, all the stimuli were translated into Dutch using chatGPT (see ``src/add_context_and_translate.py``).

Description of variables:
| Variable Name          | Type | Description                                                       |
|------------------------|------|-------------------------------------------------------------------|
| constraint                | str  | The constraint of the stimuli (H = high, L = low)                 |
| context                   | str  | The two-sentence context prior to the target                      |
| expected                  | str  | The expected target                                               |
| within                    | str  | The within-category target                                        |
| between                   | str  | The between-category target                                       |
| unexpected                | str  | The unexpected target                                             |
| longer_context            | str  | A longer ~100 words context                                       |
| translated_context        | str  | The Dutch-translated two-sentence context prior to the target     |
| translated_expected       | str  | The Dutch-translated expected target                              |
| translated_within         | str  | The Dutch-translated within-category target                       |
| translated_between        | str  | The Dutch-translated between-category target                      |
| translated_longer_context  | str  | The Dutch-translated longer ~100 words context                |
