# Evaluate model comparison with the Savage-Dickey method

library(tidytable)
library(stringr)
library(brms)
library(bayestestR)

options(mc.cores = parallel::detectCores())

models_path <- file.path("analysis", "brms_models")

dep_vars <- c("rt", "n400")
for (dep_var in dep_vars) {
  baseline_m <- readRDS(file.path(models_path, paste0(dep_var, "_baseline.rds")))

  sem_model_names <- list.files(models_path,
    full.names = FALSE,
    pattern = paste0(dep_var, "_semantic_association_.*\\.rds$")
  )

  for (model_name in sem_model_names) {
    sem_m <- readRDS(file.path(models_path, model_name))

    # savage-dickey ratio
    bf <- bayesfactor_parameters(
      sem_m,
      null = 0,
      prior = sem_m,
      parameters = "b_s_sem"
    )

    print(bf)
    # # group-level variance
    # VarCorr(baseline_m)
    # VarCorr(sem_m)

    tmp_df <- data.frame(
      "log_bf" = bf$log_BF,
      "dep_var" = dep_var,
      "implementation" = str_extract(model_name, paste0("(?<=_semantic_association_).*(?=\\.rds)"))
    )

    if (exists("sd_df")) {
      sd_df <- rbind(tmp_df, sd_df)
    } else {
      sd_df <- tmp_df
    }
  }
}

write.csv(sd_df, file.path("results", "savage-dickey.csv"))
