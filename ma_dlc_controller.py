import deeplabcut
from deeplabcut.utils import auxiliaryfunctions
import threading
import sys
import os
import sys

os.environ["DLClight"] = "False"


def analyze_videos(path_config_file, videofile_path, shuffle=1, videotype='mp4', manual_refinement=False):



    scorername = deeplabcut.analyze_videos(path_config_file,
                                           videofile_path,
                                           shuffle=shuffle,
                                           videotype=videotype,
                                           c_engine=False,
                                           dynamic=(True, .5, 10) # <- Research
                                           )

    scorername_path = 'data/' + scorername

    # deeplabcut.create_video_with_all_detections(path_config_file, videofile_path, scorername_path)

    deeplabcut.convert_detections2tracklets(path_config_file, videofile_path, videotype=videotype,
                                            shuffle=shuffle, track_method='box', overwrite=True)

    pickle_path = videofile_path.split('.')[0] + scorername + '_bx.pickle'

    # h5_path = videofile_path.split('.')[0] + scorername + '_bx.h5'
    # filtered_h5_path = videofile_path.split('.')[0] + scorername + '_bx_filtered.h5'

    deeplabcut.convert_raw_tracks_to_h5(path_config_file, pickle_path, min_tracklet_len=1, max_gap=2)
    deeplabcut.filterpredictions(path_config_file, [videofile_path], track_method='box')

    if manual_refinement:
        os.system(
            f'pythonw -c "import deeplabcut;deeplabcut.refine_tracklets(\'{path_config_file}\', '
            f'\'{pickle_path}\', \'{videofile_path}\', max_gap=2)"')




    return scorername



# def refine_tracklets(path_config_file, h5_path, videofile_path):
#     deeplabcut.refine_tracklets(
#         path_config_file,
#         h5_path,
#         videofile_path,
#         max_gap=0,
#     )
