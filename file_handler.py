import os
import sys
from datetime import datetime


def move_files_to_dir(videofile_path):
    """Moves the generated plotted movie into the /data/plotted_videos/ folder

    :param videofile_path: Takes inn the video path
    """
    my_dir = sys.path[0] + '/results/'
    current_dir = videofile_path.rsplit('/', 1)[0] + '/'

    video_identifier = (videofile_path.split('/')[-1]).split('.mp4')[0]
    new_dir = my_dir + 'plotted_videos/'

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for fname in os.listdir(current_dir):
        if fname.startswith(video_identifier) and fname.endswith('plotted.mp4'):
            os.replace(current_dir + fname, new_dir + fname)


def delete_analysis_temp_files(videofile_path):
    """Removes the temporary files from the analysis

    :param videofile_path: Takes inn the video path
    """
    my_dir = videofile_path.rsplit('/', 1)[0] + '/'
    video_identifier = (videofile_path.split('/')[-1]).split('.mp4')[0]

    for fname in os.listdir(my_dir):
        if fname.startswith(video_identifier) and not fname.endswith('plotted.mp4'):
            os.remove(my_dir + '/' + fname)


def log_to_file(result_txt):
    """Appends all the analysis results to results.txt

    :param result_txt: Takes inn result txt string
    """
    now = datetime.now()
    # open a file to append
    outF = open("results/results.txt", "a")
    outF.write('\nNew analysis:' + "\n")
    outF.write(now.strftime("%d/%m/%Y %H:%M:%S") + "\n")

    for result in result_txt:
        outF.write(result)
