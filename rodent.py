from tkinter import *
from tkinter import filedialog
import pandas as pd


class Rodent:
    def __init__(self, data):
        df = data['snout']
        df.drop('likelihood', inplace=True, axis=1)
        self.snout = df.to_dict('records')

        df = data['leftear']
        df.drop('likelihood', inplace=True, axis=1)
        self.left_ear = df.to_dict('records')

        df = data['rightear']
        df.drop('likelihood', inplace=True, axis=1)
        self.right_ear = df.to_dict('records')

        df = data['upperspine']
        df.drop('likelihood', inplace=True, axis=1)
        self.upper_spine = df.to_dict('records')

        df = data['lowerspine']
        df.drop('likelihood', inplace=True, axis=1)
        self.lower_spine = df.to_dict('records')

        df = data['tailbase']
        df.drop('likelihood', inplace=True, axis=1)
        self.tail_base = df.to_dict('records')

        self.eyes = calculate_centroid([self.snout, self.left_ear, self.right_ear])

        self.center_of_points = calculate_centroid([self.snout,
                                                    self.left_ear,
                                                    self.right_ear,
                                                    self.upper_spine,
                                                    self.lower_spine,
                                                    self.tail_base])

        self.number_of_frames = len(self.snout)

    def get_all_points_from_frame(self, frame):
        return {'snout': self.snout[frame],
                'left_ear': self.left_ear[frame],
                'right_ear': self.right_ear[frame],
                'tail_base': self.tail_base[frame],
                'upper_spine': self.upper_spine[frame],
                'lower_spine': self.lower_spine[frame],
                'eyes': self.eyes[frame],
                'center_of_points': self.center_of_points[frame]}

    def set_all_points_for_frame(self, frame, points):
        self.snout[frame] = points['snout']
        self.left_ear[frame] = points['left_ear']
        self.right_ear[frame] = points['right_ear']
        self.tail_base[frame] = points['tail_base']
        self.upper_spine[frame] = points['upper_spine']
        self.lower_spine[frame] = points['lower_spine']
        self.eyes[frame] = points['eyes']
        self.center_of_points[frame] = points['center_of_points']


def calculate_centroid(list_of_points):
    centroid = []
    number_of_points = len(list_of_points)
    number_of_frames = len(list_of_points[0])

    for i in range(number_of_frames):
        x_avg = 0
        y_avg = 0

        for n in range(number_of_points):
            x_avg += list_of_points[n][i]['x'] / number_of_points
            y_avg += list_of_points[n][i]['y'] / number_of_points

        centroid.append({'x': x_avg, 'y': y_avg})

    return centroid


# Tk().withdraw()
# filename = filedialog.askopenfilename(initialdir=sys.path[0], title='Select trackelt .h5 file:')
#
# df = pd.read_hdf(filename)
# df = df['DLC_resnet50_multi_2Oct19shuffle1_200000']
#
# observer_df = df['observer']
#
#
# observer = Rodent(observer_df)
#
# print(observer.center_of_points[0])



