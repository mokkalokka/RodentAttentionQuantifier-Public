import numpy as np


def get_angles(from_point, end_point_1, end_point_2, angles):

    for frame in range(len(from_point)):
        # print(frame, from_point[frame], end_point_1[frame], end_point_2[frame])
        if not (np.isnan(sum(list(from_point[frame].values()))) or
                np.isnan(sum(list(end_point_1[frame].values()))) or
                np.isnan(sum(list(end_point_2[frame].values())))):

            vector_1 = [end_point_1[frame]['x'] - from_point[frame]['x'],
                        end_point_1[frame]['y'] - from_point[frame]['y']]

            vector_2 = [end_point_2[frame]['x'] - from_point[frame]['x'],
                        end_point_2[frame]['y'] - from_point[frame]['y']]

            unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
            unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angles.append(np.rad2deg(np.arccos(dot_product)))

        else:
            angles.append(np.nan)

    return angles #, results


def calculate_score(angles, from_index, to_index):
    binocular_40 = 0
    binocular_110 = 0
    binocular_176 = 0
    uncalculated_angles = 0

    for i in range(from_index, to_index):
        if np.isnan(angles[i]):
            uncalculated_angles += 1

        binocular_40 += angles[i] < 20
        binocular_110 += 20 < angles[i] <= 55  # in range(20, 55)
        binocular_176 += 55 < angles[i] <= 88

    binocular_40 = binocular_40 / (to_index - from_index - uncalculated_angles)
    binocular_110 = binocular_110 / (to_index - from_index - uncalculated_angles)
    binocular_176 = binocular_176 / (to_index - from_index - uncalculated_angles)
    total_average = np.nanmean(angles[from_index:to_index - 1])

    # print(f'Total average angle: {total_average}')
    # print(f'binocular40 score: {binocular_40}')
    # print(f'binocular110 score: {binocular_110}')
    # print(f'binocular176 score: {binocular_176}')
    results = [total_average, binocular_40, binocular_110, binocular_176, uncalculated_angles]

    return results
