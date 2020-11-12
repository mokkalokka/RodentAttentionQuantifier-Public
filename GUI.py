import io
import platform
import threading
import time
from tkinter import Tk, Text, BOTH, W, N, E, S, StringVar, filedialog, HORIZONTAL, LEFT, RIGHT, IntVar, Checkbutton, \
    Menu
from tkinter.ttk import Frame, Button, Label, Style, Progressbar
import sys
from tqdm import trange
from io import StringIO  # Python 3
from contextlib import redirect_stdout
from attention_quantifier import start_pipeline
from crop_and_confine import crop_and_confine
from log_to_file import log_to_file
import matplotlib.pyplot as plt
from plot_angle_on_video import plot_angle_on_video
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import pandas as pd

import multiprocessing


# multiprocessing.set_start_method("spawn", force=True)


class Example(Frame):

    def __init__(self):
        super().__init__()
        self.video_input_paths = ''
        self.initUI()
        self.thread = None
        # self.task_title = None
        self.results = None
        # Checkbox options
        # self.plot = IntVar()

    def update_console(self, txt='', clear=False):
        txt = '\n' + txt
        self.console.configure(state='normal')
        if clear:
            self.console.delete('1.0', 'end')
        self.console.insert('end', txt)
        self.console.configure(state='disabled')

    def update_progress_console(self, txt='', clear=False):
        self.progress_console.configure(state='normal')
        if clear:
            self.progress_console.delete('1.0', 'end')
        self.progress_console.insert('end', txt)
        self.progress_console.configure(state='disabled')

    def open_video(self):
        self.video_input_paths = filedialog.askopenfilenames(initialdir=sys.path[0] + 'data/',
                                                             title='Select unprocessed video file:',
                                                             filetypes=(("Video", "*.h264"), ("all files", "*.*")))

        self.update_console(f'File(s) loaded:\n')
        for file in self.video_input_paths:
            file = file.split('/')[-1]
            self.update_console(f'{file}')

        self.update_console(f'\nNumber of files: {len(self.video_input_paths)}')
        self.thread = None
        self.results = None
        self.run_stdout_capture(False)

    def start_analysis(self):
        if self.video_input_paths == '':
            self.update_console('Please select a video before analysis', clear=True)
        else:
            crop_ratio = []
            max_y_observer = []

            for video_input_path in self.video_input_paths:
                new_crop_ratio, new_max_y_observer = crop_and_confine(video_input_path)
                crop_ratio.append(new_crop_ratio)
                max_y_observer.append(new_max_y_observer)

            self.run_stdout_capture(True)
            # self.progress.start()
            # video_path, crop_ratio, max_y_observer, gui_handler

            # ctx = multiprocessing.get_context('spawn')
            # if __name__ == '__main__':
            #     if platform.system() == "Darwin":
            #         multiprocessing.set_start_method('spawn')

            options = {'plot': self.plot_video.get(),
                       'only_light': self.only_light.get(),
                       'log': self.log.get(),
                       'accumulate': self.accumulate.get()}

            # multiprocessing.set_start_method('spawn')
            # self.process = multiprocessing.Process(
            #     target=start_pipeline, args=[self.video_input_path, crop_ratio,
            #                                  max_y_observer, options, self])
            # self.process.start()
            # self.update_console(f'Options: \nPlotting video: {self.plot_video.get()}\nOnly extracting frames with light:')
            # print(f'plotting video: {plot_video}')
            # plot_video = True
            self.disable_buttons()
            self.thread = threading.Thread(target=start_pipeline,
                                           args=[self.video_input_paths, crop_ratio,
                                                 max_y_observer, options, self])
            self.thread.start()

            # self.progress.stop()
            # self.run_stdout_capture(False)

    def plot_identity_location(self):
        plot = []

        for i in range(len(self.results.observer)):
            observer_points = self.results.observer[i].snout
            performer_points = self.results.performer[i].snout

            window = Tk()
            window.title('Location of rodents with identities')
            # the figure that will contain the plot
            fig = Figure(figsize=(5, 5),
                         dpi=100)

            # adding the subplot
            # plot.append(fig.add_subplot(int(f'1{len(self.results.observer)}{i}')))
            plot.append(fig.add_subplot(111))

            o_df = pd.DataFrame(observer_points)
            # print(o_df)
            p_df = pd.DataFrame(performer_points)
            # print(p_df)
            plot[-1].scatter(o_df['x'], - o_df['y'])
            plot[-1].scatter(p_df['x'], - p_df['y'])
            plot[-1].legend(['Observer', 'Performer'], loc="upper right")
            plot[-1].set_xlim([0, 250])
            plot[-1].set_ylim([-300, 0])
            # plot1.legend(['observer', 'performer'])
            # plot1.title(title)
            filename = self.video_input_paths[i].split('/')[-1]
            plot[-1].set_title(filename)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().pack()

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, window)

            toolbar.update()

            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().pack()

    def disable_buttons(self):
        self.load_btn["state"] = "disabled"
        self.anlysis_btn["state"] = "disabled"

    def enable_buttons(self):
        self.load_btn["state"] = "enabled"
        self.anlysis_btn["state"] = "enabled"
        self.log_btn["state"] = "enabled"
        self.create_video_btn["state"] = "enabled"

    def run_stdout_capture(self, run):
        if run:
            # self.stdout = sys.stdout
            self.stderr = sys.stderr
            # sys.stdout.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called
            # self.stdout.write = sys.stdout.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called
            self.stderr.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called

        else:
            # sys.stdout = self.stdout
            sys.stderr = self.stderr

    def capture_stdout(self, captured_txt):
        # if self.task_title is not None:
        #     captured_txt = self.task_title + '\n' + captured_txt
        self.update_progress_console(captured_txt, True)

    def log_to_file(self):
        log_to_file(self.results.result_txt, self.results.preprocessed_video_path)
        self.update_console('Results logged to results.txt!', True)

    def create_video(self):
        self.update_console('Creating video..', True)
        self.update_console(self.results.preprocessed_video_path)
        self.update_console(type(self.results.observer.eyes))
        self.update_console(type(self.results.observer.snout))
        self.update_console(type(self.results.ball_location))
        self.update_console(type(self.results.angles))

        # self.thread = threading.Thread(target=plot_angle_on_video,
        #                                args=[self.results.preprocessed_video_path,
        #                                      self.results.observer.eyes,
        #                                      self.results.observer.snout,
        #                                      self.results.ball_location,
        #                                      self.results.angles])
        # self.thread.start()
        plot_angle_on_video(self.results.preprocessed_video_path,
                            from_point=self.results.observer.eyes,
                            end_point_1=self.results.observer.snout,
                            end_point_2=self.results.ball_location,
                            angles=self.results.angles)

    def set_progress(self, progress):
        self.progress['value'] = int(progress)
        self.update()

    def initUI(self):
        self.master.title("Rodent Attention Quantifier")
        menubar = Menu(self.master)
        self.pack(fill=BOTH, expand=True)

        self.master.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Load new model")
        fileMenu.add_command(label="Exit")
        menubar.add_cascade(label="File", menu=fileMenu)

        left_frame = Frame(self, width=200)
        right_frame = Frame(self, width=200)

        # left_frame.pack(side=LEFT)
        # right_frame.pack(side=RIGHT)
        left_frame.grid(row=0, column=0)
        right_frame.grid(row=0, column=1)

        right_frame.columnconfigure(0, weight=1, pad=5)
        left_frame.columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.rowconfigure(5, weight=1)
        # self.rowconfigure(5, pad=7)

        lbl = Label(left_frame, text="Console:").grid(row=0, sticky=W, padx=5, pady=5)
        # lbl.grid(sticky=W, pady=4, padx=5)

        self.console = Text(left_frame, state='disabled', height=20)
        self.console.grid(row=1, rowspan=1, padx=5)  # , sticky=E + W + S + N)

        self.progress_console = Text(left_frame, state='disabled', height=2)
        self.progress_console.grid(row=2, rowspan=1,
                                   padx=5)  # , sticky=E + W + S + N)
        # Progress bar widget
        progress_lbl = Label(left_frame, text="Total progress:")
        progress_lbl.grid(row=4, sticky=W, pady=4, padx=5)
        self.progress = Progressbar(left_frame, orient=HORIZONTAL,
                                    length=100, mode='determinate')
        self.progress.grid(row=5,
                           padx=5, sticky=E + W + S + N)

        hbtn = Button(left_frame, text="Help", command=lambda: self.update_console('Helpful text \n', clear=True))
        hbtn.grid(row=6, padx=5)

        # Configure right frame
        self.load_btn = Button(right_frame, text="Load video(s)", command=self.open_video)
        self.load_btn.grid(row=0)
        lbl2 = Label(right_frame, text="Options:")
        lbl2.grid(row=1, pady=5)
        self.plot_video = IntVar()
        self.plot_check = Checkbutton(right_frame, text="Plot on video", var=self.plot_video).grid(row=2, sticky=W)
        self.only_light = IntVar(value=1)
        self.light_check = Checkbutton(right_frame, text="Extract active task", var=self.only_light).grid(row=3,
                                                                                                          sticky=W)
        self.log = IntVar()
        self.log_check = Checkbutton(right_frame, text="Log to file", var=self.log).grid(row=4, sticky=W)

        self.accumulate = IntVar()
        self.accumulate_check = Checkbutton(right_frame, text="Accumulate score", var=self.accumulate) \
            .grid(row=5, sticky=W)

        self.anlysis_btn = Button(right_frame, text="Start analysis", command=self.start_analysis)
        self.anlysis_btn.grid(row=6, pady=60)

        self.log_btn = Button(right_frame, text="Plot identities", state='disabled',
                              command=self.plot_identity_location)
        self.log_btn.grid(row=7, pady=1)
        #
        # self.create_video_btn = Button(right_frame, text="Create video", state='disabled', command=self.create_video)
        # self.create_video_btn.grid(row=6, )

def main():
    root = Tk()
    root.geometry("750x420+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
