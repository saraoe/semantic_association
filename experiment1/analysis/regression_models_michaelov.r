### Regression models:  Models N400 from Michaelov et al., 2024 ###

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
