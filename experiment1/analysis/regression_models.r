### Regression models:  Models N400 from Delogu et al., 2019 ###

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

### Delogu et al. (2019) ###
# read data
erp_df <- read.csv(file.path("data", "Delogu", "dbc_data.csv"))

id_cols <- c(
    "ItemNum", "Condition", "Subject",
    "TrialNum", "Assoc", "Plaus"
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

lp_df <- read.csv(file.path("results", "delogu_log_probability.csv")) |>
    select(-X)

delogu_df <- read.csv(file.path("results", "delogu_semantic_association.csv")) |>
    left_join(lp_df) |>
    left_join(mean_amplitude_df) |>
    mutate("cond" = factor(Condition,
        levels = c("control", "script-related", "script-unrelated")
    )) |>
    mutate(model = str_replace(model, "/", "_")) |>
    mutate(full_implementation = paste(implementation, model, sep = "_"))

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

# sem + plaus
sem_plaus_formula <- bf(
    n400 ~ s_sem + s_plaus +
        (s_sem + s_plaus || Subject) +
        (s_sem + s_plaus || ItemNum)
)

all_implementations <- delogu_df |>
    pull(full_implementation) |>
    unique()

for (impl in all_implementations) {
    print(impl)
    data <- delogu_df |>
        filter(
            full_implementation == impl
        ) |>
        mutate(
            s_sem = scale(semantic_association),
            s_plaus = scale(Plaus)
        )

    fit_sem <- brm(sem_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("delogu_", impl))
    )

    fit_sem_lp <- brm(sem_lp_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("delogu_lp_", impl))
    )

    fit_sem_plaus <- brm(sem_plaus_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("delogu_plaus_", impl))
    )
}

# assoc + plaus
assoc_plaus_formula <- bf(
    n400 ~ s_assoc + s_plaus +
        (s_assoc + s_plaus || Subject) +
        (s_assoc + s_plaus || ItemNum)
)

# assoc + lp
assoc_lp_formula <- bf(
    n400 ~ s_assoc + s_lp +
        (s_assoc + s_lp || Subject) +
        (s_assoc + s_lp || ItemNum)
)

data <- delogu_df |>
    select(Assoc, Plaus, s_lp, Subject, ItemNum, n400) |>
    distinct() |>
    mutate(
        s_plaus = scale(Plaus),
        s_assoc = scale(Assoc)
    )

fit_assoc_plaus <- brm(assoc_plaus_formula,
    family = gaussian(),
    prior = erp_priors,
    data = data,
    chains = 4,
    control = list(adapt_delta = 0.9999),
    seed = 246,
    file = file.path(out_folder, "delogu_assoc_plaus")
)

fit_assoc_lp <- brm(assoc_lp_formula,
    family = gaussian(),
    prior = erp_priors,
    data = data,
    chains = 4,
    control = list(adapt_delta = 0.9999),
    seed = 246,
    file = file.path(out_folder, "delogu_assoc_lp")
)

### Aurnhammer et al. (2019) ###
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
    mutate(full_implementation = paste(implementation, model, sep = "_"))

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


### Michaelov et al. (2024) ###
# read data
n400_df <- read.csv(file.path("data", "michaelov_2024.csv")) |>
    group_by(across(c(-Electrode, -N400))) |>
    summarize(
        "n400" = mean(N400)
    ) |>
    ungroup()

lp_df <- read.csv(file.path("results", "michaelov_log_probability.csv")) |>
    select(-X)

michaelov_df <- read.csv(file.path("results", "michaelov_semantic_association.csv")) |>
    select(-X) |>
    left_join(n400_df) |>
    left_join(lp_df) |>
    mutate(model = str_replace(model, "/", "_")) |>
    mutate(
        full_implementation = paste(implementation, model, sep = "_")
    )

# model formula
# sem
sem_formula <- bf(
    n400 ~ s_sem +
        (s_sem || Subject) +
        (s_sem || ContextCode)
)

# sem + lp
sem_lp_formula <- bf(
    n400 ~ s_sem + s_lp +
        (s_sem + s_lp || Subject) +
        (s_sem + s_lp || ContextCode)
)

all_implementations <- michaelov_df |>
    filter(!implementation %in% c("BERTWE", "Mamba")) |>
    pull(full_implementation) |>
    unique()

for (impl in all_implementations) {
    print(impl)
    data <- michaelov_df |>
        filter(
            full_implementation == impl
        ) |>
        mutate(
            s_sem = scale(semantic_association)
        )

    fit_sem <- brm(sem_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("michaelov_", impl))
    )

    fit_sem_lp <- brm(sem_lp_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0("michaelov_lp_", impl))
    )
}
