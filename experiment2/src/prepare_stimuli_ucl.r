# Extract stimuli from EEG files
# NB: src/extract_erps_ucl.py must be run before this file

library(tidytable)
library(purrr)
library(pangoling)

setwd("experiment2")

data_folder <- file.path("data", "UCL")
mean_amplitude <- read.csv(file.path(data_folder, "mean_amplitude.csv"))

erp_names <- c("ELAN", "LAN", "N400", "EPNP", "P600", "PNP")

stim <- mean_amplitude |>
    select(-c(X, subject, reject, artifact, erp_names)) |>
    distinct() |>
    arrange(id, word_n)

# create context and target columns
stim <- stim |>
    group_by(id) |>
    mutate(context = accumulate(word, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    ungroup() |>
    mutate(target = word)


# extract lp from LLMs
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
    mutate("s_lp" = scale(lp_gpt2))

write.csv(stim, file.path(data_folder, "stim.csv"))
