# def update_console(self, txt='', clear=False):
#     txt = '\n' + txt
#     self.console.configure(state='normal')
#     if clear:
#         self.console.delete('1.0', 'end')
#     self.console.insert('end', txt)
#     self.console.configure(state='disabled')
#
#
# def update_progress_console(self, txt='', clear=False):
#     self.progress_console.configure(state='normal')
#     if clear:
#         self.progress_console.delete('1.0', 'end')
#     self.progress_console.insert('end', txt)
#     self.progress_console.configure(state='disabled')
#
#
# def open_video(self):
#     self.video_input_path = filedialog.askopenfilename(initialdir=sys.path[0] + 'data/',
#                                                        title='Select unprocessed video file:',
#                                                        filetypes=(("Video", "*.h264"), ("all files", "*.*")))
#     self.update_console(f'File loaded:\n{self.video_input_path}', clear=True)
#
#
# def start_analysis(self):
#     if self.video_input_path == '':
#         self.update_console('Please select a video before analysis', clear=True)
#     else:
#         crop_ratio, max_y_observer = crop_and_confine(self.video_input_path)
#         self.run_stdout_capture(True)
#         # self.progress.start()
#         # video_path, crop_ratio, max_y_observer, gui_handler
#
#         # ctx = multiprocessing.get_context('spawn')
#         # if __name__ == '__main__':
#         #     if platform.system() == "Darwin":
#         #         multiprocessing.set_start_method('spawn')
#
#         options = {'plot': self.plot_video.get(),
#                    'only_light': self.only_light.get(),
#                    'log': self.log.get()}
#
#         # multiprocessing.set_start_method('spawn')
#         # self.process = multiprocessing.Process(
#         #     target=start_pipeline, args=[self.video_input_path, crop_ratio,
#         #                                  max_y_observer, options, self])
#         # self.process.start()
#         # self.update_console(f'Options: \nPlotting video: {self.plot_video.get()}\nOnly extracting frames with light:')
#         # print(f'plotting video: {plot_video}')
#         # plot_video = True
#         self.disable_buttons()
#         self.thread = threading.Thread(target=start_pipeline,
#                                        args=[self.video_input_path, crop_ratio,
#                                              max_y_observer, options, self])
#         self.thread.start()
#
#         # self.progress.stop()
#         # self.run_stdout_capture(False)
#
#
# def plot_identity_location(self):
#     observer_points = self.results.observer.snout
#     performer_points = self.results.performer.snout
#     title = 'Points after identity swap cleanup'
#
#     window = Tk()
#     window.title('Location of rodents with identities')
#     # the figure that will contain the plot
#     fig = Figure(figsize=(5, 5),
#                  dpi=100)
#
#     # adding the subplot
#     plot1 = fig.add_subplot(111)
#
#     o_df = pd.DataFrame(observer_points)
#     # print(o_df)
#     p_df = pd.DataFrame(performer_points)
#     # print(p_df)
#     plot1.scatter(o_df['x'], - o_df['y'])
#     plot1.scatter(p_df['x'], - p_df['y'])
#     plot1.legend(['Observer', 'Performer'], loc="upper right")
#     # plot1.legend(['observer', 'performer'])
#     # plot1.title(title)
#     plot1.set_title('Location of rodents with identities')
#
#     # creating the Tkinter canvas
#     # containing the Matplotlib figure
#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas.draw()
#
#     # placing the canvas on the Tkinter window
#     canvas.get_tk_widget().pack()
#
#     # creating the Matplotlib toolbar
#     toolbar = NavigationToolbar2Tk(canvas, window)
#
#     toolbar.update()
#
#     # placing the toolbar on the Tkinter window
#     canvas.get_tk_widget().pack()
#
#
# def disable_buttons(self):
#     self.load_btn["state"] = "disabled"
#     self.anlysis_btn["state"] = "disabled"
#
#
# def enable_buttons(self):
#     self.load_btn["state"] = "enabled"
#     self.anlysis_btn["state"] = "enabled"
#     self.log_btn["state"] = "enabled"
#     self.create_video_btn["state"] = "enabled"
#
#
# def run_stdout_capture(self, run):
#     if run:
#         # self.stdout = sys.stdout
#         self.stderr = sys.stderr
#         # sys.stdout.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called
#         # self.stdout.write = sys.stdout.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called
#         self.stderr.write = self.capture_stdout  # whenever sys.stdout.write is called, redirector is called
#
#     else:
#         # sys.stdout = self.stdout
#         sys.stderr = self.stderr
#
#
# def capture_stdout(self, captured_txt):
#     # if self.task_title is not None:
#     #     captured_txt = self.task_title + '\n' + captured_txt
#     self.update_progress_console(captured_txt, True)
#
#
# def log_to_file(self):
#     log_to_file(self.results.result_txt, self.results.preprocessed_video_path)
#     self.update_console('Results logged to results.txt!', True)
#
#
# def create_video(self):
#     self.update_console('Creating video..', True)
#     self.update_console(self.results.preprocessed_video_path)
#     self.update_console(type(self.results.observer.eyes))
#     self.update_console(type(self.results.observer.snout))
#     self.update_console(type(self.results.ball_location))
#     self.update_console(type(self.results.angles))
#
#     # self.thread = threading.Thread(target=plot_angle_on_video,
#     #                                args=[self.results.preprocessed_video_path,
#     #                                      self.results.observer.eyes,
#     #                                      self.results.observer.snout,
#     #                                      self.results.ball_location,
#     #                                      self.results.angles])
#     # self.thread.start()
#     plot_angle_on_video(self.results.preprocessed_video_path,
#                         from_point=self.results.observer.eyes,
#                         end_point_1=self.results.observer.snout,
#                         end_point_2=self.results.ball_location,
#                         angles=self.results.angles)
#
#
# def set_progress(self, progress):
#     self.progress['value'] = int(progress)
#     self.update()