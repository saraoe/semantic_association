# Model diagnostics from Bayesian models fitted with brms

library(tidytable)
library(brms)


number_divergent_transitions <- function(fit) {
    np <- nuts_params(fit)
    # extract the number of divergence transitions
    sum(subset(np, Parameter == "divergent__")$Value)
}

# max r_hat and min ESS (Bulk and tail)
get_diagnostic_from_summary <- function(summary, diag) {
    c(
        summary$fixed[, diag],
        summary$random$document_id[, diag],
        summary$random$participant_number[, diag],
        summary$random$word[, diag]
    )
}

diagnostics_rhat_ess <- function(fit) {
    # Extract diagnostics from the summary
    model_summary <- summary(fit)
    rhats <- get_diagnostic_from_summary(model_summary, "Rhat")
    ess_bulk <- get_diagnostic_from_summary(model_summary, "Bulk_ESS")
    ess_tail <- get_diagnostic_from_summary(model_summary, "Tail_ESS")

    return(data.frame(
        max_rhat = max(rhats),
        min_ess_bulk = min(ess_bulk),
        min_ess_tail = min(ess_tail),
        avg_ess = mean(c(ess_bulk, ess_tail))
    ))
}
