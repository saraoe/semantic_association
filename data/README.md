# Data

## Federmeier & Kutas (1999)
The data in the file ``federmeier_kutas_1999.csv`` is from [A Rose by Any Other Name: Long-Term Memory Structure and Sentence Processing](https://doi.org/10.1006/jmla.1999.2660) by Federmeier & Kutas (1999). The data includes two sentence contexts with a sentence-final target word that is either *expected*, *within category*, or *between category*. An example would be: *"Checkmate," Rosaline announced with glee. She was getting to be really good at chess/ monopoly/football.* Additionally, the stimuli is divided into two levels of contraint - high constraining and low constraining - where the high constraining context had a high cloze probability of the expected target and low constraining contexts had a low cloze probability of the expected target (divided by median split). The original study included 132 stimuli - in the file ``federmeier_kutas_1999.csv`` are only the 40 examples provided in the paper.

On top of the original stimuli, an extra sentence-final target were added. This was an unexpected target, i.e., a target that did not make sense it the context. The unexpected target corresponded to an expected target word in one of the previous contexts. Additionally, a longer context of approx. 100 words that could come before the original two-sentence context and the expected target were added in a new column ("longer context"). The longer context was generated using GPT-5. Finally, all the stimuli were translated into Dutch using chatGPT (see ``src/add_context_and_translate.py``).

Description of variables in the data:
| Variable Name          | Type | Description                                                       |
|------------------------|------|-------------------------------------------------------------------|
| constraint             | str  | The constraint of the stimuli (H = high, L = low)                 |
| context                | str  | The two-sentence context prior to the target                      |
| expected               | str  | The expected target                                               |
| within                 | str  | The within-category target                                        |
| between                | str  | The between-category target                                       |
| unexpected             | str  | The unexpected target                                             |
| longer_context         | str  | A longer ~100 words context                                       |
| translated_context     | str  | The Dutch-translated two-sentence context prior to the target     |
| translated_expected    | str  | The Dutch-translated expected target                              |
| translated_within      | str  | The Dutch-translated within-category target                       |
| translated_between     | str  | The Dutch-translated between-category target                      |
| translated_longer_context  | str  | The Dutch-translated longer ~100 words context                                       |
