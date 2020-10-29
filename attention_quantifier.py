
from tkinter import *
from tkinter import filedialog
from plot_angle_on_video import plot_angle_on_video
from process_angle import get_angles
from read_tracklets import read_tracklets
from ma_dlc_controller import analyze_videos
import os

# TODO Create GUI for this section
from video_preprocessing import video_preprocess

os.chdir('data')

# Pre-processing video and get coordinates for ball with light
list_of_rows, preprocessed_video_path = video_preprocess()


# Analyze video with maDLC
Tk().withdraw()
#config_file_path = filedialog.askopenfilename(initialdir=sys.path[0], title='Select DLC config file:')
config_file_path = 'config.yaml'
preprocessed_video_path = 'unprocessed_preprocessed.mp4'
scorername = analyze_videos(config_file_path, preprocessed_video_path)


# Reading the tracklet
print('Reading the tracklet ...')
list_of_rows = read_tracklets(scorername, preprocessed_video_path)

print('Getting the angles ...')
list_of_rows = get_angles(list_of_rows)

print('Plotting lines and angles on video')
plot_angle_on_video(list_of_rows)

print("Pipeline finished!")







