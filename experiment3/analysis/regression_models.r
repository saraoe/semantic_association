### Bayesian hierarchical regression models ###

library(tidytable)
library(brms)
library(stringr)
library(argparse)

setwd("experiment3")

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

## Specify dependent variables using argparse
parser <- ArgumentParser(description = "Run brms models")
parser$add_argument("--dataset",
    type = "character",
    nargs = "+",
    default = c("derco", "tint"),
    help = "Specify dataset (derco or tint)"
)

args <- parser$parse_args()
dataset <- args$dataset

print(paste(
    "Running models for dataset: ",
    dataset,
    sep = ""
))

# create out folder
out_folder <- file.path("analysis", "brms_models")
if (!dir.exists(out_folder)) {
    dir.create(out_folder)
}

# function for cleaning word
clean_word <- function(word) {
    word |>
        tolower() |>
        gsub("[[:punct:]]", "", x = _)
}

# prior
erp_priors <- c(
    prior(normal(0, 20), class = Intercept),
    prior(normal(0, 10), class = b),
    prior(normal(0, 10), class = sigma),
    prior(normal(0, 10), class = sd)
)

# content words pos tags
content_pos <- c("NOUN", "VERB", "ADJ", "ADV")

# models that need larger adapt_delta
increase_adapt_delta <- list(
    "derco" = c("WE_sentences1_word2vec-google-news-300"),
    "tint" = c()
)

if ("derco" %in% dataset) {
    # load data
    derco_sem <- read.csv(
        file.path("results", "derco_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    derco_df <- read.csv(
        file.path("data", "DERCo", "mean_amplitude.csv")
    ) |>
        left_join(derco_sem) |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(target)) |>
        arrange(subject, article_n, word_n)

    # model formula
    sem_formula <- bf(
        n400 ~ s_sem +
            (s_sem || subject) +
            (s_sem || article_n) +
            (s_sem || word)
    )

    sem_lp_formula <- bf(
        n400 ~ s_sem + s_lp +
            (s_sem + s_lp || subject) +
            (s_sem + s_lp || article_n) +
            (s_sem + s_lp || word)
    )

    interaction_formula <- bf(
        n400 ~ s_lp * s_sem +
            (s_lp * s_sem || subject) +
            (s_lp * s_sem || article_n) +
            (s_lp * s_sem || word)
    )

    # run models
    implementations <- derco_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- derco_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))

        # only word for lp models
        if (imp_id %in% increase_adapt_delta$derco) {
            ad <- 0.99999
        } else {
            ad <- 0.9999
        }

        # n400 ~ sem
        m_sem <- brm(sem_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("derco_", imp_id))
        )

        # n400 ~ sem + lp
        m_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = ad),
            seed = 246,
            file = file.path(out_folder, paste0("derco_lp_", imp_id))
        )

        # n400 ~ sem * lp
        m_sem_lp <- brm(interaction_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("derco_interaction_", imp_id))
        )
    }

    # extra priors for Savage-Dickey BF
    print("Models with extra priors")
    prior_sem_sd <- c(1, 2)
    for (imp_id in implementations) {
        data <- derco_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))
        for (prior_sd in prior_sem_sd) {
            prior_sem <- set_prior(
                sprintf("normal(0, %s)", prior_sd),
                class = "b",
                coef = "s_sem"
            )
            priors <- c(erp_priors, prior_sem)

            prior_suffix <- paste0("_bsemprior", prior_sd)
            print(paste0(imp_id, prior_suffix))

            fit_sem_lp <- brm(sem_lp_formula,
                family = gaussian(),
                prior = priors,
                data = data,
                chains = 4,
                control = list(adapt_delta = 0.9999),
                seed = 246,
                file = file.path(out_folder, paste0("derco_lp_", imp_id, prior_suffix))
            )
        }
    }
}

if ("tint" %in% dataset) {
    # load data
    tint_sem <- read.csv(
        file.path("results", "tint_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    tint_df <- read.csv(
        file.path("..", "cmcl26", "data", "tint.csv")
    ) |>
        left_join(tint_sem) |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(target)) |>
        arrange(participant_number, document_id, word_n)

    # model formula
    sem_formula <- bf(
        n400 ~ s_sem +
            (s_sem || participant_number) +
            (s_sem || document_id) +
            (s_sem || word)
    )

    sem_lp_formula <- bf(
        n400 ~ s_sem + s_lp +
            (s_sem + s_lp || participant_number) +
            (s_sem + s_lp || document_id) +
            (s_sem + s_lp || word)
    )

    interaction_formula <- bf(
        n400 ~ s_lp * s_sem +
            (s_lp * s_sem || participant_number) +
            (s_lp * s_sem || document_id) +
            (s_lp * s_sem || word)
    )

    # run models
    implementations <- tint_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- tint_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))

        # n400 ~ sem
        m_sem <- brm(sem_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tint_", imp_id))
        )

        # n400 ~ sem + lp
        m_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tint_lp_", imp_id))
        )

        # n400 ~ sem * lp
        m_sem_lp <- brm(interaction_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tint_interaction_", imp_id))
        )
    }

    # extra priors for Savage-Dickey BF
    print("Models with extra priors")
    prior_sem_sd <- c(1, 2)
    for (imp_id in implementations) {
        data <- tint_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))
        for (prior_sd in prior_sem_sd) {
            prior_sem <- set_prior(
                sprintf("normal(0, %s)", prior_sd),
                class = "b",
                coef = "s_sem"
            )
            priors <- c(erp_priors, prior_sem)

            prior_suffix <- paste0("_bsemprior", prior_sd)
            print(paste0(imp_id, prior_suffix))

            fit_sem_lp <- brm(sem_lp_formula,
                family = gaussian(),
                prior = priors,
                data = data,
                chains = 4,
                control = list(adapt_delta = 0.9999),
                seed = 246,
                file = file.path(out_folder, paste0("tint_lp_", imp_id, prior_suffix))
            )
        }
    }
}
