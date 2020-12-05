import time

from file_handler import move_files_to_dir, delete_analysis_temp_files
from log_to_file import log_to_file
from plot_angle_on_video import plot_angle_on_video
from process_angle import get_angles, calculate_score
from read_tracklets import read_tracklets
from ma_dlc_controller import analyze_videos
from video_preprocessing import video_preprocess


def start_pipeline(video_paths, crop_ratio, max_y_observer, options, gui_handler):
    number_of_points = 0
    number_of_videos = len(video_paths)
    angles = []
    counter = 0
    observer = []
    performer = []
    result_txt = []



    # x.join()
    # gui_handler.update_console('\nCropping and confining .. ')

    # import time
    # for i in range(1000):
    #     gui_handler.update_console('\nsleeping .. ')
    #     print('sleeping 2.4 sec')
    #     time.sleep(2.4)

    # crop_ratio, max_y_observer = crop_and_confine(video_path)
    # crop_ratio = (0,0,640,480)
    # max_y_observer= 0
    for video_path in video_paths:

        gui_handler.set_progress(1/number_of_videos * 10)
        # Pre-processing video and get coordinates for ball with light
        gui_handler.update_console('\nStarting video preprocessing .. ')
        ball_location, preprocessed_video_path = video_preprocess(video_path,
                                                                  crop_ratio[counter],
                                                                  gui_handler,
                                                                  options)
        gui_handler.update_console('Done! ')
        # gui_handler.set_progress(40)

        # gui_handler.run_stdout_capture(True)

        #
        # # Analyze video with maDLC
        # Tk().withdraw()
        # #config_file_path = filedialog.askopenfilename(initialdir=sys.path[0], title='Select DLC config file:')
        config_file_path = 'data/config.yaml'
        # preprocessed_video_path = 'ObsLear_DudleyPriam_3_preprocessed.mp4'
        gui_handler.update_console('\nAnalysing the preprocessed video .. ')
        scorername = analyze_videos(config_file_path, preprocessed_video_path)
        gui_handler.update_console('Done!')
        gui_handler.set_progress(80)

        # scorername = ''

        # Reading the tracklet
        gui_handler.update_console('\nReading the tracklets ..')
        new_observer, new_performer = read_tracklets(scorername, preprocessed_video_path, max_y_observer[counter],
                                                     gui_handler)
        # gui_handler.update_console('Done!')
        observer.append(new_observer)
        performer.append(new_performer)
        gui_handler.set_progress(90)

        gui_handler.update_console('\nGetting the angles ...')
        # Calculate the angles between the two vectors [from_point, end_point_1] and [from_point, end_point_2]
        # gui_handler.run_stdout_capture(True)
        if options['focus'] == 'Ball with light':
            angles = get_angles(from_point=observer[-1].eyes,
                                end_point_1=observer[-1].snout,
                                end_point_2=ball_location,
                                angles=angles)
        else:
            angles = get_angles(from_point=observer[-1].eyes,
                                end_point_1=observer[-1].snout,
                                end_point_2=performer[-1].eyes,
                                angles=angles)
        from_index = number_of_points
        number_of_points = len(angles)
        to_index = number_of_points
        results = calculate_score(angles, from_index, to_index)

        filename = video_path.split('/')[-1]

        mode = options['mode']
        focus = options['focus']
        result_txt.append(f'\nAttention results for {filename}:' +
                          f'\nMode: {mode}' +
                          f'\nFocus: {focus} \n' +
                          f'\nTotal average angle: {results[0]}' +
                          f'\nbinocular40 score: {results[1]}' +
                          f'\nbinocular110 score: {results[2]}' +
                          f'\nbinocular176 score: {results[3]}' +
                          f'\nNumber of uncalculated angles: {results[4]}/ {to_index - from_index}' +
                          f'\nPercentage of uncalculated angles: {(results[4] / (to_index - from_index)) * 100 }\n')


        gui_handler.update_console(result_txt[-1], True)

        # if options['log']:
        #     gui_handler.update_console('\nlogging results to results.txt')
        #     log_to_file(results, video_path)

        if options['plot']:
            gui_handler.update_console('\nPlotting lines and angles on video')
            if options['focus'] == 'Ball with light':
                plot_angle_on_video(preprocessed_video_path,
                                    options,
                                    from_point=observer[-1].eyes,
                                    end_point_1=observer[-1].snout,
                                    end_point_2=ball_location,
                                    angles=angles[from_index:to_index])
            else:
                plot_angle_on_video(preprocessed_video_path,
                                    options,
                                    from_point=observer[-1].eyes,
                                    end_point_1=observer[-1].snout,
                                    end_point_2=performer[-1].eyes,
                                    angles=angles[from_index:to_index])
            move_files_to_dir(preprocessed_video_path)

        delete_analysis_temp_files(preprocessed_video_path)


        counter += 1

    if options['accumulate']:
        # Calculating the accumulative score:
        results = calculate_score(angles, from_index=0, to_index=number_of_points)

        result_txt.append(f'\nAccumulated attention results for all selected videos:' +
                          f'\nTotal average angle: {results[0]}' +
                          f'\nbinocular40 score: {results[1]}' +
                          f'\nbinocular110 score: {results[2]}' +
                          f'\nbinocular176 score: {results[3]}' +
                          f'\nNumber of uncalculated angles: {results[4]} / {number_of_points}' +
                          f'\nNumber of uncalculated angles: {(results[4] / number_of_points) * 100}\n')

        gui_handler.update_console('All results:\n', True)
        for res in result_txt:
            gui_handler.update_console(res)

    if options['log']:
        gui_handler.update_console('\nlogging results to results.txt')
        log_to_file(result_txt)

    # gui_handler.run_stdout_capture(False)
    # gui_handler.update_console('Done!')

    res = Results(observer, performer, angles, results, preprocessed_video_path)
    gui_handler.results = res

    gui_handler.update_console('\n\nPipeline finished!')
    gui_handler.set_progress(100)
    gui_handler.enable_buttons()
    # gui_handler.progress.stop()

    time.sleep(5)


class Results:
    def __init__(self, observer, performer, angles, result_txt, preprocessed_video_path):
        self.observer = observer
        self.performer = performer
        self.angles = angles
        self.result_txt = result_txt
        self.preprocessed_video_path = preprocessed_video_path
