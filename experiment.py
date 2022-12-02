import pandas as pd
from pandas import DataFrame as df
import datetime
from datetime import datetime as dt
from single_trial import *

def run_experiment(pid):
  try:
    print('Loading config_{}.csv...'.format(pid), end='\r')
    config = pd.read_csv(
        os.path.join(PATH_INPUT, 'config_{}.csv'.format(pid)),
        keep_default_na=False).to_dict(orient='records')
    print('Loading config_{}.csv...done'.format(pid))

    print('Loading block_parameters_{}.csv...'.format(pid), end='\r')
    block_params = pd.read_csv(
        os.path.join(PATH_INPUT, 'block_parameters_{}.csv'.format(pid)),
        keep_default_na=False).to_dict(orient='records')
    print('Loading block_parameters_{}.csv...done'.format(pid))

    print('Loading experimental_parameters_{}.csv...'.format(pid), end='\r')
    experimental_params = pd.read_csv(
        os.path.join(PATH_INPUT, 'experimental_parameters_{}.csv'.format(pid)),
        keep_default_na=False).to_dict(orient='records')
    print('Loading experimental_parameters_{}.csv...done\n'.format(pid))
  except BaseException as error:
    exit('\n{}\n{}\n{}\n{}'.format(error,
                                  '#######################',
                                  '### EXITING PROGRAM ###',
                                  '#######################'))

  os.makedirs(PATH_OUTPUT, exist_ok=True)
  config_out = os.path.join(PATH_OUTPUT, 'out_config_{}.csv'.format(pid))
  block_out = os.path.join(PATH_OUTPUT, 'out_block_parameters_{}.csv'.format(pid))
  exp_out = os.path.join(PATH_OUTPUT, 'out_experimental_parameters_{}.csv'.format(pid))

  config_df = df.from_dict(config)
  config_df.to_csv(config_out, mode='w+', index=False,
                   header=not os.path.exists(config_out))

  iteration = block_number = block_start_time = inter_block_pause_duration = 0
  last_block = block_params[-1]['block']

  show_instructions()
  show_pre_trial_countdown()

  for exp_param in experimental_params:
    iteration += 1
    trial = Trial(exp_param, iteration)

    if trial.block > block_number:
      if not block_number == 0:
        block_end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        block_params[block_number-1]['end_time'] = block_end_time
        block_df = df.from_dict(block_params)
        block_df.to_csv(block_out, mode='w+', index=False,
                        header=not os.path.exists(block_out))
        print('### BLOCK {} END: {}'.format(block_number, block_end_time))
        show_inter_block_countdown(inter_block_pause_duration)
        show_pre_trial_countdown()

      inter_block_pause_duration = block_params[block_number]['inter_block_pause_duration'] 
      block_start_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      block_params[block_number]['start_time'] = block_start_time
      block_df = df.from_dict(block_params)
      block_df.to_csv(block_out, mode='w+', index=False,
                      header=not os.path.exists(block_out))
      block_number = trial.block
      print('### BLOCK {} BEGIN: {}'.format(block_number, block_start_time))
 
    response = run_trial(trial)

    if response:
      exp_param['response'] = response[0].name
      exp_param['response_time_ms'] = [response[0].rt * 1000]
    else:
      exp_param['response'] = 'NA'
      exp_param['response_time_ms'] = ['NA']

    exp_df = df.from_dict(exp_param)
    exp_df.to_csv(exp_out, mode='a+', index=False,
                  header=not os.path.exists(exp_out))

  block_end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
  block_params[block_number-1]['end_time'] = block_end_time
  block_df = df.from_dict(block_params)
  block_df.to_csv(block_out, mode='w+', index=False,
                  header=not os.path.exists(block_out))
  print('### BLOCK {} END: {}'.format(block_number, block_end_time))

  print('Experiment completed:', block_end_time)
  print('Results written to:', PATH_OUTPUT)

  show_completion_message()

def show_instructions():
  print('### EXPERIMENT BEGIN: {}'.format(dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
  print('AWAITING RESPONSE', end='\r')
  instructions = visual.TextBox2(WINDOW, text=INSTRUCTIONS,
                                 alignment='center', color='black', bold=True,
                                 letterHeight=28, size=[99999, None])
  instructions.draw()
  WINDOW.flip()

  KEYBOARD.clearEvents()
  response = KEYBOARD.waitKeys(keyList=['space'], waitRelease=False)
  print('Response: {} {}'.format(response[0].name, dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
  WINDOW.flip()
  core.wait(0.5)

def show_pre_trial_countdown():
  countdown_stim_L = visual.TextStim(WINDOW)
  countdown_stim_R = visual.TextStim(WINDOW)
  countdown_stim_L.bold = countdown_stim_R.bold = True
  countdown_stim_L.colorSpace = countdown_stim_R.colorSpace = 'rgb'
  countdown_stim_L.color = countdown_stim_R.color = 'black'
  countdown_stim_L.units = countdown_stim_R.units = 'deg'
  countdown_stim_L.size = countdown_stim_R.size = R2_SIZE
  countdown_stim_L.pos = [STIMULI['left'][0]['x'], STIMULI['left'][0]['y']]
  countdown_stim_R.pos = [STIMULI['right'][0]['x'], STIMULI['right'][0]['y']]
  
  for i in range(3, 0, -1):
    print('COUNTDOWN:', datetime.timedelta(0, i), end='\r')
    countdown_stim_L.text = countdown_stim_R.text = '{}...'.format(i)
    countdown_stim_L.draw()
    countdown_stim_R.draw()
    WINDOW.flip()
    core.wait(1)
  print('      BEGIN       ', end='\r')

  countdown_stim_L.text = countdown_stim_R.text = 'BEGIN'
  countdown_stim_L.draw()
  countdown_stim_R.draw()
  WINDOW.flip()
  core.wait(1)

  WINDOW.flip()
  core.wait(1)

def show_inter_block_countdown(secs):
  print('### INTER-BLOCK PAUSE: {} ms'.format(secs))
  pause_message = visual.TextBox2(WINDOW, text='',
                                  alignment='center', color='black', bold=True,
                                  letterHeight=32, size=[99999, None])
  KEYBOARD.clearEvents()

  for i in range(round(secs/1000), -1, -1):
    response = KEYBOARD.getKeys(keyList=['space'], waitRelease=False)
    if response: break

    time_left = datetime.timedelta(0, i)
    print('COUNTDOWN: {}'.format(time_left), end='\r')
    pause_message.text = 'You may now take a short break.\n\nREMAINING TIME: {}\n\nPress [SPACE BAR] to continue now.'.format(time_left)
    pause_message.draw()
    WINDOW.flip()
    core.wait(secs=1, hogCPUperiod=1)
  print()

  WINDOW.flip()
  core.wait(1)

def show_completion_message():
  message = 'Thank you for your time.\n\nThe experiment is now over.\n\nPress [SPACE BAR] to end this session.'
  completion_message = visual.TextBox2(WINDOW, text=message,
                                 alignment='center', color='black', bold=True,
                                 letterHeight=32, size=[99999, None])
  completion_message.draw()
  WINDOW.flip()

  KEYBOARD.clearEvents()
  KEYBOARD.waitKeys(keyList=['space'], waitRelease=False)
  WINDOW.flip()
  core.wait(0.5)