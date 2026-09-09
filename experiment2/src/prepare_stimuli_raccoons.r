## Add target, context, and lp columns to stimuli df from RaCCooNS ##

library(tidytable)
library(purrr)
library(pangoling)

setwd("experiment2")

data_path <- file.path("data", "RaCCooNS")

stim <- read.csv(file.path(data_path, "words.tsv"), sep = "\t") |>
    mutate(id = item_id)

# create context and target columns
stim <- stim |>
    group_by(id) |>
    mutate(context = accumulate(word, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    mutate(word_n = row_number()) |>
    ungroup() |>
    mutate(target = word)

# extract lp from LLMs
causal_preload("GroNLP/gpt2-small-dutch")

stim <- stim |>
    mutate("lp_GroNLP_gpt2_small_dutch" = causal_words_pred(target,
        by = id,
        model = "GroNLP/gpt2-small-dutch",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_GroNLP_gpt2_small_dutch))

# write csv
write.csv(stim, file.path(data_path, "stim.csv"))

# make mean_amplitude.csv by joining stimuli and N400.tsv
n400_df <- read.csv(file.path(data_path, "N400.tsv"), sep = "\t")

n400_df <- n400_df |>
    left_join(stim) |>
    # baseline correct N400
    mutate(n400 = N400 - baseline) |>
    select(-N400) |>
    rename("subject" = "participant_id")

# write csv
write.csv(n400_df, file.path(data_path, "mean_amplitude.csv"))
