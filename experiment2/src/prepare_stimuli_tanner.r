# Extract stimuli from RT

library(tidytable)
library(purrr)
setwd("experiment2")
data_folder <- file.path("data", "Tanner")

rt_df <- csvs <- list.files(file.path(data_folder, "behavioral"), pattern = "csv$", full.names = TRUE) |>
    lapply(fread) |>
    bind_rows() |>
    # based on the original analysis
    rename_with(~ stringr::str_replace_all(., "-", ".")) |>
    select(
        trial = Trial,
        subject = SubjectID,
        item = TrialTable.SentenceNumber,
        experiment = TrialTable.Experiment,
        Acceptability = TrialTable.TotalWord,
        VerbType = TrialTable.VerbType,
        LexVerb = TrialTable.Antecedent,
        Gender = TrialTable.AntecedentGender,
        AntecedentPosition = TrialTable.AntecedentPosition,
        Condition = TrialTable.Condition,
        AuxVerb = TrialTable.AuxVerb,
        Antecedent = TrialTable.LexVerb,
        CorrResponse = TrialTable.CorrResp,
        CritSemanticword = TrialTable.CritSemanticWord,
        Critword_Position = TrialTable.CritWordPosition,
        list = TrialTable.List,
        SentenceLength = TrialTable.Acceptability,
        ResponseAccuracy = Response.Keyboard.IsCorrect,
        Response_RT = Response.Keyboard.ResponseTime,
        word_1 = TrialTable.W1,
        word_2 = TrialTable.W2,
        word_3 = TrialTable.W3,
        word_4 = TrialTable.W4,
        word_5 = TrialTable.W5,
        word_6 = TrialTable.W6,
        word_7 = TrialTable.W7,
        word_8 = TrialTable.W8,
        word_9 = TrialTable.W9,
        word_10 = TrialTable.W10,
        word_11 = TrialTable.W11,
        word_12 = TrialTable.W12,
        word_13 = TrialTable.W13,
        word_14 = TrialTable.W14,
        word_15 = TrialTable.W15,
        word_16 = TrialTable.W16,
        rt_1 = Word1.Keyboard.ResponseTime,
        rt_2 = Word2.Keyboard.ResponseTime,
        rt_3 = Word3.Keyboard.ResponseTime,
        rt_4 = Word4.Keyboard.ResponseTime,
        rt_5 = Word5.Keyboard.ResponseTime,
        rt_6 = Word6.Keyboard.ResponseTime,
        rt_7 = Word7.Keyboard.ResponseTime,
        rt_8 = Word8.Keyboard.ResponseTime,
        rt_9 = Word9.Keyboard.ResponseTime,
        rt_10 = Word10.Keyboard.ResponseTime,
        rt_11 = Word11.Keyboard.ResponseTime,
        rt_12 = Word12.Keyboard.ResponseTime,
        rt_13 = Word13.Keyboard.ResponseTime,
        rt_14 = Word14.Keyboard.ResponseTime,
        rt_15 = Word15.Keyboard.ResponseTime,
        rt_16 = Word16.Keyboard.ResponseTime
    ) |>
    pivot_longer(
        cols = c(starts_with("word_"), starts_with("rt_")),
        names_to = c(".value", "word_n"),
        names_pattern = "(.+)_(\\d+)"
    ) |>
    mutate(word_n = word_n |> as.numeric()) |>
    arrange(subject, item, trial, word_n) |>
    filter(word != "X")

stim <- rt_df |>
    distinct(item, experiment, word_n, word, Acceptability, Condition) |>
    mutate(
        id = as.factor(item):as.factor(experiment):as.factor(Acceptability):as.factor(Condition) |>
            as.numeric()
    )

stim <- stim |>
    group_by(id) |>
    mutate(context = accumulate(word, ~ paste(.x, .y))) |>
    mutate(context = lag(context)) |>
    ungroup() |>
    mutate(target = word)

write.csv(stim, file.path(data_folder, "stim.csv"))
