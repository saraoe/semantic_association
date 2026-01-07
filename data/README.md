# Data

## Federmeier & Kutas (1999)
The data in the file ``federmeier_kutas_1999.xlsx`` is from [A Rose by Any Other Name: Long-Term Memory Structure and Sentence Processing](https://doi.org/10.1006/jmla.1999.2660) by Federmeier & Kutas (1999). The data includes two sentence contexts with a sentence-final target word that is either *expected*, *within category*, or *between category*. An example would be: *"Checkmate," Rosaline announced with glee. She was getting to be really good at chess/ monopoly/football.* Additionally, the stimuli is divided into two levels of contraint - high constraining and low constraining - where the high constraining context had a high cloze probability of the expected target and low constraining contexts had a low cloze probability of the expected target (divided by median split). The original study included 132 stimuli - in the file ``federmeier_kutas_1999.xlsx`` are only the 40 examples provided in the paper.

On top of the original stimuli, an extra sentence-final target were added. This was an unexpected target, i.e., a target that did not make sense it the context. The unexpected target corresponded to an expected target word in one of the previous contexts. Additionally, all the stimuli were translated into Dutch using chatGPT. Note that the translation of the two-sentence context, didn't always results in a two-sentence translated context. Furthermore, for some of the translations, the target words were not sentence final, thus, they are not included in the data.

Description of variables in the data:
| Variable Name          | Type | Description                                                       |
|------------------------|------|-------------------------------------------------------------------|
| constraint             | str  | The constraint of the stimuli (H = high, L = low)                 |
| context                | str  | The two-sentence context prior to the target                      |
| expected               | str  | The expected target                                               |
| within                 | str  | The within-category target                                        |
| between                | str  | The between-category target                                       |
| unexpected                | str  | The unexpected target                                       |
| translated_context     | str  | The Dutch-translated two-sentence context prior to the target     |
| translated_expected    | str  | The Dutch-translated expected target                              |
| translated_within      | str  | The Dutch-translated within-category target                       |
| translated_between     | str  | The Dutch-translated between-category target                      |
