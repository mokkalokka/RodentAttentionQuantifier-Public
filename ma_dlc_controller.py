import os
import deeplabcut

os.environ["DLClight"] = "False"


def analyze_videos(path_config_file, videofile_path, shuffle=1, videotype='mp4', manual_refinement=False):
    """Method for analysing the selected video with the pre-trained pose estimation model for DeepLabCut.

    This method does the following pipeline:

    - DeepLabCut pose estimation
    - Converts the pose estimation to a raw tracklet file
    - Filters the predictions

    :param path_config_file: DeepLabCut config file
    :param videofile_path: Video to be analysed
    :param shuffle: Shuffle number
    :param videotype: Type of video format (default = mp4)
    :param manual_refinement: Possibility to refine the tracklets manualy (currently unused)
    :return: Returns the scorername that is used to open the pandas HD5 file
    """
    scorername = deeplabcut.analyze_videos(path_config_file,
                                           videofile_path,
                                           shuffle=shuffle,
                                           videotype=videotype,
                                           c_engine=False,
                                           dynamic=(True, .5, 10)  # <- Research
                                           )

    deeplabcut.convert_detections2tracklets(path_config_file, videofile_path, videotype=videotype,
                                            shuffle=shuffle, track_method='box', overwrite=True)

    pickle_path = videofile_path.split('.')[0] + scorername + '_bx.pickle'

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
