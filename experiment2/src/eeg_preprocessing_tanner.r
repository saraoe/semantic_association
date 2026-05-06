# Preprocessing of EEG data in SPR condition

### Libraries
library(eeguana)
library(ggplot2)
library(tidytable)

setwd("experiment2")

data_path <- file.path("data", "Tanner")
eeg_files <- list.files(file.path(data_path, "eeg"), full.names = TRUE, pattern = "_AGLA_s1.vhdr")
stim <- read.csv(file.path(data_path, "stim.csv")) |>
    select(-X)

mean_amplitude_path <- file.path(data_path, "mean_amplitude.csv")

inspect_rejected <- function(epochs, participant_n, rt_df, save_figs = FALSE) {
    reject_eyeblinks <- epochs |>
        eeg_group_by(segment) |>
        events_tbl() |>
        filter(grepl("minmax_threshold=130", .description, fixed = TRUE)) |>
        group_by(.id) |>
        summarize(N = n()) |>
        filter(N >= 2)

    reject_eyemovements <- epochs |>
        eeg_group_by(segment) |>
        events_tbl() |>
        filter(grepl("step_threshold", .description, fixed = TRUE)) |>
        group_by(.id) |>
        summarize(N = n()) |>
        filter(!(.id %in% reject_eyeblinks$.id))

    reject_ptp <- epochs |>
        eeg_group_by(segment) |>
        events_tbl() |>
        filter(grepl("minmax_threshold=150", .description, fixed = TRUE)) |>
        group_by(.id) |>
        summarize(N = n()) |>
        filter(N >= 3 & !(.id %in% c(reject_eyeblinks$.id, reject_eyemovements$.id)))

    n_reject <- nrow(reject_eyeblinks) + nrow(reject_eyemovements) + nrow(reject_ptp)
    print(paste("#Rejected epochs:", n_reject))
    print(paste("%Rejected epochs:", n_reject / nrow(segments_tbl(epochs))))

    epochs <- epochs |>
        eeg_mutate(
            "reject_reason" = ifelse(
                segment %in% reject_eyeblinks$.id, "eyeblink", ifelse(
                    segment %in% reject_eyemovements$.id, "eyemovement", ifelse(
                        segment %in% reject_ptp$.id, "ptp", NA
                    )
                )
            )
        )

    if (save_figs) {
        figs_path <- file.path("figs", "preprocessing")
        dir.create(figs_path, showWarnings = FALSE)

        if (nrow(reject_eyeblinks) > 0) {
            p_artif_eyeblink <- epochs |>
                eeg_filter(reject_reason == "eyeblink") |>
                eeg_select(VEOG, Fp1, Fp2) |>
                ggplot(aes(x = .time, y = .value, color = .key)) +
                geom_line() +
                facet_wrap(~segment) +
                theme(axis.text.x = element_text(angle = 90)) +
                theme_eeguana()
            ggsave(
                file.path(figs_path, paste(participant_n, "_artif_eyeblink.png", sep = "")),
                plot = p_artif_eyeblink
            )
        }

        if (nrow(reject_eyemovements) > 0) {
            p_artif_eyemovement <- epochs |>
                eeg_filter(reject_reason == "eyemovement") |>
                eeg_select(HEOG) |>
                ggplot(aes(x = .time, y = .value, color = .key)) +
                geom_line() +
                facet_wrap(~segment) +
                theme(axis.text.x = element_text(angle = 90)) +
                theme_eeguana()
            ggsave(
                file.path(figs_path, paste(participant_n, "_artif_eyemovement.png", sep = "")),
                plot = p_artif_eyemovement
            )
        }

        if (nrow(reject_ptp) > 0) {
            p_artif_ptp <- epochs |>
                eeg_filter(reject_reason == "ptp") |>
                eeg_select(-HEOG, -VEOG) |>
                ggplot(aes(x = .time, y = .value, color = .key)) +
                geom_line() +
                facet_wrap(~segment) +
                theme(axis.text.x = element_text(angle = 90)) +
                theme_eeguana()
            ggsave(
                file.path(figs_path, paste(participant_n, "_artif_ptp.png", sep = "")),
                plot = p_artif_ptp
            )
        }
    }

    rt_df <- rt_df |>
        mutate(
            "reject_reason" = ifelse(
                segment %in% reject_eyeblinks$.id, "eyeblink", ifelse(
                    segment %in% reject_eyemovements$.id, "eyemovement", ifelse(
                        segment %in% reject_ptp$.id, "ptp", NA
                    )
                )
            )
        )
    return(rt_df)
}

cal_mean_amplitude <- function(epochs, chs, time_from, time_to, time_unit) {
    amplitude_mean <- epochs |>
        eeg_filter(between(as_time(.sample, .unit = time_unit), time_from, time_to)) |>
        eeg_group_by(segment, .sample) |>
        eeg_summarize(
            "mean_amplitude_sample" = chs_mean(across(
                chs
            ), na.rm = TRUE)
        ) |>
        eeg_group_by(segment) |>
        eeg_summarize(
            "mean_amplitude" = mean(mean_amplitude_sample)
        )

    return(amplitude_mean)
}

for (eeg_file in eeg_files) {
    n <- as.numeric(gsub(".*?([0-9]+).*", "\\1", eeg_file))
    print(
        paste("Running participant: ", n, sep = "")
    )

    ### load files
    tryCatch( # try catch in case there is an error in the data
        expr = {
            raw_eeg <- eeguana::read_vhdr(eeg_file)
        },
        error = function(e) {
            print("raw_eeg could not be read")
            print(paste("filename:", eeg_file))
            next
        }
    )
    rt_df <- read.csv(file.path(data_path, "behavioral", paste(n, ".csv", sep = ""))) |>
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
        mutate(
            word_n = word_n |> as.numeric()
        ) |>
        arrange(trial, word_n) |>
        filter(word != "X") |>
        left_join(stim)
    rt_df$segment <- seq_len(nrow(rt_df))
    # skip if there is not an S251 trigger for every word
    if (nrow(rt_df) != nrow(events_tbl(raw_eeg) %>% filter(.description == "S251"))) {
        print("Number of 251 trigger doesn't match number of words!")
        next
    }

    ### preprocessing
    # using the 1020 layout
    eeguana::channels_tbl(raw_eeg) <- select(eeguana::channels_tbl(raw_eeg), .channel) |>
        mutate(
            .channel = ifelse(.channel == "FP1", "Fp1", .channel),
            .channel = ifelse(.channel == "FP2", "Fp2", .channel),
        ) |>
        left_join(eeguana::layout_32_1020)

    # extracting EOG sinal
    raw_eeg <- raw_eeg |>
        eeguana::eeg_rereference(LO2, .ref = "LO1") |>
        eeguana::eeg_rereference(IO1, .ref = "Fp1") |>
        eeguana::eeg_rename(VEOG = IO1, HEOG = LO2) |>
        eeguana::eeg_select(-LO1)

    # re-referencing
    raw_eeg <- eeguana::eeg_rereference(raw_eeg, -VEOG, -HEOG, .ref = "M2")

    # filtering
    raw_filt <- eeguana::eeg_filt_band_pass(raw_eeg, -VEOG, -HEOG, .freq = c(.1, 30))

    # artifact detection
    artif_detect <- raw_filt |>
        eeguana::eeg_artif_minmax(-HEOG, -VEOG,
            .threshold = 150,
            .window = 200,
            .unit = "ms"
        ) |>
        eeguana::eeg_artif_minmax(VEOG, Fp1, Fp2,
            .threshold = 130,
            .window = 200,
            .unit = "ms"
        ) |>
        eeguana::eeg_artif_step(HEOG,
            .threshold = 50,
            .window = 200,
            .unit = "ms"
        )

    ### create epochs
    # trigger word onset
    word_trigger <- events_tbl(artif_detect) |>
        filter(.description == "S251") |>
        mutate(
            "rt_sample" = as_sample_int(rt_df$rt / 1000, .sampling_rate = 1000),
            .initial = .initial - rt_sample,
            .final = .final - rt_sample,
            ".description" = "word"
        ) |>
        select(-rt_sample)

    events_tbl(artif_detect) <- events_tbl(artif_detect) |> rbind(word_trigger)

    # epoching
    epochs <- eeguana::eeg_segment(artif_detect,
        .description == "word",
        .lim = c(-0.2, 1.2)
    )

    rt_df <- inspect_rejected(epochs, participant_n = n, rt_df = rt_df, save_figs = TRUE)

    epochs <- epochs |>
        eeguana::eeg_baseline() |>
        eeg_events_to_NA( # if threhold is exceeded in two channels Fp1, Fp2, and VEOG
            grepl("minmax_threshold=130", .description, fixed = TRUE),
            .drop_events = TRUE, .n_chs = 2
        ) |>
        eeg_events_to_NA( # eyemovements detected in HEOG
            grepl("step_threshold", .description, fixed = TRUE),
            .drop_events = TRUE, .n_chs = 1
        ) |>
        eeg_events_to_NA( # other signal with a ptp above 150
            grepl("minmax_threshold=150", .description, fixed = TRUE),
            .drop_events = TRUE, .n_chs = 3
        ) |>
        eeg_left_join(rt_df, by = "segment")

    # mean amplitudes
    print(">>> mean amplitude")
    n400_chs <- c(
        "Cz", "Pz", "C4", "CP6", "P4", "P3",
        "CP5", "C3", "P8", "P7"
    )
    amplitude_n400 <- cal_mean_amplitude(
        epochs,
        chs = n400_chs,
        time_from = .3,
        time_to = .5,
        time_unit = "s"
    )

    p600_chs <- c(
        "Cz", "CP2", "Pz", "CP1", "C4",
        "CP6", "P4", "P3", "CP5", "C3",
        "T8", "P8", "P7", "T7"
    )
    amplitude_p600 <- cal_mean_amplitude(
        epochs,
        chs = p600_chs,
        time_from = .5,
        time_to = .7,
        time_unit = "s"
    )

    tmp_mean_amplitude <- amplitude_n400 |>
        as_tidytable() |>
        rename(n400 = .value) |>
        select(-.key) |>
        left_join(
            amplitude_p600 |>
                as_tidytable() |>
                rename(p600 = .value) |>
                select(-.key)
        ) |>
        left_join(rt_df, by = "segment")

    write.table(
        tmp_mean_amplitude,
        mean_amplitude_path,
        sep = ",",
        col.names = !file.exists(mean_amplitude_path),
        row.names = FALSE,
        append = TRUE
    )
}
