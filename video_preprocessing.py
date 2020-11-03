import numpy as np
import imutils
import cv2
import pandas as pd
import time
from alive_progress import alive_bar
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True, help="-inn (input video)")
# ap.add_argument("-o", "--output", required=True, help="-output (output video)")
#
# args = vars(ap.parse_args())
# video_path = args['input']
# video_output = args['output']

def video_preprocess(extract_pushed_balls=True, threshold=2):
    root = Tk()
    root.iconify()
    video_input_path = filedialog.askopenfilename(initialdir=sys.path[0],
                                                  title='Select unprocessed video file:',
                                                  filetypes=(("Video", "*.h264"), ("all files", "*.*")))
    video_output_path = video_input_path.split('.')[
                            0] + '_preprocessed.mp4'  # filedialog.asksaveasfilename(initialdir=sys.path[0], title='Select ')

    # Creating a Pandas DataFrame To Store Data Point
    # Data_Features = ['frame', 'original_frame', 'x', 'y', 'radius']
    # list_of_rows = []
    # df = pd.DataFrame(data=None, columns=Data_Features)

    # Setting initial values
    original_frame = 1
    new_frame = 1
    frames_with_light = []
    ball_location = []

    # Initializing OpenCV video capture
    video = cv2.VideoCapture(video_input_path)

    # Setting upper and lower HSV values for green light to be detected
    greenLower = np.array([0, 0, 180])
    greenUpper = np.array([255, 255, 255])

    # Grab first frame and open GUI for cropping
    (grabbed, frame) = video.read()
    fromCenter = False
    r = cv2.selectROI('Crop', frame, fromCenter)
    cv2.waitKey(0)  # close window when a key press is detected
    cv2.destroyWindow('Crop')  # <-- Does not work on mac .......
    root.iconify()

    cropped_frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    observer_area = cv2.selectROI('Confine Observer', cropped_frame, fromCenter)
    cv2.waitKey(0)  # close window when a key press is detected
    cv2.destroyWindow('Confine Observer')  # <-- Does not work on mac .......
    root.deiconify()
    root.iconify()

    max_y_observer = int(observer_area[1] + observer_area[3])
    print(f'Observer confined to: {observer_area}')
    print(f'y_max: {max_y_observer}')
    # root.deiconify()

    # Getting the video parameters
    fps = int(video.get(cv2.CAP_PROP_FPS))
    # total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # height, width = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])].shape[:2]
    height, width = cropped_frame.shape[:2]
    min_y = int(height / 2)

    # Setting the video output writer
    out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), 0)

    print(f'Video metadata after cropping:\nfps: {fps} \nheight: {height}\nwidth: {width}')
    print('Extracting frames with light on using openCV ...')

    # df = pd.read_hdf('coordinates.h5')
    # df = df['coordinates']
    untouched_ball_y = 0
    # threshold = 2

    with alive_bar(0) as bar:
        while True:
            bar()
            (grabbed, frame) = video.read()

            if not grabbed:
                break
            frame = frame[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            original_frame += 1

            frame = imutils.resize(frame, width=int(width))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                if radius > 5 and y > min_y:  # and not (228 < y < 232):  # y > min_y to ensure that ball is only detected in the lower half of video
                    if untouched_ball_y == 0:
                        untouched_ball_y = y
                        # print('untouched: ', untouched_ball_y)

                    if not (
                            untouched_ball_y - threshold < y < untouched_ball_y + threshold) or not extract_pushed_balls:
                        # print('outside bounds')
                        new_row = {
                            'x': x,
                            'y': y,
                            'radius': radius}

                        # print(f'x: {x} \n y: {y}, \n r: {radius}')

                        # 'frame': new_frame,
                        # 'original_frame': original_frame,
                        # 'time (s)': original_frame / fps,

                        ball_location.append(new_row)
                        cv2.circle(frame, (int(x), int(y)), int(radius), (33, 255, 255), 2)

                        frames_with_light.append(frame)
                        new_frame += 1

                        # normalized = np.zeros((width, height))
                        filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        filtered_frame = cv2.normalize(filtered_frame, None, 0, 255, cv2.NORM_MINMAX)
                        alpha = 2  # Contrast control (1.0-3.0)
                        beta = 0  # Brightness control (0-100)
                        filtered_frame = cv2.convertScaleAbs(filtered_frame, alpha=alpha, beta=beta)
                        out.write(filtered_frame)

    out.release()
    video.release()

    # plot ball location
    # plot_posistion(ball_location)
    print(f'Success! Extracted {new_frame} frames.')
    return ball_location, video_output_path, max_y_observer


def plot_posistion(ball_location):
    df = pd.DataFrame(ball_location)
    # print(df)
    plt.scatter(df['x'], df['y'])
    # plt.legend(['observer', 'performer'])
    plt.title('Position of ball with light')
    plt.show()

# video_preprocess()

# Populate and save pandas dataframe

#
# store = pd.HDFStore(f'{str(video_path)}.h5')
# store.append(video_path, df, data_columns=['int32', 'int32', 'int64', 'string'])
# store.close()
