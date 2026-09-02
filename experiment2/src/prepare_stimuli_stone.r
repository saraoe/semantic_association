## Add target, context, and lp columns to rt_df of Stone et al., 2023 ##

library(tidytable)
library(purrr)
library(pangoling)

setwd("experiment2")

data_path <- file.path("data", "Stone")

stim <- read.csv(file.path(data_path, "experimental_stimuli.tsv"), sep = "\t")

# make on row for each word
stim <- stim |>
    select(item, cond, cond_label, list, context) |>
    mutate(id = as.factor(item):as.factor(cond) |> as.numeric()) |>
    separate_rows(context, sep = "\\s+") |> # check what "_" means
    rename(word = context)

# create context and target columns
stim <- stim |>
    group_by(id) |>
    mutate(context = accumulate(word, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    ungroup() |>
    mutate(target = word)

# extract lp from gpt2
causal_preload("gpt2")
causal_preload("EleutherAI/pythia-70m-deduped")

stim <- stim |>
    mutate("lp_gpt2" = causal_words_pred(target,
        by = id,
        model = "gpt2",
        batch_size = 10
    )) |>
    mutate("lp_pythia" = causal_words_pred(target,
        by = id,
        model = "EleutherAI/pythia-70m-deduped",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_pythia))

# write csv
write.csv(stim, file.path(data_folder, "stim.csv"))
