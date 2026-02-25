### Bayesian hierarchical regression models ###

library(tidytable)
library(brms)
library(stringr)
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
)
tint_df <- read.csv(file.path("data", "tint.csv")) |>
    select(-X) |>
    left_join(sem_df) |>
    filter(pos %in% c("NOUN", "VERB", "ADJ", "ADV")) |> # model only content words
    mutate(across(
        starts_with("semantic_association"),
        ~ scale(.) # scale sem_vars
    )) |>
    # include only complete cases
    select(
        starts_with("semantic_association"), s_lp,
        participant_number, word, document_id,
        n400, p600, rt
    ) |>
    drop_na()

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
run_baseline_model <- function(dep_var, priors) {
    data <- tint_df |>
        rename("dep_var" = dep_var)

    if (dep_var %in% c("n400", "p600")) {
        family <- gaussian()
    } else if (dep_var == "rt") {
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

run_sem_model <- function(dep_var, sem_var, priors, suffix = "") {
    data <- tint_df |>
        rename(
            "dep_var" = dep_var,
            "s_sem" = sem_var
        )

    if (dep_var %in% c("n400", "p600")) {
        family <- gaussian()
    } else if (dep_var == "rt") {
        family <- lognormal()
    }

    m <- brm(sem_formula,
        family = family,
        prior = priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0(dep_var, "_", sem_var, suffix))
    )
    return(m)
}

run_sem_model_more_iter <- function(dep_var, sem_var, priors, suffix = "") {
    data <- tint_df |>
        rename(
            "dep_var" = dep_var,
            "s_sem" = sem_var
        )

    if (dep_var %in% c("n400", "p600")) {
        family <- gaussian()
    } else if (dep_var == "rt") {
        family <- lognormal()
    }

    m <- brm(sem_formula,
        family = family,
        prior = priors,
        data = data,
        chains = 4,
        threads = threading(2),
        iter = 3000,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(out_folder, paste0(dep_var, "_", sem_var, suffix))
    )
    return(m)
}

run_sem_only_model <- function(dep_var, sem_var, priors) {
    data <- tint_df |>
        rename(
            "dep_var" = dep_var,
            "s_sem" = sem_var
        )

    if (dep_var %in% c("n400", "p600")) {
        family <- gaussian()
    } else if (dep_var == "rt") {
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
    if (dep_var %in% c("n400", "p600")) {
        priors <- erp_priors
    } else if (dep_var == "rt") {
        priors <- rt_priors
    }
    print(paste("Running baseline model with", dep_var))
    run_baseline_model(dep_var, priors)

    for (sem_var in sem_vars) {
        print(paste("Running model with", sem_var))
        run_sem_model(dep_var, sem_var, priors)

        print(paste("Running model with only", sem_var))
        run_sem_only_model(dep_var, sem_var, priors)
    }
}

# extra priors for Savage-Dickey BF
prior_sem_sd <- list("rt" = c(.05, .5), "n400" = c(1, 2))
more_iter<- c(
    "rt_semantic_association_WordEmbedding_bsemprior05",
    "rt_semantic_association_WordEmbedding_bsemprior5",
    "rt_semantic_association_WordEmbeddingContentWord_nSentences1_bsemprior05",
    "rt_semantic_association_WordEmbeddingContentWord_nSentences1_bsemprior5",
    "n400_semantic_association_SentenceEmbedding_bsemprior2",
    "n400_semantic_association_WordEmbeddingContentWord_bsemprior1"
)
for (dep_var in dep_vars) {
    print(paste("Running extra prior models for", dep_var))
    for (sem_var in sem_vars) {
        print(paste("Running model(s) with", sem_var))
        for (prior_sd in prior_sem_sd[[dep_var]]) {
            # define prior
            prior_sem <- set_prior(
                sprintf("normal(0, %s)", prior_sd),
                class = "b",
                coef = "s_sem"
            )
            if (dep_var == "rt") {
                priors <- c(rt_priors, prior_sem)
            } else if (dep_var %in% c("n400", "p600")) {
                priors <- c(erp_priors, prior_sem)
            }

            prior_suffix <- paste0("_bsemprior", str_replace(as.character(prior_sd), "0.", ""))
            model_name <- paste0(dep_var, "_", sem_var, prior_suffix)

            # run model
            if (model_name %in% more_iter) {
                run_sem_model_more_iter(dep_var, sem_var, priors, suffix = prior_suffix)
            } else {
                run_sem_model(dep_var, sem_var, priors, suffix = prior_suffix)
            }
        }
    }
}
