import cv2
import numpy as np
from tqdm import trange


def plot_angle_on_video(video_path, options, from_point, end_point_1, end_point_2, angles):
    """
    Plots the results from the analysis frame by frame onto the preprocessed video, with the given options.

    :param video_path: Takes inn the video path
    :param options: Options: mode and focus
    :param from_point: First point to plot from
    :param end_point_1: First point to plot to
    :param end_point_2: Second point to plot to
    :param angles: Calculated angle for each frame
    """
    mode = options['mode']
    if mode == 'All frames':
        mode = 'AF'
    elif mode == 'Light on':
        mode = 'LO'
    else:
        mode = 'TE'

    focus = options['focus']
    if focus == 'Performer (Head)':
        focus = 'PH'
    else:
        focus = 'BL'

    video_output = video_path.split('.')[0] + f'_{mode}_{focus}_plotted.mp4'
    video = cv2.VideoCapture(video_path)

    # Getting the video parameters
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Setting the video output writer
    out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    # Green color in BGR
    color = (0, 255, 0)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Line thickness of 1 px
    thickness = 1

    print('from point: ', len(from_point))
    print('total frames: ', total_frames)

    for i in trange(len(from_point), ncols=70, unit='frames'):
        (grabbed, frame) = video.read()

        if not grabbed:
            break

        if not (np.isnan(sum(list(from_point[i].values()))) or
                np.isnan(sum(list(end_point_1[i].values())))):

            start_point = (int(from_point[i]['x']), int(from_point[i]['y']))
            end_point = (int(end_point_1[i]['x']), int(end_point_1[i]['y']))
            end_point = lengthen_line(start_point, end_point, multiplier=8)
            frame = cv2.line(frame, start_point, end_point, color, thickness)

        if not (np.isnan(sum(list(from_point[i].values()))) or np.isnan(sum(list(end_point_2[i].values())))):
            start_point = (int(from_point[i]['x']), int(from_point[i]['y']))
            end_point = (int(end_point_2[i]['x']), int(end_point_2[i]['y']))
            frame = cv2.line(frame, start_point, end_point, color, thickness)

        txt = f"Angle: {round(angles[i], 2)}"
        frame = cv2.putText(frame, txt, (10, height - 40), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        txt = f"Frame: {i}"
        frame = cv2.putText(frame, txt, (10, height - 10), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        out.write(frame)

    out.release()
    video.release()


def lengthen_line(start_point, end_point, multiplier):
    """
    Takes in two points, and creates a lengthened version of the endpoint according to the multiplier.
    This is based on parameterized line.

    :param start_point: From point
    :param end_point:  To point
    :param multiplier: Multiplier to lengthen the line by
    :return: Returns the lengthened version of the endpoint on the same line as the two original points
    """
    end_point = (start_point[0] + (end_point[0] - start_point[0]) * multiplier,
                 start_point[1] + (end_point[1] - start_point[1]) * multiplier)
    return end_point
