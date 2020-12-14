import sys
import threading
from tkinter import Tk, Text, BOTH, W, N, E, S, StringVar, filedialog, HORIZONTAL, IntVar, Checkbutton, \
    Menu
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Frame, Button, Label, Progressbar, Combobox
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from attention_quantifier import start_pipeline
from crop_and_confine import crop_and_confine


class GUI(Frame):

    def __init__(self):
        super().__init__()
        self.video_input_paths = ''
        self.initUI()
        self.thread = None
        self.results = None

    def update_console(self, txt='', clear=False):
        """
        Updates the GUI console

        :param txt: Text to be written to console
        :param clear: Boolean for clearing the console
        """
        fully_scrolled_down = self.console.yview()[1] == 1.0
        txt = '\n' + txt
        self.console.configure(state='normal')
        if clear:
            self.console.delete('1.0', 'end')
        self.console.insert('end', txt)
        self.console.configure(state='disabled')
        # Only scroll down automatically if the user has not scrolled up manually
        if fully_scrolled_down:
            self.console.see("end")

    def update_progress_console(self, txt='', clear=False):
        """
        Updates the progress console

        :param txt: Text to be written (This is gathered from tqdm via sys.stderr )
        :param clear:  Boolean for clearing the console
        """
        self.progress_console.configure(state='normal')
        if clear:
            self.progress_console.delete('1.0', 'end')
        self.progress_console.insert('end', txt)
        self.progress_console.configure(state='disabled')

    def open_video(self):
        """
        Opens up the file chooser to select video(s).
        """
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

    def start_analysis(self):
        """
        Starts the analysis pipeline if all the requirements are met.
        """
        if self.video_input_paths == '':
            self.update_console('Please select a video before analysis', clear=True)
        elif self.mode_combo.current() == -1:
            self.update_console('Please select a extraction mode before analysis', clear=True)
        elif self.focus_combo.current() == -1:
            self.update_console('Please select a focus point before analysis', clear=True)
        else:
            crop_ratio = []
            max_y_observer = []

            for video_input_path in self.video_input_paths:
                new_crop_ratio, new_max_y_observer = crop_and_confine(video_input_path)
                crop_ratio.append(new_crop_ratio)
                max_y_observer.append(new_max_y_observer)

            self.run_stderr_capture(True)

            options = {
                'mode': self.mode_selected.get(),
                'focus': self.focus_mode_selected.get(),
                'plot': self.plot_video.get(),
                'log': self.log.get(),
                'accumulate': self.accumulate.get()}

            print(options)

            self.disable_buttons()
            self.thread = threading.Thread(target=start_pipeline,
                                           args=[self.video_input_paths, crop_ratio,
                                                 max_y_observer, options, self])
            self.thread.start()

    def plot_identity_location(self):
        """
        Plots the location of the two rodents pr frame in a scatter plot (numpy)
        """
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
            plot.append(fig.add_subplot(111))

            o_df = pd.DataFrame(observer_points)
            p_df = pd.DataFrame(performer_points)
            plot[-1].scatter(o_df['x'], - o_df['y'])
            plot[-1].scatter(p_df['x'], - p_df['y'])
            plot[-1].legend(['Observer', 'Performer'], loc="upper right")
            plot[-1].set_xlim([0, 250])
            plot[-1].set_ylim([-300, 0])
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
        """
        Disables the GUI buttons and checkboxes
        """
        self.load_btn["state"] = "disabled"
        self.anlysis_btn["state"] = "disabled"
        self.mode_combo["state"] = "disabled"
        self.focus_combo["state"] = "disabled"
        self.plot_check["state"] = "disabled"
        self.accumulate_check["state"] = "disabled"
        self.log_check["state"] = "disabled"

    def enable_buttons(self):
        """
        Enables the GUI buttons and checkboxes"
        """
        self.load_btn["state"] = "enabled"
        self.anlysis_btn["state"] = "enabled"
        self.plot_btn["state"] = "enabled"
        self.mode_combo["state"] = "enabled"
        self.focus_combo["state"] = "enabled"
        self.plot_check["state"] = "normal"
        self.accumulate_check["state"] = "normal"
        self.log_check["state"] = "normal"

    def run_stderr_capture(self, run):
        """
        Starts the re-routing of sys.stderr to the capture_stderr() method

        :param run: Boolean for starting or stopping this
        """
        if run:
            self.stderr = sys.stderr
            self.stderr.write = self.capture_stderr  # whenever sys.stdout.write is called, redirector is called

        else:
            sys.stderr = self.stderr

    def capture_stderr(self, captured_txt):
        """
        Method for writing what usually is written to the sys.stderr to progress console

        :param captured_txt: Captured text (tqdm progress)
        """
        self.update_progress_console(captured_txt, True)

    def set_progress(self, progress):
        """
        Updates the total progress widget

        :param progress: Progress value (0% - 100%)
        """
        self.progress['value'] = int(progress)
        self.update()

    def get_focus_options(self, *args):
        """
        Gets the selected value from focus drop down

        """
        focus_options = ['Performer (Head)']

        if not (self.mode_selected.get() == 'All frames'):
            focus_options.append('Ball with light')

        elif not (self.focus_combo.current() == -1):
            self.focus_combo.current(0)
        self.focus_combo['values'] = focus_options

    def initUI(self):
        """
        Defines and draws the GUI elements with Tkinter
        """
        self.master.title("Rodent Attention Quantifier")
        self.pack(fill=BOTH, expand=True)
        # menubar = Menu(self.master)
        # self.master.config(menu=menubar)
        # fileMenu = Menu(menubar)
        # fileMenu.add_command(label="Load new model")
        # fileMenu.add_command(label="Exit")
        # menubar.add_cascade(label="File", menu=fileMenu)

        left_frame = Frame(self)
        right_frame = Frame(self)

        left_frame.grid(row=0, column=0, padx=10, sticky=N + S + E + W)
        right_frame.grid(row=0, column=1, sticky=N + S + E + W)

        right_frame.columnconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)

        lbl = Label(left_frame, text="Console:").grid(row=0, sticky=W, padx=5, pady=5)

        self.console = ScrolledText(left_frame, state='disabled', height=20)
        self.console.grid(row=1, rowspan=1)

        self.progress_console = Text(left_frame, state='disabled', height=2)
        self.progress_console.grid(row=2, sticky=W, rowspan=1,
                                   padx=0)

        progress_lbl = Label(left_frame, text="Total progress:")
        progress_lbl.grid(row=4, sticky=W, pady=4, padx=5)
        self.progress = Progressbar(left_frame, orient=HORIZONTAL,
                                    length=100, mode='determinate')
        self.progress.grid(row=5,
                           padx=5, sticky=E + W + S + N)

        help_txt = 'Welcome to Rodent Attention Quantifier!\n\n' \
                   'To start an analysis select one or more videos with the Load Video(s) button.\n' \
                   'Then select extraction mode: \n' \
                   'All Frames (Every frame in the video)\n' \
                   'Light On (Only extract frames when experiment light is turned on)\n' \
                   'Task executed (Only when the light is on and the light is pushed)\n' \
                   'After selecting mode please chose the focus point where the\n' \
                   'attention is calculated towards.\n\n' \
                   'Other options:\n' \
                   'Plot on video: This plots the calculated angles and the vectors from which the \n' \
                   'angles are calculated from.\n' \
                   'Log to file: logs the results to the file /data/results.txt.\n' \
                   'Accumulate score: This accumulates all the videos selected when analysing more\n' \
                   'than one video.\n\n' \
                   'When all the settings are set you can start the analysis by pressing\n' \
                   'Start analysis button.\n' \
                   'When analysis is starting you will first be asked to select the crop ratio. \n' \
                   'This is done by selecting a rectangle around the area of interest.\n' \
                   'After this you must select the area where the observer is confined to.\n' \
                   'Press enter once or twice to continue\n' \
                   'Plot identities can be used to check the location of the calculated identities.\n\n\n' \
                   'If you want to replace the existing pre-trained DeepLabCut model\n' \
                   'you can replace the content in the model folder with your DeepLabCut\n' \
                   'model of choice.'

        hbtn = Button(left_frame, text="Help", command=lambda: self.update_console(help_txt, clear=True))
        hbtn.grid(row=6, padx=5)

        # Configure right frame
        self.load_btn = Button(right_frame, text="Load video(s)", command=self.open_video)
        self.load_btn.grid(row=0, pady=20)

        lbl2 = Label(right_frame, text="Mode:")
        lbl2.grid(row=1, pady=5)
        self.mode_options = [
            "All frames",
            "Light on",
            "Task executed"
        ]

        self.mode_selected = StringVar()
        self.mode_combo = Combobox(right_frame,
                                   textvariable=self.mode_selected,
                                   values=self.mode_options,
                                   state="readonly",
                                   width=18)

        self.mode_combo.grid(row=2, pady=5)
        self.mode_combo.set('Select extraction mode')

        self.mode_selected.trace("w", self.get_focus_options)

        lbl3 = Label(right_frame, text="Focus:")
        lbl3.grid(row=3, pady=5)

        focus_options = ['Performer (Head)']
        self.focus_mode_selected = StringVar()
        self.focus_combo = Combobox(right_frame,
                                    textvariable=self.focus_mode_selected,
                                    state="readonly",
                                    values=focus_options,
                                    width=18,
                                    )
        self.focus_combo.grid(row=4, pady=5)
        self.focus_combo.set('Select focus point')

        lbl4 = Label(right_frame, text="Options:") \
            .grid(row=5, pady=5)

        self.plot_video = IntVar()
        self.plot_check = Checkbutton(right_frame, text="Plot on video", var=self.plot_video)
        self.plot_check.grid(row=6, sticky=W)

        self.log = IntVar()
        self.log.set(1)
        self.log_check = Checkbutton(right_frame, text="Log to file", var=self.log)
        self.log_check.grid(row=7, sticky=W)

        self.accumulate = IntVar()
        self.accumulate_check = Checkbutton(right_frame, text="Accumulate score", var=self.accumulate)
        self.accumulate_check.grid(row=8, sticky=W)

        self.anlysis_btn = Button(right_frame, text="Start analysis", command=self.start_analysis)
        self.anlysis_btn.grid(row=9, pady=10)

        self.plot_btn = Button(right_frame, text="Plot identities", state='disabled',
                               command=self.plot_identity_location)
        self.plot_btn.grid(row=10, pady=1)


def main():
    root = Tk()
    root.geometry("800x440+300+300")
    app = GUI()
    root.mainloop()


if __name__ == '__main__':
    main()
