### Bayesian hierarchical regression models ###

library(tidytable)
library(brms)
library(stringr)
library(argparse)

setwd("experiment2")

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

## Specify dependent variables using argparse
parser <- ArgumentParser(description = "Run brms models")
parser$add_argument("--dataset",
    type = "character",
    nargs = "+",
    default = c("tanner", "ucl"),
    help = "Specify dataset (ucl or tanner)"
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

# model formulas
sem_formula <- bf(
    n400 ~ s_sem +
        (s_sem || subject) +
        (s_sem || id) +
        (s_sem || word)
)

sem_lp_formula <- bf(
    n400 ~ s_sem + s_lp +
        (s_sem + s_lp || subject) +
        (s_sem + s_lp || id) +
        (s_sem + s_lp || word)
)

interaction_formula <- bf(
    n400 ~ s_lp * s_sem +
        (s_lp * s_sem || subject) +
        (s_lp * s_sem || id) +
        (s_lp * s_sem || word)
)

if ("tanner" %in% dataset) {
    print("Dataset: Tanner")
    # load data
    tanner_sem <- read.csv(
        file.path("results", "tanner_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    tanner_df <- read.csv(file.path("data", "Tanner", "mean_amplitude.csv")) |>
        mutate(context = ifelse(is.na(context), "", context)) |>
        left_join(tanner_sem) |>
        filter(Acceptability == "Gram") |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(word)) |>
        # only use complete cases across implementations of sem
        group_by(id, word_n) |>
        filter(all(!is.na(semantic_association))) |>
        ungroup() |>
        arrange(subject, id, word_n)

    # run models
    implementations <- tanner_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- tanner_df |>
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
            file = file.path(out_folder, paste0("tanner_", imp_id))
        )

        # n400 ~ sem + lp
        m_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tanner_lp_", imp_id))
        )

        # n400 ~ sem * lp
        m_sem_lp <- brm(interaction_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tanner_interaction_", imp_id))
        )
    }
}

if ("ucl" %in% dataset) {
    print("Dataset: UCL")
    # load data
    ucl_sem <- read.csv(
        file.path("results", "ucl_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    ucl_df <- read.csv(file.path("data", "UCL", "mean_amplitude.csv")) |>
        left_join(ucl_sem) |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(word)) |>
        rename("n400" = "N400") |>
        # only use complete cases across implementations of sem
        group_by(id, word_n) |>
        filter(all(!is.na(semantic_association))) |>
        ungroup() |>
        arrange(subject, id, word_n)

    # run models
    implementations <- ucl_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- ucl_df |>
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
            file = file.path(out_folder, paste0("ucl_", imp_id))
        )

        # n400 ~ sem + lp
        m_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("ucl_lp_", imp_id))
        )

        # n400 ~ sem * lp
        m_sem_lp <- brm(interaction_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("ucl_interaction_", imp_id))
        )
    }
}
