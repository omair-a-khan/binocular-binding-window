try:
    import numpy as np
except ModuleNotFoundError:
    import sys, subprocess
    print('')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
    import numpy as np
    print('')
import os

PATH_PARTICIPANT_DATA = os.path.join(os.getcwd(), 'participant_data')
PATH_OUTPUT = os.path.join(os.getcwd(), 'output')

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
DISPLAY_PPI =             267
DISPLAY_SIZE_X_PX =      1024
DISPLAY_SIZE_Y_PX =       768
#DISPLAY_SIZE_X_PX =      2736
#DISPLAY_SIZE_Y_PX =      1824
DISPLAY_SIZE_X_CM =      29.0
DISPLAY_SIZE_Y_CM =      20.1
DISTANCE_TO_DISPLAY_CM = 20.0

# formulae
DISPLAY_DIAG_PX = np.sqrt(DISPLAY_SIZE_X_PX**2 + DISPLAY_SIZE_Y_PX**2)
DISPLAY_DIAG_CM = np.sqrt(DISPLAY_SIZE_X_CM**2 + DISPLAY_SIZE_Y_CM**2)
DVA_PER_CM = 2 * np.arctan(1 / (2 * DISTANCE_TO_DISPLAY_CM)) * 180 / np.pi
PX_PER_DVA = (DISPLAY_DIAG_PX / DISPLAY_DIAG_CM) / DVA_PER_CM

HELP_TEXT = '{:>10} : {:<20}\n\n{:>10} : {:<20}\n\n{:>10} : {:<20}'.format('[Enter]', 'Begin experiment', '[Esc]', 'Quit program', '[T]', 'Test plots (debug)')

INSTRUCTIONS = r'$\bf{' + 'This\ experiment\ will\ take\ about\ 45\ minutes\ of\ your\ time.'+'}$\n'+\
                'You will have the opportunity to take a short stretching break every 12 minutes.' +\
                                            '\n\n'+\
                  r'$\bf{' + 'If\ you\ need\ to\ use\ the\ restroom' + '}$\n'+\
                            r'$\bf{' + 'or\ get\ a\ drink\ of\ water,' + '}$\n'+\
                            r'$\bf{' + 'please\ do\ so\ right\ now.' + '}$\n'+\
                                            '\n'+\
                          'When the experiment begins, the screen will\n'+\
                      'repeatedly display one or two dots in a rapid fashion.\n'+\
                                            '\n'+\
                      'At each prompt, indicated by a giant question mark (?),\n'+\
                      r'$\bf{' + 'press\ the\ [LEFT\ ARROW]\ key\ if\ you\ saw\ one\ dot'+'}$\n'+\
                    r'or $\bf' +' {press\ the\ [RIGHT\ ARROW]\ key\ if\ you\ saw\ two\ dots.' + '}$\n'+\
                                            '\n'+\
              'Please respond as quickly as possible, as you will have the opportunity\n'+\
              'to earn an additional gift card based on your accuracy and response time.\n'+\
                                             '\n'+\
                 'If you have any questions, please ask the experimenter right now.\n'+\
                                             '\n'+\
                r'$\bf{' + 'If\ you\ are\ ready\ to\ begin,\ press\ the\ [SPACE\ BAR]\ key.}$'

STIMULI = {
    0:  { # central fixation point (cfp)
        'x': R0_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R0_SIZE
    },
    1:  { # N, R1_ECCENTRICITY dva from cfp
        'x': R0_ECCENTRICITY,
        'y': R1_ECCENTRICITY,
        'size': R1_SIZE
    },
    2:  { # E, R1_ECCENTRICITY dva from cfp
        'x': R1_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R1_SIZE
    },
    3:  { # S, R1_ECCENTRICITY dva from cfp
        'x': R0_ECCENTRICITY,
        'y': -R1_ECCENTRICITY,
        'size': R1_SIZE
    },
    4:  { # W, R1_ECCENTRICITY dva from cfp
        'x': -R1_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R1_SIZE
    },
    5:  { # N, R2_ECCENTRICITY dva from cfp
        'x': R0_ECCENTRICITY,
        'y': R2_ECCENTRICITY,
        'size': R2_SIZE
    },
    6:  { # NE, R2_ECCENTRICITY dva from cfp
        'x': R2_ECCENTRICITY * np.sin(np.radians(45)),
        'y': R2_ECCENTRICITY * np.cos(np.radians(45)),
        'size': R2_SIZE
    },
    7:  { # E, R2_ECCENTRICITY dva from cfp
        'x': R2_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R2_SIZE
    },
    8:  { # SE, R2_ECCENTRICITY dva from cfp
        'x': R2_ECCENTRICITY * np.sin(np.radians(135)),
        'y': R2_ECCENTRICITY * np.cos(np.radians(135)),
        'size': R2_SIZE
    },
    9:  { # S, R2_ECCENTRICITY dva from center
        'x': R0_ECCENTRICITY,
        'y': -R2_ECCENTRICITY,
        'size': R2_SIZE
    },
    10: { # SW, R2_ECCENTRICITY dva from cfp
        'x': R2_ECCENTRICITY * np.sin(np.radians(225)),
        'y': R2_ECCENTRICITY * np.cos(np.radians(224)),
        'size': R2_SIZE
    },
    11: { # W, R2_ECCENTRICITY dva from cfp
        'x': -R2_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R2_SIZE
    },
    12: { # NW, R2_ECCENTRICITY dva from cfp
        'x': R2_ECCENTRICITY * np.sin(np.radians(315)),
        'y': R2_ECCENTRICITY * np.cos(np.radians(315)),
        'size': R2_SIZE
    },
    13: { # E, R3_ECCENTRICITY dva from cfp
        'x': R3_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R3_SIZE
    },
    14: { # W, R3_ECCENTRICITY dva from cfp
        'x': -R3_ECCENTRICITY,
        'y': R0_ECCENTRICITY,
        'size': R3_SIZE
    }
}

print('Loaded config from ' + __file__)