# Make target and context cols in tint_stimuli.csv file from cmcl26/ folder

library(tidytable)
library(stringr)
library(purrr)

stim <- read.csv(file.path("cmcl26", "data", "tint_stim.csv")) |>
    select(-X)

stim <- stim |>
    mutate(target = word) |>
    group_by(document_id) |>
    mutate(context = accumulate(target, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    ungroup()

write.csv(stim, file.path("experiment3", "data", "tint_stim.csv"))
