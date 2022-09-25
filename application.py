try:
    import matplotlib
except ModuleNotFoundError:
    import sys, subprocess
    print('')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib'])
    import matplotlib
    print('')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from experiment import *

class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.figure = self.axes = self.canvas = self.dva_to_point = self.pid_input_text = self.menu_text = None
        self.experiment_running = self.getting_pid = False
        self.pid_input = []
        self.response_keypress = self.pid = ''
        self.response_start_time = self.response_time = None
        self.createWidgets()
        self.show_help_message()

    def createWidgets(self, show_grid=False):
        configure_grid(enabled=show_grid)

        figure, axes = plt.subplots(1,2)
        figure.set_size_inches(8,6)
        # figure.set_size_inches(tk.Tk.winfo_screenwidth(self) * dpi * 0.9,
        #                       tk.Tk.winfo_screenheight(self) * dpi * 0.9)
        dpi = 1 / figure.dpi

        axes[0].set_aspect('equal', adjustable='box')
        axes[0].set(xlim=(-6.0, 6.0), ylim=(-6.0, 6.0))
        axes[1].set_aspect('equal', adjustable='box')
        axes[1].set(xlim=(-6.0, 6.0), ylim=(-6.0, 6.0))
        axes[0].set_position([0, 0.25, 0.5, 0.5])
        axes[1].set_position([0.5, 0.25, 0.5, 0.5])
        
        canvas = FigureCanvasTkAgg(figure, master=self.master)
        canvas.mpl_connect('key_press_event', self.keypress_event)
        canvas.get_tk_widget().grid(row=0,column=0)
        canvas.draw()
        self.figure, self.axes, self.canvas = figure, axes, canvas
        self.dva_to_point = PX_PER_DVA * (72. * dpi) # Matplotlib uses 'points' as the unit for marker size
                                                     # see: https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html#using-offset-transforms-to-create-a-shadow-effect

    def keypress_event(self, event):
        print('>> KeypressEvent: ' + (event.key if event.key != ' ' else 'space'))
        match event.key.lower():
            case 'escape' | 'ctrl+c':
                self.canvas.stop_event_loop()
                close_application(self.master)
            case 'enter':
                if not self.experiment_running:
                    self.experiment_running = True
                    self.begin_experiment()
                    self.experiment_running = False
                    self.canvas.start_event_loop(0.25)
                    self.show_help_message()
                elif self.getting_pid:
                    if self.pid != '' and self.pid != '000':
                        self.canvas.stop_event_loop()
            case 't':
                if not self.experiment_running:
                    self.experiment_running = True
                    self.createWidgets(show_grid=True)
                    print('Running plot_test...')
                    plot_test(self, ['g','r'])
                    self.createWidgets()
                    print('plot_test complete.')
                    self.experiment_running = False
                    self.canvas.start_event_loop(0.25)
                    self.show_help_message()
            case 'h':
                if not self.experiment_running:
                    self.show_help_message()
            case ' ':
                if self.experiment_running and self.getting_pid != True:
                    self.canvas.stop_event_loop()
            case 'left':
                if self.experiment_running and self.response_keypress == 'NA':
                    self.response_time = dt.now() - self.response_start_time
                    self.response_keypress = '1'
            case 'right':
                if self.experiment_running and self.response_keypress == 'NA':
                    self.response_time = dt.now() - self.response_start_time
                    self.response_keypress = '2'
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                if self.getting_pid and len(self.pid_input) < 3:
                    self.pid_input.append(event.key)
                    self.update_pid()
            case 'backspace':
                if self.getting_pid and len(self.pid_input) > 0:
                    self.pid_input.pop()
                    self.update_pid()
            case 'l':
                self.test()

    def show_help_message(self):
        if self.menu_text:
            self.menu_text.set_visible(False)
        self.menu_text = self.figure.text(0.5, 0.5, HELP_TEXT,
                                        fontsize=12, family='monospace',
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        transform=self.figure.transFigure)
        self.canvas.draw()
        print('===========')
        print('{:>10}: {}'.format('Esc', 'Quit'))
        print('{:>10}: {}'.format('Enter', 'Begin experiment'))
        print('{:>10}: {}'.format('T', 'Test plots (debug)'))
        print('{:>10}: {}'.format('H', 'Print this help message'))
        print('===========')

    def begin_experiment(self):
        self.getting_pid = True
        self.menu_text.set_visible(False)
        self.canvas.draw()
        self.canvas.start_event_loop(0.1)
        self.pid_input_text = self.figure.text(0.5, 0.5, 'Enter PID:\n\n- - -\n\n',
                                        fontsize=12, family='monospace',
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        transform=self.figure.transFigure)
        self.canvas.draw()
        self.canvas.start_event_loop()
        
        self.getting_pid = False
        print("Entered PID:", self.pid)
        self.pid_input_text.set_visible(False)
        self.canvas.draw()
        self.canvas.start_event_loop(0.25)
        
        run_experiment(self)

    def update_pid(self):
        self.pid = ''.join(self.pid_input).rjust(3, '0')

        self.pid_input_text.set_visible(False)

        if self.pid == '':
            self.pid_input_text = self.figure.text(0.5, 0.5, 'Enter PID:\n\n- - -\n\n',
                            fontsize=12, family='monospace',
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform=self.figure.transFigure)
        else:
            self.pid_input_text = self.figure.text(0.5, 0.5, 'Enter PID:\n\n'+ self.pid + '\n\nPress [ENTER] when done.',
                            fontsize=12, family='monospace',
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform=self.figure.transFigure)
        
        self.canvas.draw()

def configure_grid(enabled=False):
    plt.rcParams['axes.grid'] = enabled
    plt.rcParams['axes.spines.left'] = enabled
    plt.rcParams['axes.spines.right'] = enabled
    plt.rcParams['axes.spines.top'] = enabled
    plt.rcParams['axes.spines.bottom'] = enabled
    plt.rcParams['xtick.bottom'] = enabled
    plt.rcParams['xtick.labelbottom'] = enabled
    plt.rcParams['ytick.left'] = enabled
    plt.rcParams['ytick.labelleft'] = enabled
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['toolbar'] = 'None' 
    plt.gca().set_aspect('equal', adjustable='box')
    plt.close()

def close_application(master):
    print('Closing application.')
    master.quit()
    master.destroy()