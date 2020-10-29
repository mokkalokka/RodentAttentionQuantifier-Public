import numpy as np
import matplotlib.pyplot as plt


def get_angles(list_of_rows):
    angle = []
    binocular_40 = 0
    binocular_110 = 0
    binocular_176 = 0
    for i in range(len(list_of_rows)):

        vector_1 = [list_of_rows[i]['o_snout_x'] - list_of_rows[i]['o_centroid_x'],
                    list_of_rows[i]['o_snout_y'] - list_of_rows[i]['o_centroid_y']]

        vector_2 = [list_of_rows[i]['t_centroid_x'] - list_of_rows[i]['o_centroid_x'],
                    list_of_rows[i]['t_centroid_y'] - list_of_rows[i]['o_centroid_y']]

        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle.append(np.rad2deg(np.arccos(dot_product)))
        binocular_40 += angle[-1] < 20
        binocular_110 += 20 < angle[-1] <= 55  # in range(20, 55)
        binocular_176 += 55 < angle[-1] <= 88

        list_of_rows[i]['angle'] = angle[-1]

    binocular_40 = binocular_40 / len(angle)
    binocular_110 = binocular_110 / len(angle)
    binocular_176 = binocular_176 / len(angle)
    print(f'binocular40 score: {binocular_40}')
    print(f'binocular110 score: {binocular_110}')
    print(f'binocular176 score: {binocular_176}')
    # plt.plot(angle)
    # plt.xlabel('Frame', fontsize=18)
    # plt.ylabel('Angle', fontsize=18)
    # plt.show()

    return list_of_rows

