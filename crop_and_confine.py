import cv2


def crop_and_confine(video_input_path):
    # Initializing OpenCV video capture
    video = cv2.VideoCapture(video_input_path)

    # Grab first frame and open GUI for cropping
    (grabbed, frame) = video.read()
    fromCenter = False
    # gui_handler.update_console('Crop the video')
    crop_ratio = cv2.selectROI('Crop', frame, fromCenter)
    # gui_handler.crop_ratio = crop_ratio
    cv2.waitKey(0)  # close window when a key press is detected
    cv2.destroyWindow('Crop')  # <-- Does not work on mac .......

    cropped_frame = frame[int(crop_ratio[1]):int(crop_ratio[1] + crop_ratio[3]),
                    int(crop_ratio[0]):int(crop_ratio[0] + crop_ratio[2])]

    # gui_handler.update_console('Select area where the observer is confined to')

    observer_area = cv2.selectROI('Confine observer', cropped_frame, fromCenter)
    cv2.destroyAllWindows()

    max_y_observer = int(observer_area[1] + observer_area[3])
    # gui_handler.max_y_observer = max_y_observer
    print(f'Observer confined to: {observer_area}')
    # gui_handler.update_console(f'Observer confined to: {observer_area}')
    print(f'y_max: {max_y_observer}')

    video.release()
    return crop_ratio, max_y_observer
