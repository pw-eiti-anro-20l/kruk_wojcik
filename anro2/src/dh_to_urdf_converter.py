#!/usr/bin/python

from collections import OrderedDict
from tf.transformations import *

dh = {'row1': [0, 1, 0, 0], 'row2': [0, 1, 1.57, 1.57], 'row3': [0, 1, 1.57, 1.57]}

def writeUrdfFile ():
    with open ('./src/anro2/config/urdf_data.yaml', 'w') as f:
        rowNumber = 1
        for row in dh:
            a, d, alpha, theta = dh [row]

            move_along_x = translation_matrix ((a, 0, 0))
            move_along_z = translation_matrix ((0, 0, d))
            
            rotate_around_x = rotation_matrix (alpha, (1, 0 ,0))
            rotate_around_z = rotation_matrix (theta, (0, 0, 1))

            transformation = concatenate_matrices (move_along_x, rotate_around_x, move_along_z, rotate_around_z)
            rpy = euler_from_matrix (transformation)
            xyz = translation_from_matrix (transformation)
            
            
            f.write("i{}:".format(rowNumber) + "\n")
            f.write("  j_xyz: {} {} {}".format(*xyz) + "\n")
            f.write("  j_rpy: {} {} {}".format(*rpy) + "\n")
            f.write("  l_xyz: {} {} {}".format(*xyz / 2) + "\n")
            f.write("  l_rpy: 0 0 0\n")
            f.write("  l_len: {}".format(d) + "\n")

            rowNumber += 1

if __name__ == "__main__":
    print ('converting dh to urdf...')
    writeUrdfFile ()
