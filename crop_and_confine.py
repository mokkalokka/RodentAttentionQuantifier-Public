import cv2


def crop_and_confine(video_input_path):
    """
    Crops the video with a user prompted GUI, followed by a GUI for confining the observer

    :param video_input_path: Takes in the video path
    :return: Returns a crop ratio and the max y coordinate for observer
    """
    # Initializing OpenCV video capture
    video = cv2.VideoCapture(video_input_path)

    # Grab first frame and open GUI for cropping
    (grabbed, frame) = video.read()
    fromCenter = False
    crop_ratio = cv2.selectROI('Crop', frame, fromCenter)
    cv2.waitKey(0)  # close window when a key press is detected
    cv2.destroyWindow('Crop')  # <-- Does not work on mac .......

    cropped_frame = frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
                    int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]

    observer_area = cv2.selectROI('Confine observer', cropped_frame, fromCenter)
    cv2.destroyAllWindows()

    max_y_observer = int(observer_area[1] + observer_area[3])
    print(f'Observer confined to: {observer_area}')
    print(f'y_max: {max_y_observer}')

    video.release()
    return crop_ratio, max_y_observer
