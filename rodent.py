import numpy as np


class Rodent:
    """A class for containing the position of all the points for a given rodent

    :param data: pandas dataframe for the given rodent
    """

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

        self.eyes = calculate_centroid([self.snout, self.left_ear, self.right_ear], ignore_nans=False)

        self.center_of_points = calculate_centroid([self.snout,
                                                    self.left_ear,
                                                    self.right_ear,
                                                    self.upper_spine,
                                                    self.lower_spine,
                                                    self.tail_base],
                                                   ignore_nans=True)

        self.number_of_frames = len(self.snout)

    def get_all_points_from_frame(self, frame):
        """Gets all the points from the current frame of the video

        :param frame: frame number
        :return: Returns all the points as a dictionary
        """
        return {'snout': self.snout[frame],
                'left_ear': self.left_ear[frame],
                'right_ear': self.right_ear[frame],
                'tail_base': self.tail_base[frame],
                'upper_spine': self.upper_spine[frame],
                'lower_spine': self.lower_spine[frame],
                'eyes': self.eyes[frame],
                'center_of_points': self.center_of_points[frame]}

    def set_all_points_for_frame(self, frame, points):
        """Sets all the points for the selected frame from a dictionary of points

        :param frame: Frame number
        :param points: Dictionary of points
        """
        self.snout[frame] = points['snout']
        self.left_ear[frame] = points['left_ear']
        self.right_ear[frame] = points['right_ear']
        self.tail_base[frame] = points['tail_base']
        self.upper_spine[frame] = points['upper_spine']
        self.lower_spine[frame] = points['lower_spine']
        self.eyes[frame] = points['eyes']
        self.center_of_points[frame] = points['center_of_points']


def calculate_centroid(list_of_points, ignore_nans):
    """Takes in 2 or more points and calculates the centroid point. This is used for calculating the eyes by inputing the [left_ear, right_ear, snout]

    :param list_of_points: A list of points
    :param ignore_nans: A option to ignore nan values in case of missing points
    :return: Returns the centroid point
    """
    centroid = []
    number_of_points = len(list_of_points)
    number_of_frames = len(list_of_points[0])

    for i in range(number_of_frames):
        x_avg = 0
        y_avg = 0
        number_of_nans_x = 0
        number_of_nans_y = 0

        if ignore_nans:

            for n in range(number_of_points):
                if np.isnan(list_of_points[n][i]['x']):
                    number_of_nans_x += 1
                if np.isnan(list_of_points[n][i]['y']):
                    number_of_nans_y += 1

        for n in range(number_of_points):
            if number_of_nans_x == number_of_points:
                x_avg = np.nan
            else:
                x_avg += list_of_points[n][i]['x'] / (number_of_points - number_of_nans_x)
            if number_of_nans_y == number_of_points:
                y_avg = np.nan
            else:
                y_avg += list_of_points[n][i]['y'] / (number_of_points - number_of_nans_y)

        centroid.append({'x': x_avg, 'y': y_avg})

    return centroid
