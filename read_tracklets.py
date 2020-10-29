import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tqdm import trange


def fix_identities(centroid_x, centroid_y, snout_x, snout_y, y_max):
    indices_to_be_removed = []
    print('Fixing identity swaps..')
    for i in trange(len(centroid_y[1])):

        if centroid_y[0][i] < y_max:
            tmp_snout_x = snout_x[0][i]
            tmp_snout_y = snout_y[0][i]
            tmp_centroid_y = centroid_y[0][i]
            tmp_centroid_x = centroid_x[0][i]

            centroid_y[0][i] = centroid_y[1][i]
            centroid_x[0][i] = centroid_x[1][i]
            snout_x[0][i] = snout_x[1][i]
            snout_y[0][i] = snout_y[1][i]

            centroid_y[1][i] = tmp_centroid_y
            centroid_x[1][i] = tmp_centroid_x
            snout_x[1][i] = tmp_snout_x
            snout_y[1][i] = tmp_snout_y

        if centroid_y[1][i] > y_max:
            tmp_snout_x = snout_x[1][i]
            tmp_snout_y = snout_y[1][i]
            tmp_centroid_y = centroid_y[1][i]
            tmp_centroid_x = centroid_x[1][i]

            centroid_y[1][i] = centroid_y[0][i]
            centroid_x[1][i] = centroid_x[0][i]
            snout_x[1][i] = snout_x[0][i]
            snout_y[1][i] = snout_y[0][i]

            centroid_y[0][i] = tmp_centroid_y
            centroid_x[0][i] = tmp_centroid_x
            snout_x[0][i] = tmp_snout_x
            snout_y[0][i] = tmp_snout_y

        if centroid_y[1][i] > y_max or centroid_y[0][i] < y_max:
            indices_to_be_removed.append(i)

    return centroid_x, centroid_y, snout_x, snout_y

    # for i in range(2):
    #  centroid_x[i] = list(np.delete(centroid_x[i], indecies_to_be_removed))
    #  centroid_y[i] = list(np.delete(centroid_y[i], indecies_to_be_removed))
    #  snout_x[i] = list(np.delete(snout_x[i], indecies_to_be_removed))
    #  snout_y[i] = list(np.delete(snout_y[i], indecies_to_be_removed))


def read_tracklets(scorername, preprocessed_video_path):
    Tk().withdraw()

    #hdf_points = filedialog.askopenfilename(initialdir=sys.path[0], title="Select tracklet file (.hd5)") # initialdir="/"
    hdf_points_path = preprocessed_video_path.split('.')[0] + scorername + '_bx.h5'
    df = pd.read_hdf(hdf_points_path)
    # df = pd.read_pickle(filename)
    df = df[scorername]
    #df = df['DLC_resnet50_multi_2Oct19shuffle1_200000']
    # print(df)
    # df = df.loc[0]
    subjects = ['observer', 'task_doer']
    list_of_rows = []

    snout_x = [[], []]
    snout_y = [[], []]

    centroid_x = [[], []]
    centroid_y = [[], []]
    n = -1
    for subject in subjects:
        n += 1

        data = df[subject]['snout']
        snout_x[n] = data['x'].to_numpy()
        snout_y[n] = data['y'].to_numpy()

        data = df[subject]['rightear']
        rightear_x = data['x'].to_numpy()
        rightear_y = data['y'].to_numpy()

        data = df[subject]['leftear']
        leftear_x = data['x'].to_numpy()
        leftear_y = data['y'].to_numpy()

        for i in range(len(data)):
            centroid_x[n].append((snout_x[n][i] + rightear_x[i] + leftear_x[i]) / 3)
            centroid_y[n].append(-(snout_y[n][i] + rightear_y[i] + leftear_y[i]) / 3)

        # plt.plot(centroid_x[n], centroid_y[n])
    y_max = -125
    centroid_x, centroid_y, snout_x, snout_y = fix_identities(centroid_x, centroid_y, snout_x, snout_y, y_max)
    # print(centroid_x)
    #
    # for i in range(2):
    #     plt.plot(centroid_x[i], centroid_y[i])
    #
    # plt.legend(subjects)
    # plt.title('position of centroid')
    # plt.show()
    #
    list_of_rows = []

    for i in range(len(snout_y[1])):
        new_row = {'o_snout_x': snout_x[0][i],
                   'o_snout_y': - snout_y[0][i],
                   'o_centroid_x': centroid_x[0][i],
                   'o_centroid_y': centroid_y[0][i],
                   't_snout_x': snout_x[1][i],
                   't_snout_y': - snout_y[1][i],
                   't_centroid_x': centroid_x[1][i],
                   't_centroid_y': centroid_y[1][i]
                   }
        list_of_rows.append(new_row)
    # print(list_of_rows)

    # list_of_rows = {'hello': 'World'}
    return list_of_rows
