### Extract ERPs from preprocessed EEG from Stone et al. (2023)
# Code is modified from: https://osf.io/fndk5/files/6txbq
# data is downloaded from: https://zenodo.org/records/7334782

library(tidyverse)
library(eeguana)

setwd("experiment2")
data_path <- file.path("data", "stone")

# create list of file names
files <- list.files(
  file.path(data_path, "prepro_eeg"),
  pattern = "_prepro.rds"
)
subjects <- sub("\\_prepro.rds", "", files)

# create empty storage vectors
eegs <- c()
tmp <- c()


# load each subject's preprocessed data
for (i in subjects) {
  message(i)

  # load the preprocessed file
  file <- file.path(data_path, "prepro_eeg", paste0(i, "_prepro.rds"))
  eegble <- readRDS(file)

  # extract target noun only to keep file size down
  eegble <- filter(eegble, trigger %in% c("s13", "s23", "s33", "s43"))

  # create subject id
  eegble <- mutate(eegble, .recording = i)

  # make sure everything is in the current version of eeguana
  eegble <- as_eeg_lst(eegble)

  # give the eegble a subject id
  assign(paste0("eeg", i), eegble)

  # paste eeg id into vector of ids for binding later
  eegs <- c(eegs, paste0("eeg", i))
}

# .......................................................
# Bind everything together
# .......................................................

eeg <- do.call(bind, mget(eegs))

# clear cache
rm(list = c(paste0("eeg", subjects)))
rm(eegble)
gc()


# .......................................................
# Data exclusions
# .......................................................

# subjects with >75% rejected segments
(artifact_excludes <-
  summary(eeg)$segments %>%
  mutate(prop_artifact = (n_incomplete / n_segments) * 100) %>%
  filter(prop_artifact > 75) %>%
  distinct(.recording) %>%
  pull(.recording) %>%
  as.numeric())


# subjects with mismatching log files (should only be 37)
(mismatch_excludes <- filter(eeg$.segments, description.y != trigger) %>%
  distinct(.recording) %>%
  pull() %>%
  as.numeric())


# technical problems (software crashes, etc.)
technical_excludes <- c(8, 15, 37, 40:43)


# .......................................................
# Manual inspection: segments with remaining artifact in averaged data
# .......................................................

# N400 window
(df_N400 <- eeg %>%
  transmute(posterior = chs_mean(Cz, CP1, CP2, P3, Pz, P4, POz, na.rm = TRUE)) %>%
  as_tibble() %>%
  filter(
    # technical issue with recording (software crashes mid-exp, etc.)
    !(.recording %in% technical_excludes),
    # >75% artifact
    !(.recording %in% artifact_excludes),
    # mismatched log files
    !(.recording %in% mismatch_excludes),
    # extract target word
    trigger %in% c("s13", "s23", "s33", "s43"),
    # extract N400 window
    (between(.time, .3, .5)),
    # extract N400 electrodes
    .key == "posterior"
  ) %>%
  group_by(.recording, item, trigger, segment, accuracy, datetime) %>%
  summarise(amplitude = mean(.value, na.rm = FALSE)) %>%
  mutate(window = "N400"))


# PNP window
(df_PNP <- eeg %>%
  transmute(anterior = chs_mean(Fpz, Fp1, Fp2, F3, Fz, F4, na.rm = TRUE)) %>%
  as_tibble() %>%
  filter(
    # technical issue with recording (software crashes mid-exp, etc.)
    !(.recording %in% technical_excludes),
    # >75% artifact
    !(.recording %in% artifact_excludes),
    # mismatched log files
    !(.recording %in% mismatch_excludes),
    # extract target word
    trigger %in% c("s13", "s23", "s33", "s43"),
    # extract PNP window
    (between(.time, .6, 1)),
    # extract PNP electrodes
    .key == "anterior"
  ) %>%
  group_by(.recording, item, trigger, segment, accuracy, datetime) %>%
  summarise(amplitude = mean(.value, na.rm = FALSE)) %>%
  mutate(window = "PNP"))


# P600 window
(df_P600 <- eeg %>%
  transmute(posterior = chs_mean(Cz, CP1, CP2, P3, Pz, P4, POz, na.rm = TRUE)) %>%
  as_tibble() %>%
  filter(
    # technical issue with recording (software crashes mid-exp, etc.)
    !(.recording %in% technical_excludes),
    # >75% artifact
    !(.recording %in% artifact_excludes),
    # mismatched log files
    !(.recording %in% mismatch_excludes),
    # extract target word
    trigger %in% c("s13", "s23", "s33", "s43"),
    # extract N400 window
    (between(.time, .6, 1)),
    # extract N400 electrodes
    .key == "posterior"
  ) %>%
  group_by(.recording, item, trigger, segment, accuracy, datetime) %>%
  summarise(amplitude = mean(.value, na.rm = FALSE)) %>%
  mutate(window = "P600"))



df_erp <- bind_rows(df_N400, df_PNP, df_P600)

rm(df_N400, df_PNP, df_P600)
gc()


# find segments with extreme amplitudes
bad_segments <- filter(df_erp, !(between(amplitude, -50, 50)), is.nan(amplitude) == FALSE)

# extract bad segements from raw eeg
eeg_filtered <- semi_join(eeg, bad_segments, by = c(".recording", "segment"))

# print segment IDs
eeg_filtered$.segments %>%
  group_by(.recording) %>%
  distinct(.id) %>%
  print(n = Inf)

# visualise each ID
eeg_filtered %>%
  # filter(.recording == 10 & .id %in% c(345)) %>% # blink not fully corrected, remove
  # filter(.recording == 20 & .id %in% c(2493)) %>% # frontal contamination, remove Fp1/2/z, F7
  # filter(.recording == 22 & .id %in% c(2873,3034)) %>% # drift, could remove
  # filter(.recording == 23 & .id %in% c(3183,3185,3236,3257,3289)) %>% # bad drift, remove
  # filter(.recording == 24 & .id %in% c(3349,3365,3383,3385)) %>% # bad drift, remove
  # filter(.recording == 24 & .id %in% c(3404,3408,3419,3425)) %>% # bad drift, remove
  # filter(.recording == 24 & .id %in% c(3432,3459,3461,3462)) %>% # bad drift, remove
  # filter(.recording == 24 & .id %in% c(3466,3473,3475,3485)) %>% # bad drift, remove
  # filter(.recording == 24 & .id %in% c(3492,3496,3498,3515,3516,3529)) %>% # bad drift, remove
  # filter(.recording == 25 & .id %in% c(3678,3727,3750)) %>% # frontal contamination, remove
  # filter(.recording == 26 & .id %in% c(3898,3903)) %>% # bad drift, remove
  # filter(.recording == 28 & .id %in% c(4428)) %>% # blink not well corrected, remove
  # filter(.recording == 29 & .id %in% c(4443)) %>% # blink not well corrected, remove
  # filter(.recording == 30 & .id %in% c(4932,5007,5038,5041,5050)) %>% # bad drift, remove
  # filter(.recording == 38 & .id %in% c(6626,6629,6677,6679,6682)) %>% # drift, could remove
  # filter(.recording == 38 & .id %in% c(6683,6684,6689,6718)) %>% # bad drift, remove
  # filter(.recording == 39 & .id %in% c(6877,6930,6964,7053)) %>% # drift, could remove
  # filter(.recording == 48 & .id %in% c(8196)) %>% # fine
  # filter(.recording == 52 & .id %in% c(9375,3429,9462,9510,9546)) %>% # frontal contamination, remove
  # filter(.recording == 53 & .id %in% c(9546)) %>% # fine
  # filter(.recording == 59 & .id %in% c(10999,11076)) %>% # general noise, remove
  # filter(.recording == 61 & .id %in% c(11602,11687,11709)) %>% # frontal contamination, remove
  # filter(.recording == 7 & .id %in% c(13721)) %>% # drift, remove
  # filter(.recording == 71 & .id %in% c(14099,14131)) %>% # frontal contamination, remove
  # filter(.recording == 72 & .id %in% c(14255)) %>% # blink not well corrected, remove
  plot() +
  coord_cartesian(clip = "off") +
  annotate_events() +
  theme(legend.position = "bottom")


# update bad segments dataframe and extract IDs
(bad_ids <- eeg_filtered$.segments %>%
  distinct(.id) %>%
  filter(!(.id %in% c(9546, 8196))) %>%
  pull() %>%
  as.numeric())

# mark bad segments as artifact in eeg
eeg <- eeg %>% eeg_events_to_NA(.id %in% bad_ids, .entire_seg = TRUE, .drop_events = FALSE)

# remove bad subjects from eeg data
eeg <- filter(
  eeg,
  !(.recording %in% technical_excludes),
  !(.recording %in% artifact_excludes),
  !(.recording %in% mismatch_excludes)
)


rm(eeg_filtered)
gc()


# .......................................................
# Save mean amplitudes with stimuli
# .......................................................

# read stim_df
stim_df <- read.csv(file.path(data_path, "experimental_stimuli.tsv"), sep = "\t")

# mean amplitudes
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

print(">>> mean amplitude")
n400_chs <- c(
  "Cz", "Pz", "C4", "CP6", "P4", "P3",
  "CP5", "C3", "P8", "P7"
)
amplitude_n400 <- cal_mean_amplitude(
  eeg,
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
  eeg,
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
  left_join(rt_df, by = "segment") # should be stim_df here
