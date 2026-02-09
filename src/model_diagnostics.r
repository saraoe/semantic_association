# Model diagnostics from Bayesian models fitted with brms

library(tidytable)
library(brms)


number_divergent_transitions <- function(fit) {
    np <- nuts_params(fit)
    # extract the number of divergence transitions
    sum(subset(np, Parameter == "divergent__")$Value)
}

# max r_hat and min ESS (Bulk and tail)
diagnostics_rhat_ess <- function(fit) {
    # Extract diagnostics from the summary
    model_summary <- summary(fit)
    rhats <- model_summary$fixed[, "Rhat"] # for fixed effects
    ess_bulk <- model_summary$fixed[, "Bulk_ESS"]
    ess_tail <- model_summary$fixed[, "Tail_ESS"]

    return(data.frame(
        max_rhat = max(rhats),
        min_ess_bulk = min(ess_bulk),
        min_ess_tail = min(ess_tail),
        avg_ess = mean(c(ess_bulk, ess_tail))
    ))
}
