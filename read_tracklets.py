import numpy as np
import pandas as pd
from tqdm import trange
from rodent import Rodent

pd.options.mode.chained_assignment = None


def fix_identities(observer, performer, y_max):
    """
    Takes in the observer and performer objects and crossvalidates the location of each point.
    Specifically if any of the observer points is above the y_max value specified from the
    crop_and_confine method, the points will swap identity.

    This is needed because the pose estimation is unreliable for guessing the right identity.

    :param observer: Observer object
    :param performer: Performer object
    :param y_max: y_max from crop_and_confine()
    :return: Returns the adjusted versions of observer and performer
    """
    print('Fixing identity swaps..')
    for frame in trange(observer.number_of_frames):

        observer_tmp_points = observer.get_all_points_from_frame(frame)
        performer_tmp_points = performer.get_all_points_from_frame(frame)

        observer_misidentified = [name for name in observer_tmp_points if observer_tmp_points[name]['y'] > y_max]
        performer_misidentified = [name for name in performer_tmp_points if performer_tmp_points[name]['y'] < y_max]

        if len(observer_misidentified) + len(performer_misidentified) > 0:
            if observer_misidentified != performer_misidentified:
                xor_set = set(observer_misidentified) ^ set(performer_misidentified)
                for name in xor_set:
                    observer_tmp_points[name] = {'x': np.nan, 'y': np.nan}
                    performer_tmp_points[name] = {'x': np.nan, 'y': np.nan}

            for name in observer_misidentified:
                tmp_point = observer_tmp_points[name]
                observer_tmp_points[name] = performer_tmp_points[name]
                performer_tmp_points[name] = tmp_point
            observer.set_all_points_for_frame(frame, observer_tmp_points)
            performer.set_all_points_for_frame(frame, performer_tmp_points)

    return observer, performer


def read_tracklets(scorername, preprocessed_video_path, y_max, gui_handler):
    """
    Reads the tracklet data (pandas file) from the DeepLabCut pose estimation and creates a
    Rodent object for the observer and the performer

    :param scorername: The scorer name from the analysis
    :param preprocessed_video_path: Path to the preprocessed video
    :param y_max: y_max from
    :param gui_handler: y_max from crop_and_confine()
    :return: Returns the the observer and performer objects
    """
    hdf_points_path = preprocessed_video_path.split('.')[0] + scorername + '_bx_filtered.h5'
    df = pd.read_hdf(hdf_points_path)
    df = df[scorername]

    observer = Rodent(df['observer'])
    performer = Rodent(df['task_doer'])

    observer, performer = fix_identities(observer, performer, y_max)

    return observer, performer
