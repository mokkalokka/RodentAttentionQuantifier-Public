import cv2
import numpy as np
from tqdm import trange


def video_preprocess(video_input_path, crop_ratio, gui_handler, options, threshold=2):
    """
    Reads the video file and applies the pre-processing according to the options selected in the GUI

    :param video_input_path: The video path
    :param crop_ratio: Crop ratio from the crop_and_confine() method
    :param gui_handler: Reference to the GUI object for printing to the gui console
    :param options: Options from the GUI
    :param threshold: Threshold (px) for determining that the ball is pushed (default = 2)

    :return:
        - ball_locations - The [x,y] coordinates of the center of the ball pr frame
        - video_output_path - Path to the preprocessed video

    """
    video_output_path = video_input_path.split('.')[0] + '_preprocessed.mp4'

    pushed_max_age = 10
    pushed_age = pushed_max_age + 1
    gui_handler.update_console('Getting the frame count..')
    frame_count = get_frame_count(video_input_path)
    gui_handler.set_progress(15)

    # Setting initial values
    new_frame = 1
    ball_locations = []

    # Initializing OpenCV video capture
    video = cv2.VideoCapture(video_input_path)

    # Setting upper and lower HSV values for green light to be detected
    greenLower = np.array([0, 0, 180])
    greenUpper = np.array([255, 255, 255])

    # Grab first frame and open GUI for cropping
    (grabbed, frame) = video.read()

    cropped_frame = frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
                    int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]

    # Getting the video parameters
    fps = int(video.get(cv2.CAP_PROP_FPS))
    height, width = cropped_frame.shape[:2]
    min_y = int(height / 2)

    # Setting the video output writer
    out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), 0)

    gui_handler.update_console(f'Video metadata after cropping:\nfps: {fps} \nheight: {height}\nwidth: {width}')
    print(f'Video metadata after cropping:\nfps: {fps} \nheight: {height}\nwidth: {width}')
    gui_handler.update_console('Extracting frames using openCV:')
    print('Extracting frames using openCV:')

    untouched_ball_y = 0

    for i in trange(frame_count - 1, ncols=75, unit='frames'):

        (grabbed, frame) = video.read()

        if not grabbed:
            break

        frame = crop_frame(frame, crop_ratio)
        if options['mode'] == 'All frames':
            filtered_frame = filter_frame(frame)
            new_frame += 1
            out.write(filtered_frame)

        else:
            ((x, y), radius) = find_ball_with_light(frame, greenLower, greenUpper)

            # y > min_y to ensure that ball is only detected in the lower half of video
            if radius > 5 and y > min_y:
                if untouched_ball_y == 0:
                    untouched_ball_y = y

                if ball_pushed(untouched_ball_y, threshold, y):
                    pushed_age = 0
                else:
                    pushed_age += 1

                if options['mode'] == 'Light on' or pushed_age < pushed_max_age:
                    ball_location = {
                        'x': x,
                        'y': y,
                        'radius': radius}

                    ball_locations.append(ball_location)
                    filtered_frame = filter_frame(frame)
                    new_frame += 1
                    out.write(filtered_frame)
            else:
                pushed_age = pushed_max_age + 1

    out.release()
    video.release()

    cv2.imshow('cv2 bug..', np.zeros((512, 512, 3), np.uint8))
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print(f'Success! Extracted {new_frame} frames.')

    return ball_locations, video_output_path


def crop_frame(frame, crop_ratio):
    """
    Crops the given frame according to the crop ratio

    :param frame: A frame
    :param crop_ratio: Crop ratio
    :return: Returns the cropped frame
    """
    return frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
           int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]


def find_ball_with_light(frame, greenLower, greenUpper):
    """
    Finds the location of the ball with green light

    :param frame: A frame
    :param greenLower: Lower green HSV values
    :param greenUpper: Upper green HSV values
    :return: Returns (x,y), radius of the ball (defaults to (0,0), 0)
    """
    ((x, y), radius) = ((0, 0), 0)
    # frame = imutils.resize(frame, width=int(width))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

    return (x, y), radius


def filter_frame(frame):
    """
    Filters a frame with the following filters:
    - Gray scale
    - Normalization

    :param frame: A frame
    :return: The filtered frame
    """
    filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filtered_frame = cv2.normalize(filtered_frame, None, 0, 500, cv2.NORM_MINMAX)
    return filtered_frame


def ball_pushed(untouched_ball_y, threshold, y):
    """
    Determine if the ball has been pushed according to the set threshold value

    :param untouched_ball_y: The read y value of a non pushed ball
    :param threshold:  The y threashold
    :param y: y coordinate for the current ball
    :return: Returns True if the ball has been pushed
    """
    return not (untouched_ball_y - threshold < y < untouched_ball_y + threshold)


def get_frame_count(video_path):
    """
    Reads the frame count in order to use the tqdm progressbar.
    This value can not be directly read due to the .h264 video files that are used does not contain ths information in
    the metadata.

    :param video_path: The video path
    :return: The number of frames
    """
    video_capture = cv2.VideoCapture(video_path)

    count = 0
    while (True):
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            break

        count += 1

    video_capture.release()
    cv2.destroyAllWindows()
    return count
    # When everything done, release the capture
