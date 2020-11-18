import numpy as np
import imutils
import cv2
from tqdm import trange
import tqdm


def video_preprocess(video_input_path, crop_ratio, gui_handler,  extract_pushed_balls=True, threshold=2):
    video_output_path = video_input_path.split('.')[
                            0] + '_preprocessed.mp4'  # filedialog.asksaveasfilename(initialdir=sys.path[0], title='Select ')

    # crop_ratio = gui_handler.crop_ratio
    # max_y_observer = gui_handler.max_y_observer
    gui_handler.update_console('Getting the frame count..')
    frame_count = get_frame_count(video_input_path)
    gui_handler.set_progress(15)

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

    cropped_frame = frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
                    int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]

    # Getting the video parameters
    fps = int(video.get(cv2.CAP_PROP_FPS))
    # total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # height, width = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])].shape[:2]
    height, width = cropped_frame.shape[:2]
    min_y = int(height / 2)

    # Setting the video output writer
    out = cv2.VideoWriter(video_output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), 0)

    gui_handler.update_console(f'Video metadata after cropping:\nfps: {fps} \nheight: {height}\nwidth: {width}')
    print(f'Video metadata after cropping:\nfps: {fps} \nheight: {height}\nwidth: {width}')
    gui_handler.update_console('Extracting frames with light on using openCV:')
    print('Extracting frames with light on using openCV ...')

    untouched_ball_y = 0

    # with alive_bar(0) as bar:
    #     while True:
    #         bar()

    # @staticmethod
    # tqdm.format_meter(n, total, elapsed, ncols=None, prefix='', ascii=False, unit='it', unit_scale=False, rate=None,
    #                bar_format=None, postfix=None, unit_divisor=1000, initial=0, colour=None, **extra_kwargs)
    for i in trange(frame_count - 1, ncols=75, unit='frames'):

        if i % 1000 == 0:
            gui_handler.set_progress(15 + (i / frame_count) * 50)
        (grabbed, frame) = video.read()

        if not grabbed:
            break
        frame = frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
                int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]
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

                if not (untouched_ball_y - threshold < y < untouched_ball_y + threshold) \
                        or not extract_pushed_balls:
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

                    # kernel_sharpening = np.array([[-1, -1, -1],
                    #                               [-1, 9, -1],
                    #                               [-1, -1, -1]])
                    # # applying the sharpening kernel to the input image & displaying it.
                    # filtered_frame = cv2.filter2D(filtered_frame, -1, kernel_sharpening)
                    # # filtered_frame = cv2.GaussianBlur(filtered_frame, (3, 3), 1)
                    # filtered_frame = cv2.fastNlMeansDenoising(filtered_frame, None, 12, 7, 21)

                    filtered_frame = cv2.normalize(filtered_frame, None, 0, 500, cv2.NORM_MINMAX)
                    # alpha = 2  # Contrast control (1.0-3.0)
                    # beta = 0  # Brightness control (0-100)
                    # filtered_frame = cv2.convertScaleAbs(filtered_frame, alpha=alpha, beta=beta)
                    out.write(filtered_frame)

    out.release()
    video.release()

    # plot ball location
    # plot_posistion(ball_location)
    cv2.imshow('cv2 bug..', np.zeros((512, 512, 3), np.uint8))
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print(f'Success! Extracted {new_frame} frames.')

    return ball_location, video_output_path


def get_frame_count(video_path):
    video_capture = cv2.VideoCapture(video_path)
    # video_length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

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


