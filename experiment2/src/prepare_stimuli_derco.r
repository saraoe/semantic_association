# Extract stimuli from EEG files
# NB: src/extract_erps_derco.py must be run before this file

library(tidytable)
library(tidyr)
library(stringr)
library(readr)
library(purrr)

setwd("experiment2")

data_folder <- file.path("data", "DERCo")
mean_amplitude <- read.csv(file.path(data_folder, "mean_amplitude.csv"))

clean_word <- function(word) {
    # change fancy quotation
    word <- str_replace(word, "’", "'")
    word <- str_replace(word, "”", "\"")
    # remove punct only at beginning or end of string
    word <- str_remove_all(word, "^[[:punct:]]+|[[:punct:]]+$")
    # remove "-" in the middle of a string
    word <- str_remove_all(word, "-")
    word <- tolower(word)
    return(word)
}

stim <- mean_amplitude |>
    select(-c(X, n400, p600, subject)) |>
    distinct() |>
    separate(
        word,
        into = c("word_clean", "article_n", "word_n"),
        sep = "_",
        remove = FALSE
    ) |>
    mutate(
        article_n = as.factor(article_n),
        word_n = as.integer(word_n)
    ) |>
    arrange(article_n, word_n)

# get words from raw articles
words_df <- data.frame()
for (article_number in 0:4) {
    article_txt <- read_file(
        file.path(
            data_folder, "articles",
            paste0("article_", article_number, ".txt")
        )
    )
    words <- str_split(article_txt, "\\s+")[[1]]

    # check the number of words match the EEG data
    n_words_stim <- stim |>
        filter(article_n == article_number) |>
        nrow()
    if (length(words) != n_words_stim) {
        print(paste("Article:", article_number))
        print("The number of words in the raw article doesn't match the number of words in the EEG data")
        break
    }
    # check all the words are the same
    stim_words <- stim |>
        filter(article_n == article_number) |>
        pull(word_clean)
    if (!all(clean_word(words) == stim_words)) {
        print(paste("Article:", article_number))
        print("The words in the raw article doesn't match the words in the EEG data")
        break
    }

    words_df <- words_df |>
        rbind(data.frame(
            "target" = words,
            "article_n" = article_number,
            "word_n" = seq_along(words) - 1, # zero index
            "word_clean" = clean_word(words)
        )) |>
        mutate(article_n = as.factor(article_n))
}

stim <- stim |>
    left_join(words_df) |>
    group_by(article_n) |>
    mutate(context = accumulate(target, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    ungroup()

write.csv(stim, file.path(data_folder, "stim.csv"))
