# Regression models: Extending the modeling of the data from experiment 2

library(tidytable)
library(brms)
library(stringr)
library(argparse)

setwd("extra_experiments")

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

## Specify dependent variables using argparse
parser <- ArgumentParser(description = "Run brms models")
parser$add_argument("--dataset",
    type = "character",
    nargs = "+",
    default = c("derco", "tanner", "ucl"),
    help = "Specify dataset"
)

args <- parser$parse_args()
dataset <- args$dataset

print(paste(
    "Running models for dataset: ",
    dataset,
    sep = ""
))

# folders
out_folder <- file.path("analysis", "brms_models")
if (!dir.exists(out_folder)) {
    dir.create(out_folder)
}
exp2_folder <- file.path("..", "experiment2")
exp3_folder <- file.path("..", "experiment3")

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
erp_priors_no_intercept <- erp_priors[2:4, ]

# content words pos tags
content_pos <- c("NOUN", "VERB", "ADJ", "ADV")

if ("tanner" %in% dataset) {
    print("Running dataset tanner")
    # load data
    tanner_sem <- read.csv(
        file.path("results", "tanner_qwen_instructions_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste("instruction", model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    tanner_df <- read.csv(file.path(exp2_folder, "data", "Tanner", "mean_amplitude.csv")) |>
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

    # model formula
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

    # run models
    implementations <- tanner_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- tanner_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))

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
    print("Running dataset ucl")
    # load data
    ucl_sem <- read.csv(
        file.path("results", "ucl_qwen_instructions_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste("instruction", model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    ucl_df <- read.csv(file.path(exp2_folder, "data", "UCL", "mean_amplitude.csv")) |>
        left_join(ucl_sem) |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(word)) |>
        rename("n400" = "N400") |>
        # only use complete cases across implementations of sem
        group_by(id, word_n) |>
        filter(all(!is.na(semantic_association))) |>
        ungroup() |>
        arrange(subject, id, word_n)

    # model formula
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

    # run models
    implementations <- ucl_df |>
        pull(implementation_id) |>
        unique()
    for (imp_id in implementations) {
        print(paste("Running implementation", imp_id))
        data <- ucl_df |>
            filter(implementation_id == imp_id) |>
            mutate(s_sem = scale(semantic_association))

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

if ("derco" %in% dataset) {
    print("Running dataset derco")
    # load data
    derco_sem <- read.csv(
        file.path("results", "derco_qwen_instructions_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste("instruction", model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    derco_df <- read.csv(
        file.path(exp3_folder, "data", "DERCo", "mean_amplitude.csv")
    ) |>
        left_join(derco_sem) |>
        filter(pos %in% content_pos) |>
        mutate(word = clean_word(target)) |>
        # only use complete cases across implementations of sem
        group_by(article_n, word_n) |>
        filter(all(!is.na(semantic_association))) |>
        ungroup() |>
        arrange(subject, article_n, word_n)

    # model formula
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

        # n400 ~ sem + lp
        m_sem_lp <- brm(sem_lp_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
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
}