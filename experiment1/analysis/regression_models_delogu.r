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

# extra priors for Savage-Dickey BF
print("Models with extra priors")
prior_sem_sd <- c(1, 2)
for (impl in all_implementations) {
    data <- delogu_df |>
        filter(
            full_implementation == impl
        ) |>
        mutate(
            s_sem = scale(semantic_association)
        )
    for (prior_sd in prior_sem_sd) {
        prior_sem <- set_prior(
            sprintf("normal(0, %s)", prior_sd),
            class = "b",
            coef = "s_sem"
        )
        priors <- c(erp_priors, prior_sem)

        prior_suffix <- paste0("_bsemprior", prior_sd)
        print(paste0(impl, prior_suffix))

        fit_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("delogu_lp_", impl, prior_suffix))
        )
    }
}

print("Human-rated association")
data <- delogu_df |>
    select(Assoc, Plaus, s_lp, Subject, ItemNum, n400) |>
    distinct() |>
    mutate(
        s_plaus = scale(Plaus),
        s_assoc = scale(Assoc)
    )

for (prior_sd in prior_sem_sd) {
        prior_sem <- set_prior(
            sprintf("normal(0, %s)", prior_sd),
            class = "b",
            coef = "s_assoc"
        )
        priors <- c(erp_priors, prior_sem)

        prior_suffix <- paste0("_bsemprior", prior_sd)
        print(paste0("assoc_lp", prior_suffix))

        fit_assoc_lp <- brm(assoc_lp_formula,
            family = gaussian(),
            prior = priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("delogu_assoc_lp", prior_suffix))
        )
    }

# extra samples for bridge sampling
print("Models with extra iterations (for bridge sampling)")
implementations <- c("SE_aari1995_German_Semantic_STS_V2") # embedding-based implementations
n_samples <- 20000
for (impl in implementations) {
    data <- delogu_df |>
        filter(
            full_implementation == impl
        ) |>
        mutate(
            s_sem = scale(semantic_association)
        )
    print(paste0(impl, "_samples", n_samples))

    fit_sem_lp <- brm(sem_lp_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        warmup = 2000,
        iter = n_samples,
        control = list(adapt_delta = 0.9999),
        save_pars = save_pars(all = TRUE),
        seed = 246,
        file = file.path(out_folder, paste0("delogu_lp_", impl, "_samples", n_samples))
    )

    for (prior_sd in prior_sem_sd) {
        prior_sem <- set_prior(
            sprintf("normal(0, %s)", prior_sd),
            class = "b",
            coef = "s_sem"
        )
        priors <- c(erp_priors, prior_sem)

        prior_suffix <- paste0("_bsemprior", prior_sd)
        print(paste0(impl, "_samples", n_samples, prior_suffix))

        fit_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = priors,
            data = data,
            chains = 4,
            warmup = 2000,
            iter = n_samples,
            control = list(adapt_delta = 0.9999),
            save_pars = save_pars(all = TRUE),
            seed = 246,
            file = file.path(out_folder, paste0("delogu_lp_", impl, "_samples", n_samples, prior_suffix))
        )
    }
}

print("Human-rated association")
data <- delogu_df |>
    select(Assoc, Plaus, s_lp, Subject, ItemNum, n400) |>
    distinct() |>
    mutate(
        s_plaus = scale(Plaus),
        s_assoc = scale(Assoc)
    )

print(paste0("assoc_lp_samples", n_samples))

fit_assoc_lp <- brm(assoc_lp_formula,
    family = gaussian(),
    prior = erp_priors,
    data = data,
    chains = 4,
    warmup = 2000,
    iter = n_samples,
    control = list(adapt_delta = 0.9999),
    save_pars = save_pars(all = TRUE),
    seed = 246,
    file = file.path(out_folder, paste0("delogu_assoc_lp_samples", n_samples))
)

for (prior_sd in prior_sem_sd) {
    prior_sem <- set_prior(
        sprintf("normal(0, %s)", prior_sd),
        class = "b",
        coef = "s_assoc"
    )
    priors <- c(erp_priors, prior_sem)

    prior_suffix <- paste0("_bsemprior", prior_sd)
    print(paste0("assoc_lp_samples", n_samples, prior_suffix))

    fit_sem_lp <- brm(assoc_lp_formula,
        family = gaussian(),
        prior = priors,
        data = data,
        chains = 4,
        warmup = 2000,
        iter = n_samples,
        control = list(adapt_delta = 0.9999),
        save_pars = save_pars(all = TRUE),
        seed = 246,
        file = file.path(out_folder, paste0("delogu_assoc_lp_samples", n_samples, prior_suffix))
    )
}
