### Extracting log-probability (lp) for linguistic stimuli ###

library(tidytable)
library(readxl)
library(pangoling)

setwd("experiment1")

# preload models
causal_preload("EleutherAI/pythia-70m-deduped")
causal_preload("benjamin/gerpt2")
causal_preload("GroNLP/gpt2-small-dutch")

# Kuperberg et al. (2003, 2007)
kuperberg_stim <- read_excel(file.path("data", "Kuperberg", "sentences.xlsx")) |>
    filter(!is.na(target)) |> # one sentence doesn't have a target
    select(-edited)

kuperberg_stim <- kuperberg_stim |>
    mutate("lp_pythia" = causal_targets_pred(
        contexts = context,
        targets = target,
        model = "EleutherAI/pythia-70m-deduped",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_pythia))

write.csv(kuperberg_stim, file.path("results", "kuperberg_log_probability.csv"))

# Kim & Osterhout (2005)
kim_osterhout_stim <- read.csv(file.path("data", "kim_osterhout_2005_stim.csv")) |>
    select(-X)

kim_osterhout_stim <- kim_osterhout_stim |>
    mutate("lp_pythia" = causal_targets_pred(
        contexts = context,
        targets = target,
        model = "EleutherAI/pythia-70m-deduped",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_pythia))

write.csv(kim_osterhout_stim, file.path("results", "kim_osterhout_log_probability.csv"))

# Michaelov et al. (2024)
michaelov_stim <- read.csv(file.path("data", "michaelov_2024_stim.csv"))

michaelov_stim <- michaelov_stim |>
    mutate("lp_pythia" = causal_targets_pred(
        contexts = context,
        targets = target,
        model = "EleutherAI/pythia-70m-deduped",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_pythia))

write.csv(michaelov_stim, file.path("results", "michaelov_log_probability.csv"))

# Delogu et al. (2019)
delogu_stim <- read_excel(file.path("data", "delogu_2019_stim.xlsx"))

delogu_stim <- delogu_stim |>
    mutate("lp_benjamin_gerpt2" = causal_targets_pred(
        contexts = context,
        targets = target,
        model = "benjamin/gerpt2",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_benjamin_gerpt2))

write.csv(delogu_stim, file.path("results", "delogu_log_probability.csv"))

# Delogu et al. (2019), Dutch
delogu_nl_stim <- read.csv(file.path("data", "delogu_2019_stim_nl.csv")) |>
    select(-X)

delogu_nl_stim <- delogu_nl_stim |>
    mutate("lp_GroNLP_gpt2_small_dutch" = causal_targets_pred(
        contexts = context,
        targets = target,
        model = "GroNLP/gpt2-small-dutch",
        batch_size = 10
    )) |>
    mutate("s_lp" = scale(lp_GroNLP_gpt2_small_dutch))

write.csv(delogu_nl_stim, file.path("results", "delogu_nl_log_probability.csv"))
