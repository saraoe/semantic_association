library(tidytable)
library(stringr)

rename_implementations <- function(name) {
    name <- str_replace(name, "semantic_association_", "")

    name <- str_replace(name, "SentenceEmbedding", "SE, ")
    name <- str_replace(name, "WordEmbeddingContentWord", "CWE, ")
    name <- str_replace(name, "WordEmbedding", "WE, ")

    name <- str_replace(name, "_nSentences", "Sentence")
    name <- str_replace(name, "1", "(N=1)")
    name <- str_replace(name, "2", "(N=2)")
    name <- str_replace(name, "WE, Windowed", "CWE, Windowed")

    name <- str_replace(name, ", $", ", All")
    return(name)
}
