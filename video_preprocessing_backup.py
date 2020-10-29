import numpy as np
import argparse
import imutils
import cv2
import pandas as pd
import time
from alive_progress import alive_bar
from tqdm import trange
import ffmpeg
from matplotlib import pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="-inn (input video)")
ap.add_argument("-o", "--output", required=True, help="-output (output video)")

args = vars(ap.parse_args())

video_path = args['input']
cropped_path = video_path.split(".")[0] + "_cropped.mp4"
print('cropped: ', cropped_path)
video_output = args['output']

start_time = time.time()

#Initial videoconvertion
# (
#     ffmpeg
#     .input(video_path)
#     # .filter('crop', 'in_w-440', 'in_h-140', 'in_w-out_w-180', 'in_h-out_h-25')
#     .output(cropped_path)
#     .run()
# )

print('Initial processing completed')


greenLower = np.array([0, 0, 180])
greenUpper = np.array([255, 255, 255])

# Creating a Pandas DataFrame To Store Data Point
original_frame = 1
new_frame = 1
Data_Features = ['frame', 'original_frame', 'x', 'y', 'radius']
list_of_rows = []

frames_with_light = []

df = pd.DataFrame(data=None, columns=Data_Features)

cropped_path = video_path
video = cv2.VideoCapture(cropped_path)

# width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# min_y = int(height / 2)




(grabbed, frame) = video.read()
fromCenter = False

r = cv2.selectROI('Crop', frame, fromCenter)
cv2.waitKey(0) # close window when a key press is detected
cv2.destroyWindow('Crop') # <-- Does not work on mac .......
print(r)


# print(r)
fps = int(video.get(cv2.CAP_PROP_FPS))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
height, width = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])].shape[:2]
min_y = int(height / 2)

# imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
#
# cv2.imshow("Image", imCrop)


out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), 0)

print(f'Video metadata:\nfps: {fps} \nheight: {height}\nwidth: {width}')
print('Extracting frames with light on using openCV ..')

with alive_bar(0) as bar:
    while True:
        bar()
        (grabbed, frame) = video.read()

        if not grabbed:
            break
        frame = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
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

            if radius > 5: #and y > min_y:
                new_row = {'frame': new_frame,
                           'original_frame': original_frame,
                           'time (s)': original_frame / fps,
                           'x': x,
                           'y': y,
                           'radius': radius}
                list_of_rows.append(new_row)
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


                # cv2.imshow("Frame", frame)
                # cv2.imshow("Normalized", normalized)
                #
                # key = cv2.waitKey(1) & 0xFF
                #
                # if key == ord("q"):
                #     break



out.release()
video.release()
# cv2.destroyAllWindows()
#
# Populate and save pandas dataframe
df = pd.DataFrame(list_of_rows)

store = pd.HDFStore(f'{str(video_path)}.h5')
store.append(video_path, df, data_columns=['int32', 'int32', 'int64', 'string'])
store.close()

# # Extract the intervals to optimize ffmpeg cropping
# print('Extract the intervals to optimize ffmpeg cropping')
# frames_to_extract = []
# new_line = {'start': -2, 'stop': -2}
# for i in trange(len(df)):
#     original_frame = int(df.loc[i]['original_frame'])
#     if new_line.get('start') == -2:
#         new_line['start'] = original_frame
#     elif new_line['stop'] == -2 or new_line['stop'] == original_frame - 1:
#         new_line['stop'] = original_frame
#     else:
#         frames_to_extract.append(new_line)
#         new_line = new_line = {'start': original_frame, 'stop': -2}
#
#
#
# # Crop the videofile
# stream = ffmpeg.input(cropped_path)
# new_stream = ffmpeg.trim(stream, start_frame=0, end_frame=0)
#
# print('Making new videofile with frames when light is on ..')
# for i in trange(len(frames_to_extract)):
#     trimmed_section = ffmpeg.trim(stream, start_frame=frames_to_extract[i]['start'],
#                                   end_frame=frames_to_extract[i]['stop']).setpts('PTS-STARTPTS')
#     new_stream = ffmpeg.concat(new_stream, trimmed_section)\
#         .hue(h=0, s=0, b=0.1)
#
# new_stream = ffmpeg.output(new_stream, video_output)
# ffmpeg.run(new_stream)
#
# elapsed_time = time.time() - start_time
# print(f"Process succeeded in {elapsed_time}s")
