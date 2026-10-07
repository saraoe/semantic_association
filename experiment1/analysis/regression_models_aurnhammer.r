### Regression models:  Models N400 from Aurnhammer et al. (2021) ###

library(tidytable)
library(stringr)
library(brms)
library(dplyr)

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

setwd("experiment1")

out_folder <- file.path("analysis", "brms_models")
if (!dir.exists(out_folder)) {
    dir.create(out_folder)
}

# priors
erp_priors <- c(
    prior(normal(0, 20), class = Intercept),
    prior(normal(0, 10), class = b),
    prior(normal(0, 10), class = sigma),
    prior(normal(0, 10), class = sd)
)

n400_chs <- c(
    "Cz", "Pz", "C4", "CP6", "P4", "P3",
    "CP5", "C3", "P8", "P7"
)

# read data
erp_df <- read.csv(file.path("data", "Aurnhammer", "CAPExp.csv"))

id_cols <- c(
    "ItemNum", "Condition", "Subject",
    "TrialNum", "Cloze", "Cloze_Balanced",
    "Association", "Association_RC",
    "Association_MC", "Association_weighted"
)

mean_amplitude_df <- erp_df |>
    select(all_of(c(id_cols, n400_chs, "Timestamp"))) |>
    filter(Timestamp >= 300 & Timestamp <= 500) |>
    pivot_longer(
        cols = n400_chs,
        names_to = "channel", values_to = "amplitude"
    ) |>
    group_by(across(all_of(id_cols))) |>
    summarize(n400 = mean(amplitude, na.rm = TRUE))

lp_df <- read.csv(file.path("results", "aurnhammer_log_probability.csv")) |>
    select(-X) |>
    rename("ItemNum" = Item)

aurnhammer_df <- read.csv(file.path("results", "aurnhammer_semantic_association.csv")) |>
    rename("ItemNum" = Item) |>
    left_join(lp_df) |>
    left_join(mean_amplitude_df) |>
    mutate(model = str_replace(model, "/", "_")) |>
    mutate(full_implementation = paste(implementation, model, sep = "_")) |>
    # only use complete cases across implementations of sem
    group_by(ItemNum, Condition) |>
    filter(all(!is.na(semantic_association))) |>
    ungroup() |>
    arrange(Subject, ItemNum, Condition)

# test df
if (any(is.na(aurnhammer_df$semantic_association))) {
    print("NAs in data frame!")
    quit()
}

n_obs_per_implementation <- aurnhammer_df |>
    group_by(full_implementation) |>
    summarize("N" = n()) |>
    pull(N)

if (!length(unique(n_obs_per_implementation)) == 1) {
    print("Some implementations have more observations!")
    quit()
}

# model formula
# sem
sem_formula <- bf(
    n400 ~ s_sem +
        (s_sem || Subject) +
        (s_sem || ItemNum)
)

# sem + lp
sem_lp_formula <- bf(
    n400 ~ s_sem + s_lp +
        (s_sem + s_lp || Subject) +
        (s_sem + s_lp || ItemNum)
)

all_implementations <- aurnhammer_df |>
    pull(full_implementation) |>
    unique()

for (impl in all_implementations) {
    print(impl)
    data <- aurnhammer_df |>
        filter(
            full_implementation == impl
        ) |>
        mutate(s_sem = scale(semantic_association))

    fit_sem <- brm(sem_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("aurnhammer_", impl))
    )

    fit_sem_lp <- brm(sem_lp_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("aurnhammer_lp_", impl))
    )
}
