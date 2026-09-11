### Regression models:  Models N400 from Delogu et al., 2019 ###

library(tidytable)
library(stringr)
library(lmerTest)
library(brms)

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

setwd("experiment1")

brms_out_folder <- file.path("analysis", "brms_models")
if (!dir.exists(brms_out_folder)) {
    dir.create(brms_out_folder)
}

# read data
erp_df <- read.csv(file.path("data", "Delogu", "dbc_data.csv"))

n400_chs <- c(
    "Cz", "Pz", "C4", "CP6", "P4", "P3",
    "CP5", "C3", "P8", "P7"
)
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
    group_by(id_cols) |>
    summarize(n400 = mean(amplitude))

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

# priors
erp_priors <- c(
    prior(normal(0, 20), class = Intercept),
    prior(normal(0, 10), class = b),
    prior(normal(0, 10), class = sigma),
    prior(normal(0, 10), class = sd)
)

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

# sem * lp
interaction_formula <- bf(
    n400 ~ s_sem * s_lp +
        (s_sem * s_lp || Subject) +
        (s_sem * s_lp || ItemNum)
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
            s_sem = scale(semantic_association)
        )

    fit_sem <- brm(sem_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(brms_out_folder, paste0("delogu_", impl))
    )

    fit_sem_lp <- brm(sem_lp_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(brms_out_folder, paste0("delogu_lp_", impl))
    )
}
