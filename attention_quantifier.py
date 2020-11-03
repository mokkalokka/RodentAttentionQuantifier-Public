from tkinter import *
from tkinter import filedialog
from plot_angle_on_video import plot_angle_on_video
from process_angle import get_angles
from read_tracklets import read_tracklets
from ma_dlc_controller import analyze_videos
from video_preprocessing import video_preprocess
import os

# TODO Create GUI for this section

os.chdir('data')

# Pre-processing video and get coordinates for ball with light
ball_location, preprocessed_video_path, y_max_observer = video_preprocess(extract_pushed_balls=True)
#
#
# # Analyze video with maDLC
# Tk().withdraw()
# #config_file_path = filedialog.askopenfilename(initialdir=sys.path[0], title='Select DLC config file:')
config_file_path = 'config.yaml'
# preprocessed_video_path = 'ObsLear_DudleyPriam_3_preprocessed.mp4'
scorername = analyze_videos(config_file_path, preprocessed_video_path)

# scorername = ''


# Reading the tracklet
print('Reading the tracklet ...')
observer, performer = read_tracklets(scorername, preprocessed_video_path, y_max_observer)

print('Getting the angles ...')
# Calculate the angles between the two vectors [from_point, end_point_1] and [from_point, end_point_2]
angles = get_angles(from_point=observer.eyes,
                    end_point_1=observer.snout,
                    end_point_2=ball_location)

print('Plotting lines and angles on video')
plot_angle_on_video(preprocessed_video_path,
                    from_point=observer.eyes,
                    end_point_1=observer.snout,
                    end_point_2=ball_location,
                    angles=angles)

print("Pipeline finished!")





