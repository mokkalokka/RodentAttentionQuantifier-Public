import cv2
import numpy as np

video = cv2.VideoCapture('data/Obs30_DroAre_260920.h264')
counter = 0
while True:
    counter += 1
    (grabbed, frame) = video.read()
    if counter % 100 == 0:
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        # (hMin = 0 , sMin = 0, vMin = 37), (hMax = 179 , sMax = 255, vMax = 117)
        lowerHsv = (0, 0, 37)
        upperHsv = (179, 255, 117)
        mask = cv2.inRange(hsv, lowerHsv, upperHsv)
        output = cv2.bitwise_and(hsv, hsv, mask=mask)
        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)
        #
        # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # kernel = np.ones((3, 3), np.uint8)
        # erosion = cv2.erode(frame.copy(), kernel, iterations=1)
        # normalized = cv2.normalize(erosion, None, 0, 600, cv2.NORM_MINMAX)  # 255
        # gradient = cv2.morphologyEx(normalized, cv2.MORPH_GRADIENT, kernel)

        # normalized = cv2.normalize(mask, None, 0, 400, cv2.NORM_MINMAX)  # 255
        cv2.imshow('normalized', output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
