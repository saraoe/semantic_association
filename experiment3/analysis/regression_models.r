# Regression models: Extending the modeling of the data from experiment 2

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
    default = c("derco", "tanner", "ucl"),
    help = "Specify dataset (derco or tanner)"
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
    print("Dataset: Tanner")
    # load data
    tanner_sem <- read.csv(
        file.path(exp2_folder, "results", "tanner_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
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
    word_position_formula <- bf(
        n400 ~ s_sem + s_lp + word_n +
            (s_sem + s_lp + word_n || subject) +
            (s_sem + s_lp + word_n || id) +
            (s_sem + s_lp + word_n || word)
    )
    pos_formula <- bf(
        n400 ~ -1 + pos + pos:s_sem + pos:s_lp +
            (pos + pos:s_sem + pos:s_lp || subject) +
            (pos + pos:s_sem + pos:s_lp || id) +
            (pos + pos:s_sem + pos:s_lp || word)
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

        # n400 ~ sem + lp + word_n
        m_sem <- brm(word_position_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tanner_wordn_", imp_id))
        )

        # n400 ~ pos:s_sem + pos:s_lp
        m_sem <- brm(pos_formula,
            family = gaussian(),
            prior = erp_priors_no_intercept,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("tanner_pos_", imp_id))
        )
    }
}

if ("ucl" %in% dataset) {
    print("Dataset: UCL")
    # load data
    ucl_sem <- read.csv(
        file.path(exp2_folder, "results", "ucl_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
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
    word_position_formula <- bf(
        n400 ~ s_sem + s_lp + word_n +
            (s_sem + s_lp + word_n || subject) +
            (s_sem + s_lp + word_n || id) +
            (s_sem + s_lp + word_n || word)
    )
    pos_formula <- bf(
        n400 ~ -1 + pos + pos:s_sem + pos:s_lp +
            (pos + pos:s_sem + pos:s_lp || subject) +
            (pos + pos:s_sem + pos:s_lp || id) +
            (pos + pos:s_sem + pos:s_lp || word)
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

        # n400 ~ sem + lp + word_n
        m_sem <- brm(word_position_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("ucl_wordn_", imp_id))
        )

        # n400 ~ pos:s_sem + pos:s_lp
        m_sem <- brm(pos_formula,
            family = gaussian(),
            prior = erp_priors_no_intercept,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("ucl_pos_", imp_id))
        )
    }
}


if ("derco" %in% dataset) {
    # load data
    derco_sem <- read.csv(
        file.path(exp2_folder, "results", "derco_semantic_association.csv")
    ) |>
        select(-X) |>
        mutate(
            implementation_id = paste(implementation, model, sep = "_")
        ) |>
        mutate(implementation_id = str_replace(implementation_id, "/", "_"))
    derco_df <- read.csv(
        file.path(exp2_folder, "data", "DERCo", "mean_amplitude.csv")
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
    word_position_formula <- bf(
        n400 ~ s_sem + s_lp + word_n +
            (s_sem + s_lp + word_n || subject) +
            (s_sem + s_lp + word_n || article_n) +
            (s_sem + s_lp + word_n || word)
    )
    pos_formula <- bf(
        n400 ~ -1 + pos + pos:s_sem + pos:s_lp +
            (pos + pos:s_sem + pos:s_lp || subject) +
            (pos + pos:s_sem + pos:s_lp || article_n) +
            (pos + pos:s_sem + pos:s_lp || word)
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

        # n400 ~ sem + lp + word_n
        m_sem <- brm(word_position_formula,
            family = gaussian(),
            prior = erp_priors,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("derco_wordn_", imp_id))
        )

        # n400 ~ pos:s_sem + pos:s_lp
        m_sem <- brm(pos_formula,
            family = gaussian(),
            prior = erp_priors_no_intercept,
            data = data,
            chains = 4,
            control = list(adapt_delta = 0.9999),
            seed = 246,
            file = file.path(out_folder, paste0("derco_pos_", imp_id))
        )
    }
}
