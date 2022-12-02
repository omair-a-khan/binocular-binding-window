from psychopy import visual, core, event, monitors
from psychopy.tools import monitorunittools
from psychopy.hardware import keyboard
import numpy as np
import os

print('#####################')
print('### PROGRAM START ###')
print('#####################')

PATH_PARTICIPANT_DATA = os.path.join(os.getcwd(), 'participant_data')
PATH_INPUT = os.path.join(PATH_PARTICIPANT_DATA, 'input')
PATH_OUTPUT = os.path.join(PATH_PARTICIPANT_DATA, 'output')

# stimulus radius (dva)
R0_SIZE = 1.00 
R1_SIZE = 1.40
R2_SIZE = 1.96
R3_SIZE = 3.00
# stimulus eccentricity (dva)
R0_ECCENTRICITY = 0.00
R1_ECCENTRICITY = 1.25
R2_ECCENTRICITY = 2.50
R3_ECCENTRICITY = 5.00

# display specifications
DISPLAY_SIZE_X_PX =      2736
DISPLAY_SIZE_Y_PX =      1824
DISPLAY_SIZE_X_CM =      29.0
DISPLAY_SIZE_Y_CM =      20.1
DISTANCE_TO_DISPLAY_CM = 20.0

MONITOR = monitors.Monitor(name='bbw_monitor',
                           width=DISPLAY_SIZE_X_CM,
                           distance=DISTANCE_TO_DISPLAY_CM)
MONITOR.setSizePix([DISPLAY_SIZE_X_PX, DISPLAY_SIZE_Y_PX])
MONITOR.save()

WINDOW = visual.Window(monitor=MONITOR,
                       size=MONITOR.getSizePix(),
                       units="pix",
                       pos=(0,0),
                       color=(255, 255, 255),
                       colorSpace='rgb255',
                       fullscr=True)

KEYBOARD = keyboard.Keyboard()

ORIGIN_RIGHT = monitorunittools.pix2deg(WINDOW.clientSize[0]/4, MONITOR)
ORIGIN_LEFT = -ORIGIN_RIGHT

# formulae
DISPLAY_DIAG_PX = np.sqrt(DISPLAY_SIZE_X_PX**2 + DISPLAY_SIZE_Y_PX**2)
DISPLAY_DIAG_CM = np.sqrt(DISPLAY_SIZE_X_CM**2 + DISPLAY_SIZE_Y_CM**2)
DVA_PER_CM = 2 * np.arctan(1 / (2 * DISTANCE_TO_DISPLAY_CM)) * 180 / np.pi
PX_PER_DVA = (DISPLAY_DIAG_PX / DISPLAY_DIAG_CM) / DVA_PER_CM

STIMULI = {
    'left': {
      0:  { # central fixation point (cfp)
        'x': ORIGIN_LEFT + R0_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R0_SIZE
      },
      1:  { # N, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R0_ECCENTRICITY,
          'y': R1_ECCENTRICITY,
          'size': R1_SIZE
      },
      2:  { # E, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R1_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R1_SIZE
      },
      3:  { # S, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R0_ECCENTRICITY,
          'y': -R1_ECCENTRICITY,
          'size': R1_SIZE
      },
      4:  { # W, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT - R1_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R1_SIZE
      },
      5:  { # N, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R0_ECCENTRICITY,
          'y': R2_ECCENTRICITY,
          'size': R2_SIZE
      },
      6:  { # NE, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + (R2_ECCENTRICITY * np.sin(np.radians(45))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(45)),
          'size': R2_SIZE
      },
      7:  { # E, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R2_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R2_SIZE
      },
      8:  { # SE, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + (R2_ECCENTRICITY * np.sin(np.radians(135))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(135)),
          'size': R2_SIZE
      },
      9:  { # S, R2_ECCENTRICITY dva from center
          'x': ORIGIN_LEFT + R0_ECCENTRICITY,
          'y': -R2_ECCENTRICITY,
          'size': R2_SIZE
      },
      10: { # SW, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + (R2_ECCENTRICITY * np.sin(np.radians(225))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(224)),
          'size': R2_SIZE
      },
      11: { # W, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT - R2_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R2_SIZE
      },
      12: { # NW, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + (R2_ECCENTRICITY * np.sin(np.radians(315))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(315)),
          'size': R2_SIZE
      },
      13: { # E, R3_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT + R3_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R3_SIZE
      },
      14: { # W, R3_ECCENTRICITY dva from cfp
          'x': ORIGIN_LEFT - R3_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R3_SIZE
      }
    },
    'right': {
      0:  { # central fixation point (cfp)
        'x': ORIGIN_RIGHT + R0_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R0_SIZE
      },
      1:  { # N, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R0_ECCENTRICITY,
          'y': R1_ECCENTRICITY,
          'size': R1_SIZE
      },
      2:  { # E, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R1_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R1_SIZE
      },
      3:  { # S, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R0_ECCENTRICITY,
          'y': -R1_ECCENTRICITY,
          'size': R1_SIZE
      },
      4:  { # W, R1_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT - R1_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R1_SIZE
      },
      5:  { # N, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R0_ECCENTRICITY,
          'y': R2_ECCENTRICITY,
          'size': R2_SIZE
      },
      6:  { # NE, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + (R2_ECCENTRICITY * np.sin(np.radians(45))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(45)),
          'size': R2_SIZE
      },
      7:  { # E, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R2_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R2_SIZE
      },
      8:  { # SE, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + (R2_ECCENTRICITY * np.sin(np.radians(135))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(135)),
          'size': R2_SIZE
      },
      9:  { # S, R2_ECCENTRICITY dva from center
          'x': ORIGIN_RIGHT + R0_ECCENTRICITY,
          'y': -R2_ECCENTRICITY,
          'size': R2_SIZE
      },
      10: { # SW, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + (R2_ECCENTRICITY * np.sin(np.radians(225))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(224)),
          'size': R2_SIZE
      },
      11: { # W, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT - R2_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R2_SIZE
      },
      12: { # NW, R2_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + (R2_ECCENTRICITY * np.sin(np.radians(315))),
          'y': R2_ECCENTRICITY * np.cos(np.radians(315)),
          'size': R2_SIZE
      },
      13: { # E, R3_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT + R3_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R3_SIZE
      },
      14: { # W, R3_ECCENTRICITY dva from cfp
          'x': ORIGIN_RIGHT - R3_ECCENTRICITY,
          'y': R0_ECCENTRICITY,
          'size': R3_SIZE
      }
    }
}

INSTRUCTIONS = 'This experiment will take about 45 minutes of your time.\n' +\
                                            '\n' +\
                        'You will have the opportunity to take\n' +\
                     'a short stretching break every 12 minutes.\n' +\
                                            '\n' +\
                            'If you need to use the restroom\n' +\
                                'or get a drink of water,\n' +\
                                 'please do so right now.\n' +\
                                            '\n' +\
                      'When the experiment begins, the screen will\n' +\
                  'repeatedly display one or two dots in a rapid fashion.\n' +\
                                            '\n' +\
                  'At each prompt, indicated by a giant question mark (?),\n' +\
                    'press the [LEFT ARROW] key if you saw one dot,\n' +\
                    'or press the [RIGHT ARROW] key if you saw two dots.\n' +\
                                            '\n' +\
              'Please respond as quickly as possible, as you will have the opportunity\n' +\
              'to earn an additional gift card based on your accuracy and response time.\n' +\
                                            '\n'+\
               'If you have any questions, please ask the experimenter right now.\n' +\
                                            '\n'+\
                   'When you are ready to begin, press the [SPACE BAR] key.'


print('Loaded config from {}\n'.format(__file__))