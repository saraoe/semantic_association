# Regression model including both WE and SE
# Only on DERCo

library(tidytable)
library(brms)
library(stringr)

setwd("experiment3")

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

# models (NB: Must be a WE and an SE implementation!)
model_ids <- c(
    "SE_BAAI_bge-m3",
    "WE_enwiki_20180420_300d"
)

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

# content words pos tags
content_pos <- c("NOUN", "VERB", "ADJ", "ADV")

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
    mutate(word = clean_word(target))

data <- derco_df |>
    filter(implementation_id %in% model_ids) |>
    select(-model, -implementation_id) |>
    pivot_wider(
        names_from = implementation,
        values_from = semantic_association
    ) |>
    mutate(across(all_of(c("WE", "SE")), ~ as.numeric(scale(.))))


# model formula
model_formula <- bf(
    n400 ~ WE + SE + s_lp +
        (WE + SE + s_lp || subject) +
        (WE + SE + s_lp || article_n) +
        (WE + SE + s_lp || word)
)

m <- brm(model_formula,
    family = gaussian(),
    prior = erp_priors,
    data = data,
    chains = 4,
    control = list(adapt_delta = 0.9999),
    seed = 246,
    file = file.path(
        out_folder,
        paste0("derco_both_", model_ids[1], "_", model_ids[2], ".rds")
    )
)
print(m)
