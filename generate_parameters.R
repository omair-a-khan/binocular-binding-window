generate_parameters <- function(pid, n_blocks = 6, n_reps = 4, test = FALSE, grid_visible = FALSE, output.dir = file.path(getwd(), "participant_data", "input")) {
  require(tidyverse)

  set.seed(pid)
  pid_padded <- formatC(pid, width = 3, flag = "0")

  #####
  # Configuration
  #####

  config.df <- tibble(
    pid = pid,
    left_grid_origin_x_coord = NA,
    left_grid_origin_y_coord = NA,
    right_grid_origin_x_coord = NA,
    right_grid_origin_y_coord = NA,
    test = test,
    grid_visible = grid_visible
  )

  write_csv(config.df, file = file.path(output.dir, paste0("config", "_", pid_padded, ".csv")))

  #####
  # Experimental Parameters
  #####

  experimental_parameters.df <- expand.grid(
    pid = pid,
    block = 1:n_blocks,
    first_stimulus_eye = c("left", "right"),
    first_stimulus_color = c("red", "green"),
    second_stimulus_color = NA,
    first_stimulus_location = 0,
    second_stimulus_location = 0:14,
    central_fixation_cross_duration = 75,
    pre_stimuli_pause_duration = 50,
    temporal_disparity = NA,
    stimuli_duration = 40,
    post_stimuli_pause_duration = 50,
    response_collection_duration = 1500,
    intertrial_pause_duration = NA,
    repetition = 1:n_reps
  ) %>%
    tibble()

  experimental_parameters.df$temporal_disparity <- sample(seq(0, 100, 10), nrow(experimental_parameters.df), replace = TRUE)
  experimental_parameters.df$intertrial_pause_duration <- sample(800:1200, nrow(experimental_parameters.df), replace = TRUE)

  k <- sample(nrow(experimental_parameters.df))
  experimental_parameters.df <- experimental_parameters.df[k, ]

  experimental_parameters.df$block <- map(1:n_blocks, ~ rep(.x, nrow(experimental_parameters.df)/n_blocks)) %>% unlist()

  write_csv(experimental_parameters.df, file = file.path(output.dir, paste0("experimental_parameters", "_", pid_padded, ".csv")))

  #####
  # Block Parameters
  #####

  block_parameters.df <- tibble(
    pid = pid,
    block = 1:n_blocks,
    inter_block_pause_duration = 2 * 60 * 1000,
    start_time = NA,
    end_time = NA
  )

  write_csv(block_parameters.df, file = file.path(output.dir, paste0("block_parameters", "_", pid_padded, ".csv")))
}
