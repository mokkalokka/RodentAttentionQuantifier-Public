import deeplabcut
from deeplabcut.utils import auxiliaryfunctions


def analyze_videos(path_config_file, videofile_path, model_name='todo', shuffle=1, videotype='mp4'):
    scorername = deeplabcut.analyze_videos(path_config_file,
                                           videofile_path,
                                           shuffle=shuffle,
                                           videotype=videotype,
                                           c_engine=False)

    scorername_path = 'data/'+scorername

    #deeplabcut.create_video_with_all_detections(path_config_file, videofile_path, scorername_path)

    deeplabcut.convert_detections2tracklets(path_config_file, videofile_path, videotype=videotype,
                                            shuffle=shuffle, track_method='box', overwrite=True)

    pickle_path = videofile_path.split('.')[0] + scorername + '_bx.pickle'
    deeplabcut.convert_raw_tracks_to_h5(path_config_file, pickle_path)
    return scorername
