from master_config import *

class Trial:
  def __init__(self, exp_param, iteration):
    self.pid = exp_param['pid']
    self.block = exp_param['block']
    self.first_eye = exp_param['first_stimulus_eye']
    self.first_location = exp_param['first_stimulus_location']
    self.first_color = exp_param['first_stimulus_color']
    self.second_eye = 'left' if self.first_eye == 'right' else 'right'
    self.second_location = exp_param['second_stimulus_location']
    self.second_color = exp_param['second_stimulus_color']
    self.second_color = ('red' if self.second_color == 'NA'
                              and self.first_color == 'green' else 'green')
    self.central_fixation_cross_duration = exp_param['central_fixation_cross_duration']
    self.pre_stimuli_pause_duration = exp_param['pre_stimuli_pause_duration']
    self.temporal_disparity =  exp_param['temporal_disparity']
    self.stimuli_duration =  exp_param['stimuli_duration']
    self.post_stimuli_pause_duration =  exp_param['post_stimuli_pause_duration']
    self.response_collection_duration =  exp_param['response_collection_duration']
    self.intertrial_pause_duration =  exp_param['intertrial_pause_duration']
    self.repetition =  exp_param['repetition']
    self.iteration = iteration

    self.__generate_stimuli()

  def __generate_stimuli(self):
    self.cross_stim_L = visual.TextStim(WINDOW)
    self.cross_stim_R = visual.TextStim(WINDOW)
    self.cross_stim_L.text = self.cross_stim_R.text = '+'
    self.cross_stim_L.colorSpace = self.cross_stim_R.colorSpace = 'rgb'
    self.cross_stim_L.color = self.cross_stim_R.color = 'black'
    self.cross_stim_L.units = self.cross_stim_R.units = 'deg'
    self.cross_stim_L.size = self.cross_stim_R.size = R2_SIZE
    self.cross_stim_L.pos = [STIMULI['left'][0]['x'], STIMULI['left'][0]['y']]
    self.cross_stim_R.pos = [STIMULI['right'][0]['x'], STIMULI['right'][0]['y']]

    self.dot_stim_first = visual.DotStim(WINDOW)
    self.dot_stim_first.units = 'deg'
    self.dot_stim_first.dotSize = monitorunittools.deg2pix(STIMULI[self.first_eye][self.first_location]['size'], MONITOR)
    self.dot_stim_first.colorSpace = 'rgb'
    self.dot_stim_first.color = self.first_color
    self.dot_stim_first.pos = [STIMULI[self.first_eye][self.first_location]['x'],STIMULI[self.first_eye][self.first_location]['y']]

    self.dot_stim_second = visual.DotStim(WINDOW)
    self.dot_stim_second.units = 'deg'
    self.dot_stim_second.dotSize = monitorunittools.deg2pix(STIMULI['right'][self.second_location]['size'], MONITOR)
    self.dot_stim_second.colorSpace = 'rgb'
    self.dot_stim_second.color = self.second_color
    self.dot_stim_second.pos = [STIMULI[self.second_eye][self.second_location]['x'], STIMULI[self.second_eye][self.second_location]['y']]

    self.question_stim_L = visual.TextStim(WINDOW)
    self.question_stim_R = visual.TextStim(WINDOW)
    self.question_stim_L.text = self.question_stim_R.text = '?'
    self.question_stim_L.bold = self.question_stim_R.bold = True
    self.question_stim_L.colorSpace = self.question_stim_R.colorSpace = 'rgb'
    self.question_stim_L.color = self.question_stim_R.color = 'black'
    self.question_stim_L.units = self.question_stim_R.units = 'deg'
    self.question_stim_L.size = self.question_stim_R.size = R2_SIZE
    self.question_stim_L.pos = [STIMULI['left'][0]['x'], STIMULI['left'][0]['y']]
    self.question_stim_R.pos = [STIMULI['right'][0]['x'], STIMULI['right'][0]['y']]

def run_trial(trial):
  trial.cross_stim_L.draw()
  trial.cross_stim_R.draw()
  WINDOW.flip()
  core.wait(trial.central_fixation_cross_duration/1000)
  
  WINDOW.flip()
  core.wait(trial.pre_stimuli_pause_duration/1000)
  
  trial.dot_stim_first.draw()
  WINDOW.flip()
  core.wait(trial.temporal_disparity/1000)

  trial.dot_stim_first.draw()
  trial.dot_stim_second.draw()
  WINDOW.flip()
  core.wait(trial.post_stimuli_pause_duration/1000)

  trial.question_stim_L.draw()
  trial.question_stim_R.draw()
  WINDOW.flip()

  KEYBOARD.clearEvents()
  KEYBOARD.clock.reset()
  core.wait(secs=trial.response_collection_duration/1000,
            hogCPUperiod=trial.response_collection_duration/1000) 
  response = KEYBOARD.getKeys(keyList=['left', 'right'],
                              waitRelease=False)
  print('Response {}: {} ({})'.format(trial.iteration,
                                  response[0].name if response else 'NA',
                                  response[0].rt*1000 if response else 'NA'))
  WINDOW.flip()
  core.wait(trial.intertrial_pause_duration/1000)

  return response

# for testing stimulus size and positioning
def plot_test():
  print('### RUNNING PLOT TEST')
  
  instructions = visual.TextBox2(WINDOW, text='PLOT TEST\n\nPRESS [SPACE]',
                                 color='black', alignment='center', bold=True,
                                 letterHeight=32, size=[99999, None])
  
  countdown_stim_L = visual.TextStim(WINDOW)
  countdown_stim_R = visual.TextStim(WINDOW)
  countdown_stim_L.bold = countdown_stim_R.bold = True
  countdown_stim_L.colorSpace = countdown_stim_R.colorSpace = 'rgb'
  countdown_stim_L.color = countdown_stim_R.color = 'black'
  countdown_stim_L.units = countdown_stim_R.units = 'deg'
  countdown_stim_L.size = countdown_stim_R.size = R2_SIZE
  countdown_stim_L.pos = [STIMULI['left'][0]['x'], STIMULI['left'][0]['y']]
  countdown_stim_R.pos = [STIMULI['right'][0]['x'], STIMULI['right'][0]['y']]

  stimColors = ['red', 'green']
  stimsL = []
  stimsR = []

  for stim_num in STIMULI['left']:
    if stim_num > 0:
      stim = visual.DotStim(WINDOW)
      stim.units = 'deg'
      stim.dotSize = monitorunittools.deg2pix(STIMULI['left'][stim_num]['size'], MONITOR)
      stim.colorSpace = 'rgb'
      stim.color = stimColors[0]
      stim.pos = [STIMULI['left'][stim_num]['x'], STIMULI['left'][stim_num]['y']]
      stimsL.append(stim)

      stim = visual.DotStim(WINDOW)
      stim.units = 'deg'
      stim.dotSize = monitorunittools.deg2pix(STIMULI['right'][stim_num]['size'], MONITOR)
      stim.colorSpace = 'rgb'
      stim.color = stimColors[1]
      stim.pos = [STIMULI['right'][stim_num]['x'], STIMULI['right'][stim_num]['y']]
      stimsR.append(stim)

      stimColors.reverse()  
    else:
      stim = visual.TextStim(WINDOW)
      stim.text = '+'
      stim.colorSpace = 'rgb'
      stim.color = 'black'
      stim.units = 'deg'
      stim.size = R2_SIZE
      stim.pos = [STIMULI['left'][stim_num]['x'], STIMULI['left'][stim_num]['y']]
      stimsL.append(stim)

      stim = visual.TextStim(WINDOW)
      stim.text = '+'
      stim.colorSpace = 'rgb'
      stim.color = 'black'
      stim.units = 'deg'
      stim.size = R2_SIZE
      stim.pos = [STIMULI['right'][stim_num]['x'], STIMULI['right'][stim_num]['y']]
      stimsR.append(stim)

  question_stim_L = visual.TextStim(WINDOW)
  question_stim_R = visual.TextStim(WINDOW)
  question_stim_L.text = question_stim_R.text = '?'
  question_stim_L.bold = question_stim_R.bold = True
  question_stim_L.colorSpace = question_stim_R.colorSpace = 'rgb'
  question_stim_L.color = question_stim_R.color = 'black'
  question_stim_L.units = question_stim_R.units = 'deg'
  question_stim_L.size = question_stim_R.size = R2_SIZE
  question_stim_L.pos = [STIMULI['left'][0]['x'], STIMULI['left'][0]['y']]
  question_stim_R.pos = [STIMULI['right'][0]['x'], STIMULI['right'][0]['y']]

  instructions.draw()
  WINDOW.flip()
  
  KEYBOARD.clearEvents()
  KEYBOARD.waitKeys(keyList=['space'], waitRelease=False)
  WINDOW.flip()
  core.wait(0.5)

  for i in range(3, 0, -1):
    countdown_stim_L.text = countdown_stim_R.text = '{}...'.format(i)
    countdown_stim_L.draw()
    countdown_stim_R.draw()
    WINDOW.flip()
    core.wait(1)

  countdown_stim_L.text = countdown_stim_R.text = 'BEGIN'
  countdown_stim_L.draw()
  countdown_stim_R.draw()
  WINDOW.flip()
  core.wait(1)

  WINDOW.flip()
  core.wait(1)

  for i in range(len(stimsL)+1):
    for j in range(i):
        stimsL[j].draw()
        stimsR[j].draw()
    WINDOW.flip()
    core.wait(0.3)
  core.wait(0.75)
  
  WINDOW.flip()
  core.wait(0.25)

  question_stim_L.draw()
  question_stim_R.draw()
  WINDOW.flip()
  
  KEYBOARD.clearEvents()
  KEYBOARD.clock.reset()
  core.wait(secs=2, hogCPUperiod=2) 
  response = KEYBOARD.getKeys(keyList=['left', 'right'], waitRelease=False)

  WINDOW.flip()
  core.wait(0.5)

  if response:
    print()
    for i, key in enumerate(response):
      print('{}. {}'.format(i+1, key.name))
      print('  Reaction time: {}'.format(key.rt))
      print('  Time down:     {}'.format(key.tDown))
      print('  Duration:      {}'.format(key.duration))

  return response