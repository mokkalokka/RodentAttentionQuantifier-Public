import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tqdm import trange
from rodent import Rodent
import numpy as np

pd.options.mode.chained_assignment = None


def fix_identities(observer, performer, y_max):
    print('Fixing identity swaps..')
    for frame in trange(observer.number_of_frames):

        observer_tmp_points = observer.get_all_points_from_frame(frame)
        performer_tmp_points = performer.get_all_points_from_frame(frame)

        observer_misidentified = [name for name in observer_tmp_points if observer_tmp_points[name]['y'] > y_max]
        performer_misidentified = [name for name in performer_tmp_points if performer_tmp_points[name]['y'] < y_max]

        if len(observer_misidentified) + len(performer_misidentified) > 0:
            if observer_misidentified != performer_misidentified:
                xor_set = set(observer_misidentified) ^ set(performer_misidentified)
                # print(xor_set)
                for name in xor_set:
                    observer_tmp_points[name] = {'x': np.nan, 'y': np.nan}
                    performer_tmp_points[name] = {'x': np.nan, 'y': np.nan}

            for name in observer_misidentified:
                tmp_point = observer_tmp_points[name]
                observer_tmp_points[name] = performer_tmp_points[name]
                performer_tmp_points[name] = tmp_point
            observer.set_all_points_for_frame(frame, observer_tmp_points)
            performer.set_all_points_for_frame(frame, performer_tmp_points)

        # if observer.snout[frame]['y'] > y_max:
        # if any(point['y'] > y_max for point in observer_tmp_points):
        # if len(observer_misidentified) > 0:
        #     for name in observer_misidentified:
        #         tmp_point = observer_tmp_points[name]
        #         observer_tmp_points[name] = performer_tmp_points[name]
        #         performer_tmp_points[name] = tmp_point
        #     # tmp_points = observer.get_all_points_from_frame(frame)
        #     observer.set_all_points_for_frame(frame, observer_tmp_points)
        #     performer.set_all_points_for_frame(frame, performer_tmp_points)

        # elif performer.snout[frame]['y'] < y_max:
        # elif any(point['y'] < y_max for point in performer_tmp_points):
        # elif len(performer_misidentified) > 0:
        #     for name in observer_misidentified:
        #         tmp_point = performer_tmp_points[name]
        #         performer_tmp_points[name] = observer_tmp_points[name]
        #         observer_tmp_points[name] = tmp_point
        #     # tmp_points = observer.get_all_points_from_frame(frame)
        #     observer.set_all_points_for_frame(frame, observer_tmp_points)
        #     performer.set_all_points_for_frame(frame, performer_tmp_points)

    return observer, performer


def read_tracklets(scorername, preprocessed_video_path, y_max, gui_handler):
    # Tk().withdraw()

    # hdf_points_path = filedialog.askopenfilename(initialdir=sys.path[0] + 'data/',
    #                                              title="Select tracklet file (.h5)",
    #                                              filetypes=[("Hierarchical Data Format (HDF)", "*.h5")]
    #                                              )

    hdf_points_path = preprocessed_video_path.split('.')[0] + scorername + '_bx_filtered.h5'
    df = pd.read_hdf(hdf_points_path)
    df = df[scorername]
    # df = df['DLC_resnet50_multi_2Oct19shuffle1_200000']

    observer = Rodent(df['observer'])
    performer = Rodent(df['task_doer'])

    # gui_handler.plt_test(observer.snout, performer.snout, 'before identity fix')
    observer, performer = fix_identities(observer, performer, y_max)
    # gui_handler.plt_test(observer.snout, performer.snout, 'after identity fix')

    return observer, performer

# For testing that identities actually gets fixes
# def plot_posistion(observer_points, performer_points, title):
#     o_df = pd.DataFrame(observer_points)
#     p_df = pd.DataFrame(performer_points)
#     plt.scatter(o_df['x'], o_df['y'])
#     plt.scatter(p_df['x'], p_df['y'])
#     plt.legend(['observer', 'performer'])
#     plt.title(title)
#     plt.show()


# read_tracklets('', '', 150)
