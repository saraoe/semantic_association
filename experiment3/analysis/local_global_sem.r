### Model local and global semantic association jointly ###

library(tidytable)
library(brms)
library(stringr)

setwd("experiment3")

options(mc.cores = parallel::detectCores())
options(brms.backend = "cmdstan")

# folders
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
    # only use complete cases across implementations of sem
    group_by(article_n, word_n) |>
    filter(all(!is.na(semantic_association))) |>
    ungroup()


# Run models: global = SE, All
# model 1: local = SE, Sentence(N=1) (same SE model as global)
# model 2: local = CWE, Sentence(N=1)

model_formula <- bf(
    n400 ~ s_lp + local_sem + global_sem +
        (s_lp + local_sem + global_sem || subject) +
        (s_lp + local_sem + global_sem || article_n) +
        (s_lp + local_sem + global_sem || word)
)

se_models <- derco_df |>
    filter(implementation == "SE_all") |>
    pull(model) |>
    unique()
cwe_model <- "word2vec-google-news-300"

for (se_model in se_models) {
    print(paste("SE model =", se_model))
    # model 1
    print("Running model 1")
    se_model_imp <- str_replace(se_model, "/", "_")
    local_se_imp <- paste0("SE_sentences1_", se_model_imp)
    global_se_imp <- paste0("SE_all_", se_model_imp)

    data <- derco_df |>
        filter(
            (implementation == "SE_all" |
                implementation == "SE_sentences1")
        ) |>
        filter(model == se_model) |>
        select(-model, -implementation) |>
        pivot_wider(
            names_from = implementation_id,
            values_from = semantic_association
        ) |>
        rename(
            "local_sem" = local_se_imp,
            "global_sem" = global_se_imp
        ) |>
        mutate(
            across(all_of(c("local_sem", "global_sem")), ~ as.numeric(scale(.)))
        ) |>
        arrange(subject, article_n, word_n)

    m <- brm(model_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(
            out_folder,
            paste0("derco_localSE_globalSE_", se_model_imp, ".rds")
        )
    )

    # model 2
    print("Running model 2")
    print(paste(">> with CWE model =", cwe_model))
    rm(data)
    cwe_model_imp <- str_replace(cwe_model, "/", "_")
    local_cwe_imp <- paste0("CWE_sentences1_", cwe_model_imp)

    data <- derco_df |>
        filter(
            (implementation == "SE_all" |
                implementation == "CWE_sentences1")
        ) |>
        filter(model %in% c(se_model, cwe_model)) |>
        select(-model, -implementation) |>
        pivot_wider(
            names_from = implementation_id,
            values_from = semantic_association
        ) |>
        rename(
            "local_sem" = local_cwe_imp,
            "global_sem" = global_se_imp
        ) |>
        mutate(
            across(all_of(c("local_sem", "global_sem")), ~ as.numeric(scale(.)))
        ) |>
        arrange(subject, article_n, word_n)

    m <- brm(model_formula,
        family = gaussian(),
        prior = erp_priors,
        data = data,
        chains = 4,
        control = list(adapt_delta = 0.9999),
        seed = 246,
        file = file.path(
            out_folder,
            paste0("derco_localCWE_globalSE_", model_imp, ".rds")
        )
    )
    rm(data)
}
