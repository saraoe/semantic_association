# Model Comparision

library(tidytable)
library(tibble)
library(stringr)
library(brms)
library(loo)
library(ggplot2)

options(mc.cores = parallel::detectCores())

dep_vars <- c("rt", "n400")
models_path = file.path("analysis", "brms_models")

for (dep_var in dep_vars){
    print(paste("Running baseline for", dep_var))
    # baseline model
    baseline_m <- readRDS(file.path(models_path, paste0(dep_var, "_baseline.rds")))
    loo_baseline <- loo(baseline_m)
    print("Pareto k table:")
    print(pareto_k_table(loo_baseline))

    # compare
    sem_model_names <- list.files(models_path,
        full.names = FALSE,
        pattern = paste0(dep_var, "_semantic_association_.*\\.rds$")
    )

    for (model_name in sem_model_names){
        print(paste("Comparing baseline to", model_name))
        sem_m <- readRDS(file.path(models_path, model_name))

        loo_sem <- loo(sem_m)
        print("Pareto k table (sem model):")
        print(pareto_k_table(loo_sem))

        comparision <- loo_compare(loo_baseline, loo_sem)
        print("comparison:")
        print(comparision)

        # save df
        comp_df <- comparision |>
            as.data.frame() |>
            tibble::rownames_to_column("model") |>
            mutate(
                "implementation" = str_extract(model_name, paste0("(?<=_semantic_association_).*(?=\\.rds)")),
                "dep_var" = dep_var
            )
        
        if (exists("out_df")) {
            out_df <- rbind(out_df, comp_df)
        } else {
            out_df <- comp_df
        }
    }
}

write.csv(out_df, file.path("results", "model_comparison.csv"))

