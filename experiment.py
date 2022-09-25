try:
    import pandas as pd
except ModuleNotFoundError:
    import sys, subprocess
    print('')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
    import pandas as pd
    print('')
from pandas import DataFrame as df
from single_trial import *

def run_experiment(self):
    config = pd.read_csv(
                os.path.join(PATH_PARTICIPANT_DATA, 'input', 'config_{}.csv'.format(self.pid)),
                keep_default_na=False).to_dict(orient='records')
    block_params = pd.read_csv(
                os.path.join(PATH_PARTICIPANT_DATA, 'input', 'block_parameters_{}.csv'.format(self.pid)),
                keep_default_na=False).to_dict(orient='records')
    experimental_params = pd.read_csv(
                os.path.join(PATH_PARTICIPANT_DATA, 'input', 'experimental_parameters_{}.csv'.format(self.pid)),
                keep_default_na=False).to_dict(orient='records')

    iteration = block_number = block_start_time = inter_block_pause_duration = 0
    last_block = block_params[-1]['block']

    show_instructions(self)
    countdown(self)

    for exp_param in experimental_params:
        pid = exp_param['pid']
        block = exp_param['block']
        first_stimulus_eye = exp_param['first_stimulus_eye']
        first_stimulus_color = exp_param['first_stimulus_color']
        second_stimulus_color = exp_param['second_stimulus_color']
        first_stimulus_location = exp_param['first_stimulus_location']
        second_stimulus_location = exp_param['second_stimulus_location']
        central_fixation_cross_duration = exp_param['central_fixation_cross_duration']
        pre_stimuli_pause_duration = exp_param['pre_stimuli_pause_duration']
        temporal_disparity =  exp_param['temporal_disparity']
        stimuli_duration =  exp_param['stimuli_duration']
        post_stimuli_pause_duration =  exp_param['post_stimuli_pause_duration']
        response_collection_duration =  exp_param['response_collection_duration']
        intertrial_pause_duration =  exp_param['intertrial_pause_duration']
        repetition =  exp_param['repetition']

        if block > block_number:
            if not block_number == 0:
                block_end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                block_params[block_number-1]['end_time'] = block_end_time
                pause_plot(self.canvas, inter_block_pause_duration / 1000)

            inter_block_pause_duration = block_params[block_number]['inter_block_pause_duration'] 
            block_start_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            block_params[block_number]['start_time'] = block_start_time
            block_number = block

        # assign axes and color order
        self.axes = [self.axes[0], self.axes[1]] if first_stimulus_eye == 'left' else [self.axes[1], self.axes[0]]
        second_stimulus_color = 'red' if second_stimulus_color == 'NA' and first_stimulus_color == 'green' else 'green'

        response, response_time = run_trial(self, iteration+1,
                                            first_stimulus_eye,
                                            first_stimulus_color, second_stimulus_color,
                                            first_stimulus_location, second_stimulus_location,
                                            central_fixation_cross_duration,
                                            pre_stimuli_pause_duration,
                                            temporal_disparity,
                                            stimuli_duration,
                                            post_stimuli_pause_duration,
                                            response_collection_duration,
                                            intertrial_pause_duration)
        exp_param['response'] = response
        exp_param['response_time_ms'] = response_time

        iteration += 1

    block_end_time = dt.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    block_params[block_number-1]['end_time'] = block_end_time

    output_path = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_path, exist_ok=True)

    output_config_df = df.from_dict(config)
    output_block_params_df = df.from_dict(block_params)
    output_experimental_params_df = df.from_dict(experimental_params)

    output_config_df.to_csv(os.path.join(output_path, 'out_config_{}.csv'.format(self.pid)), index=False)
    output_block_params_df.to_csv(os.path.join(output_path, 'out_block_parameters_{}.csv'.format(self.pid)), index=False)
    output_experimental_params_df.to_csv(os.path.join(output_path, 'out_experimental_parameters_{}.csv'.format(self.pid)), index=False)

    print('Experiment completed:', block_end_time)
    print('Results written to:', output_path)

    completion_message =  self.figure.text(0.5, 0.5,
                                'Thank you for your time.\n\nThe experiment is now over.\n\nPress [SPACE BAR] to end this session.',
                                fontsize=12, family='monospace',
                                horizontalalignment='center',
                                verticalalignment='center',
                                transform=self.figure.transFigure)
    self.canvas.draw()
    self.canvas.start_event_loop()

    completion_message.set_visible(False)
    self.canvas.draw()

def show_instructions(self):
    instructions_text = self.figure.text(0.5, 0.5, INSTRUCTIONS,
                                        fontsize=12,
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        transform=self.figure.transFigure)
    self.canvas.draw()
    self.canvas.start_event_loop()

    instructions_text.set_visible(False)
    self.canvas.draw()
    self.canvas.start_event_loop(1)

def countdown(self):
    canvas = self.canvas
    axes = self.axes
    for i in range(3, 0, -1):
        countdown_string = r'$\bf{' + str(i) + '...}$'
        ax_left_text = axes[0].text(0.5, 0.5, countdown_string, fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
        ax_right_text = axes[1].text(0.5, 0.5, countdown_string, fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
        self.canvas.draw()
        self.canvas.start_event_loop(1)
        
        ax_left_text.set_visible(False)
        ax_right_text.set_visible(False)

    ax_left_text = axes[0].text(0.5, 0.5, r'$\bf{BEGIN}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
    ax_right_text = axes[1].text(0.5, 0.5, r'$\bf{BEGIN}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
    canvas.draw()
    canvas.start_event_loop(1)
    
    ax_left_text.set_visible(False)
    ax_right_text.set_visible(False)
    canvas.draw()
    canvas.start_event_loop(1)