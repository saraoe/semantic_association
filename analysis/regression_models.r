### Bayesian hierarchical regression models ###

library(tidytable)
library(brms)
library(argparse)

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

## Specify dependent variables using argparse
parser <- ArgumentParser(description = "Run brms models")
parser$add_argument("--dep_vars",
    type = "character",
    nargs = "+",
    default = c("rt", "n400", "p600"),
    help = "Specify dependent variables (rt, n400, and p600)"
)

args <- parser$parse_args()
dep_vars <- args$dep_vars

print(paste(
    "Running models for dependent variable: ",
    dep_vars,
    sep = ""
))

# create out folder
out_folder <- file.path("analysis", "brms_models")
if (!dir.exists(out_folder)) {
    dir.create(out_folder)
}

# load data
sem_df <- read.csv(
    file.path("results", "tint_semantic_association.csv")
) |>
    select(-X)
tint_df <- read.csv(file.path("data", "tint.csv")) |>
    select(-X) |>
    left_join(sem_df) |>
    filter(content_word) |> # model only content words
    mutate(across(
        starts_with("semantic_association"),
        ~ scale(.) # scale sem_vars
    ))

# model formulas
baseline_formula <- bf(
    dep_var ~ s_lp +
        (s_lp || participant_number) +
        (s_lp || document_id) +
        (s_lp || word)
)

sem_formula <- bf(
    dep_var ~ s_lp + s_sem +
        (s_lp + s_sem || participant_number) +
        (s_lp + s_sem || document_id) +
        (s_lp + s_sem || word)
)

sem_only_formula <- bf(
    dep_var ~ s_sem +
        (s_sem || participant_number) +
        (s_sem || document_id) +
        (s_sem || word)
)

# priors
rt_priors <- c(
    prior(normal(5.5, 1), class = Intercept),
    prior(normal(0, .1), class = b),
    prior(normal(0, .5), class = sigma),
    prior(normal(0, .5), class = sd)
)

erp_priors <- c(
    prior(normal(0, 20), class = Intercept),
    prior(normal(0, 10), class = b),
    prior(normal(0, 10), class = sigma),
    prior(normal(0, 10), class = sd)
)

# run models
run_baseline_model <- function(dep_var) {
    data <- tint_df |>
        rename("dep_var" = dep_var)

    if (dep_var %in% c("n400", "p600")) {
        priors <- erp_priors
        family <- gaussian()
    } else if (dep_var == "rt") {
        priors <- rt_priors
        family <- lognormal()
    }

    m <- brm(baseline_formula,
        family = family,
        prior = priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0(dep_var, "_baseline"))
    )
    return(m)
}

run_sem_model <- function(dep_var, sem_var) {
    data <- tint_df |>
        rename(
            "dep_var" = dep_var,
            "s_sem" = sem_var
        )

    if (dep_var %in% c("n400", "p600")) {
        priors <- erp_priors
        family <- gaussian()
    } else if (dep_var == "rt") {
        priors <- rt_priors
        family <- lognormal()
    }

    m <- brm(sem_formula,
        family = family,
        prior = priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0(dep_var, "_", sem_var))
    )
    return(m)
}

run_sem_only_model <- function(dep_var, sem_var) {
    data <- tint_df |>
        rename(
            "dep_var" = dep_var,
            "s_sem" = sem_var
        )

    if (dep_var %in% c("n400", "p600")) {
        priors <- erp_priors
        family <- gaussian()
    } else if (dep_var == "rt") {
        priors <- rt_priors
        family <- lognormal()
    }

    m <- brm(sem_only_formula,
        family = family,
        prior = priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0(dep_var, "_only_", sem_var))
    )
    return(m)
}

sem_vars <- tint_df |>
    select(all_of(starts_with("semantic_association"))) |>
    colnames()

for (dep_var in dep_vars) {
    print(paste("Running baseline model with", dep_var))
    run_baseline_model(dep_var)

    for (sem_var in sem_vars) {
        print(paste("Running model with", sem_var))
        run_sem_model(dep_var, sem_var)

        print(paste("Running model with only", sem_var))
        run_sem_only_model(dep_var, sem_var)
    }
}
