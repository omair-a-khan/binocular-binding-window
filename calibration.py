from psychopy import visual, core, event, monitors
from psychopy.tools import monitorunittools
from psychopy.hardware import keyboard
from pandas import DataFrame as df
import random, timeit, os
import numpy as np

PATH_PARTICIPANT_DATA = os.path.join(os.getcwd(), 'participant_data')
PATH_INPUT = os.path.join(PATH_PARTICIPANT_DATA, 'input')

DISPLAY_SIZE_X_PX = 2736
DISPLAY_SIZE_Y_PX = 1824
DISPLAY_SIZE_X_CM = 29.0
DISPLAY_SIZE_Y_CM = 20.1
VIEW_DISTANCE_CM =  94.0

MONITOR = monitors.Monitor(name='bbw_monitor',
                           width=DISPLAY_SIZE_X_CM,
                           distance=VIEW_DISTANCE_CM)
MONITOR.setSizePix([DISPLAY_SIZE_X_PX, DISPLAY_SIZE_Y_PX])
MONITOR.save()

WINDOW = visual.Window(monitor=MONITOR,
                       size=MONITOR.getSizePix(),
                       units="pix",
                       pos=(0,0),
                       color=128,
                       colorSpace='rgb255',
                       fullscr=True)

KEYBOARD = keyboard.Keyboard()

stim_size_dva = 1    # size of the stimulus (dva)
movement_size = 0.25 # distance to move stimulus on each keypress (px)
jitter_size = 25     # how much to jitter the placement of stimulus on each trial (px)
on_duration = 0.2    # on duration (s) 
off_duration = 1.5   # off duration (s)

window_size = WINDOW.clientSize
center_x = window_size[0]/2 # center of the window in Screen Coordinates (px)
center_y = window_size[1]/2

x_offset_LE = -center_x/4
x_offset_RE = center_x/4
y_offset_LE = 0
y_offset_RE = 0

print()
while True:
  pid = input("Enter PID: ")

  if pid.isnumeric():
    CALIBRATION_OUT = os.path.join(PATH_INPUT, 'calibration_parameters_{}.csv'.format(pid))
    
    if os.path.isfile(CALIBRATION_OUT):
      print('calibration_parameters_{}.csv already exists!'.format(pid))
      while True:
        overwrite = input("Overwrite file? (y/N): ")
        if overwrite in ('y', 'Y'):
          break
        elif overwrite in ('n', 'N'):
          print("Exiting program.")
          exit(0)
        else:
          print("Invalid input!")
    break
  else:
    print('Invalid input!')

print("Beginning calibration.")

stim_LE = visual.ImageStim(win=WINDOW, units="pix", image="assets/CircleFusion_LE.jpg")
stim_LE.size = monitorunittools.deg2pix(stim_size_dva, MONITOR)
stim_RE = visual.ImageStim(win=WINDOW, units="pix", image="assets/CircleFusion_RE.jpg")
stim_RE.size = monitorunittools.deg2pix(stim_size_dva, MONITOR)

stim_dot_LE = visual.DotStim(win=WINDOW, units="pix", color="black")
stim_dot_LE.dotSize = monitorunittools.deg2pix(0.2, MONITOR)
stim_dot_RE = visual.DotStim(win=WINDOW, units="pix", color="black")
stim_dot_RE.dotSize = monitorunittools.deg2pix(0.2, MONITOR)

stim_outline_LE = visual.Circle(win=WINDOW, units="pix", fillColor=None, lineColor="black", lineWidth=5)
stim_outline_LE.radius = monitorunittools.deg2pix(stim_size_dva/2, MONITOR)
stim_outline_RE = visual.Circle(win=WINDOW, units="pix", fillColor=None, lineColor="black", lineWidth=5)
stim_outline_RE.radius = monitorunittools.deg2pix(stim_size_dva/2, MONITOR)

stim_LE.pos = stim_dot_LE.pos = stim_outline_LE.pos = (x_offset_LE, y_offset_LE)

stim_LE.draw()
stim_dot_LE.draw()
stim_outline_LE.draw()
WINDOW.flip()
KEYBOARD.clearEvents()

while True:
  keys = KEYBOARD.getKeys(keyList=['left', 'right', 'up', 'down', 'space', 'q'],
                          waitRelease=False, clear=False)
  if keys and not keys[-1].duration:
    key = keys[-1].name
    if key == 'left':
      x_offset_LE = x_offset_LE - movement_size
    elif key == 'right':
      x_offset_LE = x_offset_LE + movement_size
    elif key == 'up':
      y_offset_LE = y_offset_LE +  movement_size
    elif key == 'down':
      y_offset_LE = y_offset_LE - movement_size
    elif key == 'q':
      print("User aborted the experiment...")
      exit(1)
    elif key == 'space':
      break

    x_offset_LE = max(-center_x, x_offset_LE)
    x_offset_LE = min(center_x, x_offset_LE)
    y_offset_LE = max(-center_y, y_offset_LE)
    y_offset_LE = min(center_y, y_offset_LE)

    stim_LE.pos = stim_dot_LE.pos = stim_outline_LE.pos = (x_offset_LE, y_offset_LE)

    stim_LE.draw()
    stim_dot_LE.draw()
    stim_outline_LE.draw()
    WINDOW.flip()

WINDOW.flip()
core.wait(0.5)

stim_RE.pos = stim_dot_RE.pos = stim_outline_RE.pos = (x_offset_RE, y_offset_RE)

stim_RE.draw()
stim_dot_RE.draw()
stim_outline_RE.draw()
WINDOW.flip()
KEYBOARD.clearEvents()

while True:
  keys = KEYBOARD.getKeys(keyList=['left', 'right', 'up', 'down', 'space', 'q'],
                          waitRelease=False, clear=False)
  if keys and not keys[-1].duration:
    key = keys[-1].name
    if key == 'left':
      x_offset_RE = x_offset_RE - movement_size
    elif key == 'right':
      x_offset_RE = x_offset_RE + movement_size
    elif key == 'up':
      y_offset_RE = y_offset_RE +  movement_size
    elif key == 'down':
      y_offset_RE = y_offset_RE - movement_size
    elif key == 'q':
      print("User aborted the experiment...")
      exit(1)
    elif key == 'space':
      break

    x_offset_RE = max(-center_x, x_offset_RE)
    x_offset_RE = min(center_x, x_offset_RE)
    y_offset_RE = max(-center_y, y_offset_RE)
    y_offset_RE = min(center_y, y_offset_RE)

    stim_RE.pos = stim_dot_RE.pos = stim_outline_RE.pos = (x_offset_RE, y_offset_RE)

    stim_RE.draw()
    stim_dot_RE.draw()
    stim_outline_RE.draw()
    WINDOW.flip()

WINDOW.flip()
core.wait(0.5)

x_offset_RE_n = [None]*3
y_offset_RE_n = [None]*3

for i in range(3):
  core.wait(0.5)

  if i == 0:
    x_offset_RE_n[i] = x_offset_RE + (random.random()*(2*jitter_size)-jitter_size)
    y_offset_RE_n[i] = y_offset_RE + (random.random()*(2*jitter_size)-jitter_size)
  else:
    x_offset_RE_n[i] = x_offset_RE_n[i-1] + (random.random()*(2*jitter_size)-jitter_size)
    y_offset_RE_n[i] = y_offset_RE_n[i-1] + (random.random()*(2*jitter_size)-jitter_size)

  next_event = timeit.default_timer()
  show_stim = True
  KEYBOARD.clearEvents()

  while True:
    if timeit.default_timer() >= next_event:
      if show_stim:
        next_event = timeit.default_timer() + off_duration
        show_stim = False
      else:
        next_event = timeit.default_timer() + on_duration
        show_stim = True

    keys = KEYBOARD.getKeys(keyList=['left', 'right', 'up', 'down', 'space', 'q'],
                            waitRelease=False, clear=False)
    if keys and not keys[-1].duration:
      key = keys[-1].name
      if key == 'left':
        x_offset_RE_n[i] = x_offset_RE_n[i] - movement_size
      elif key == 'right':
        x_offset_RE_n[i] = x_offset_RE_n[i] + movement_size
      elif key == 'up':
        y_offset_RE_n[i] = y_offset_RE_n[i] +  movement_size
      elif key == 'down':
        y_offset_RE_n[i] = y_offset_RE_n[i] - movement_size
      elif key == 'q':
        print("User aborted the experiment...")
        exit(1)
      elif key == 'space':
        break

      x_offset_RE_n[i] = max(-center_x, x_offset_RE_n[i])
      x_offset_RE_n[i] = min(center_x, x_offset_RE_n[i])
      y_offset_RE_n[i] = max(-center_y, y_offset_RE_n[i])
      y_offset_RE_n[i] = min(center_y, y_offset_RE_n[i])

    stim_RE.pos = stim_dot_RE.pos = stim_outline_RE.pos = (x_offset_RE_n[i], y_offset_RE_n[i])

    if show_stim:
      stim_LE.draw()
      stim_dot_LE.draw()
      stim_outline_LE.draw()
      stim_RE.draw()
      stim_dot_RE.draw()
      stim_outline_RE.draw()
    else:
      stim_LE.draw()
      stim_dot_LE.draw()
      stim_outline_LE.draw()
    WINDOW.flip()

WINDOW.flip()
core.wait(0.5)

x_offset_RE_final = np.mean(x_offset_RE_n)
y_offset_RE_final = np.mean(y_offset_RE_n)

parameters = {
  "pid": pid,
  "stim_size_dva": stim_size_dva,
  "movement_size": movement_size,
  "jitter_size": jitter_size,
  "on_duration": on_duration,
  "off_duration": off_duration,
  "display_size_x_cm": DISPLAY_SIZE_X_CM,
  "display_size_y_cm": DISPLAY_SIZE_Y_CM,
  "view_distance_cm": VIEW_DISTANCE_CM,
  "display_size_x_px": WINDOW.clientSize[0],
  "display_size_y_px": WINDOW.clientSize[1],
  "x_offset_LE_final": x_offset_LE,
  "y_offset_LE_final": y_offset_LE,
  "x_offset_RE_final": x_offset_RE_final,
  "y_offset_RE_final": y_offset_RE_final,
  "x_offset_RE_0": x_offset_RE,
  "y_offset_RE_0": y_offset_RE,
  "x_offset_RE_1": [x_offset_RE_n[0]],
  "y_offset_RE_1": [y_offset_RE_n[0]],
  "x_offset_RE_2": [x_offset_RE_n[1]],
  "y_offset_RE_2": [y_offset_RE_n[1]],
  "x_offset_RE_3": [x_offset_RE_n[2]],
  "y_offset_RE_3": [y_offset_RE_n[2]]
}

param_df = df.from_dict(parameters)
param_df.to_csv(CALIBRATION_OUT, mode='w', index=False)
print("Calibration parameters written to: ", CALIBRATION_OUT)
print("Exiting program.")