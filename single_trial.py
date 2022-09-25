from datetime import datetime as dt
import decimal
from decimal import Decimal
from master_config import *

decimal.getcontext().prec = 10 # precision for response time (ms)

def run_trial(self, iteration,
             first_stimulus_eye,
             first_stimulus_color, second_stimulus_color,
             first_stimulus_location, second_stimulus_location,
             central_fixation_cross_duration,
             pre_stimuli_pause_duration,
             temporal_disparity,
             stimuli_duration,
             post_stimuli_pause_duration,
             response_collection_duration,
             intertrial_pause_duration):
    axes, canvas, dva_to_point = self.axes, self.canvas, self.dva_to_point

    axes[0].plot(STIMULI[0]['x'], STIMULI[0]['y'], color='black', marker='+', markersize=10, markeredgewidth=2)
    axes[1].plot(STIMULI[0]['x'], STIMULI[0]['y'], color='black', marker='+', markersize=10, markeredgewidth=2)
    canvas.draw()
    pause_plot(canvas, central_fixation_cross_duration / 1000)
    
    axes = clear_axes(canvas, axes)
    pause_plot(canvas, pre_stimuli_pause_duration / 1000)

    axes[0].plot(STIMULI[first_stimulus_location]['x'],
                 STIMULI[first_stimulus_location]['y'],
                 linestyle='None',
                 c=first_stimulus_color, marker='o',
                 markersize=(STIMULI[first_stimulus_location]['size']*dva_to_point))
    canvas.draw()
    pause_plot(canvas, temporal_disparity / 1000)

    axes[1].plot(STIMULI[second_stimulus_location]['x'],
                 STIMULI[second_stimulus_location]['y'],
                 linestyle='None', 
                 c=second_stimulus_color, marker='o',
                 markersize=(STIMULI[second_stimulus_location]['size']*dva_to_point))
    canvas.draw()
    pause_plot(canvas, stimuli_duration / 1000)

    axes = clear_axes(canvas, axes)
    pause_plot(canvas, post_stimuli_pause_duration / 1000)
    
    axes[0].text(0.5, 0.5, r'$\bf{?}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
    axes[1].text(0.5, 0.5, r'$\bf{?}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)    
    canvas.draw()

    self.response_time = 'NA'
    self.response_start_time = dt.now()
    self.response_keypress = 'NA'
    pause_plot(canvas, response_collection_duration / 1000)
    response = self.response_keypress
    response_time = (Decimal(self.response_time.total_seconds())*Decimal(1000.0)) if self.response_time != 'NA' else 'NA'
    self.response_keypress = ''
    print('Response {}: {} ({})'.format(iteration, response, response_time))

    axes = clear_axes(canvas, axes)
    pause_plot(canvas, intertrial_pause_duration / 1000)

    return response, response_time

def clear_axes(canvas, axes):
    axes[0].clear()
    axes[1].clear()
    axes[0].set(xlim=(-6.0, 6.0), ylim=(-6.0, 6.0))
    axes[1].set(xlim=(-6.0, 6.0), ylim=(-6.0, 6.0))
    canvas.draw()
    return axes

def pause_plot(canvas, duration):
    if duration > 0:
        canvas.start_event_loop(duration)

def plot_test(self, stimulus_colors):
    canvas = self.canvas
    axes = clear_axes(canvas, self.axes)
    dva_to_point = self.dva_to_point

    pause_plot(canvas, 1)

    axes[0].plot(STIMULI[0]['x'], STIMULI[0]['y'], color='black', marker='+', markersize=10, markeredgewidth=2)
    axes[1].plot(STIMULI[0]['x'], STIMULI[0]['y'], color='black', marker='+', markersize=10, markeredgewidth=2)
    canvas.draw()
    pause_plot(canvas, 1)
    
    for stimulus in STIMULI.values():
        axes[0].scatter(stimulus['x'], stimulus['y'], c=stimulus_colors[0], marker='o', s=(stimulus['size']*dva_to_point)**2)
        axes[1].scatter(stimulus['x'], stimulus['y'], c=stimulus_colors[1], marker='o', s=(stimulus['size']*dva_to_point)**2)
        stimulus_colors.reverse()
        canvas.draw()
        pause_plot(canvas, 0.25)
    pause_plot(canvas, 0.75)

    axes = clear_axes(canvas, axes)
    pause_plot(canvas, 0.25)

    axes[0].text(0.5, 0.5, r'$\bf{?}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[0].transAxes)
    axes[1].text(0.5, 0.5, r'$\bf{?}$', fontsize=40, horizontalalignment='center', verticalalignment='center', transform=axes[1].transAxes)
    canvas.draw()
    pause_plot(canvas, 2)

    axes = clear_axes(canvas, axes)
    pause_plot(canvas, 0.5)