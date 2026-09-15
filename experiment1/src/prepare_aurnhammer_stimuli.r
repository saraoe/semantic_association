# Define context and target for stimuli from Aurnhammer et al. (2021)

library(tidytable)

setwd("experiment1")

stim <- read.csv(file.path("data", "aurnhammer_2021_stim.csv"))

stim <- stim |>
    separate(Target, into = c("article", "target"), sep = " ", extra = "merge") |>
    mutate(context = paste(Sentence, article)) |>
    select(-Sentence)

write.csv(stim, file.path("data", "aurnhammer_2021_stim.csv"))
