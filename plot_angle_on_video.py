import cv2
from tqdm import trange
import numpy as np
from tkinter import *
from tkinter import filedialog


def plot_angle_on_video(list_of_rows):
    root = Tk()
    root.withdraw()
    root.update()
    video_path = filedialog.askopenfilename(initialdir=sys.path[0], title='Select video to plot on')
    root.destroy()

    #video_output = filedialog.asksaveasfilename(initialdir=sys.path[0], title='Save plotted video as..')
    video_output = video_path.split('.')[0] + '_with_lines_and_angles.mp4'
    # video_output = 'with_lines.mp4'

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

    # Line thickness of 9 px
    thickness = 1
    for i in trange(total_frames):
        (grabbed, frame) = video.read()

        if not grabbed:
            break

        # if not np.isnan(sum(list_of_rows[i].values())):
        if not np.isnan(sum(list(list_of_rows[i].values())[:4])):

            start_point = (int(list_of_rows[i]['o_centroid_x']), -int(list_of_rows[i]['o_centroid_y']))
            end_point = (int(list_of_rows[i]['o_snout_x']), -int(list_of_rows[i]['o_snout_y']))
            end_point = (start_point[0] + (end_point[0] - start_point[0]) * 5, start_point[1] + (end_point[1] - start_point[1]) * 5)
            frame = cv2.line(frame, start_point, end_point, color, thickness)

            if not np.isnan(sum(list(list_of_rows[i].values())[4:])):
                start_point = (int(list_of_rows[i]['o_centroid_x']), -int(list_of_rows[i]['o_centroid_y']))
                end_point = (int(list_of_rows[i]['t_centroid_x']), -int(list_of_rows[i]['t_centroid_y']))
                frame = cv2.line(frame, start_point, end_point, color, thickness)
        txt = f"Angle: {round(list_of_rows[i]['angle'], 2)}"
        frame = cv2.putText(frame, txt, (10, height - 40), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        txt = f"Frame: {i}"
        frame = cv2.putText(frame, txt, (10, height - 10), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        out.write(frame)

    out.release()
    video.release()
