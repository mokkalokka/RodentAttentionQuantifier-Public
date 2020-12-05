# Makes dir for the analysis files
import os
import sys


def move_files_to_dir(videofile_path):
    my_dir = sys.path[0] + '/data/'
    video_identifier = (videofile_path.split('/')[-1]).split('.mp4')[0]
    new_dir = my_dir + 'plotted_videos/'

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for fname in os.listdir(my_dir):
        if fname.startswith(video_identifier) and fname.endswith('plotted.mp4'):
            os.replace(my_dir + fname, new_dir + fname)


def delete_analysis_temp_files(videofile_path):
    my_dir = sys.path[0] + '/data/'
    video_identifier = (videofile_path.split('/')[-1]).split('.mp4')[0]

    for fname in os.listdir(my_dir):
        if fname.startswith(video_identifier) and not fname.endswith('plotted.mp4'):
            os.remove(my_dir + '/' + fname)

