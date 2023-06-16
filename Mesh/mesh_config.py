# Configuration file to create the mesh for the problem
#
# There are 3 cases, with corresponding inputs:
# - circle: radius, center
# - square: side length, center
# - polygon: vertices

import gmsh
import sys
import os, subprocess


args = {'width': 4,
        'length': 22,
        'bottom_distance': 2,
        'front_distance': 2,
        'coarse_distance': 5,
        # Size of the mesh
        'cylinder_size': 0.05,
        'box_size': 0.2,
        'coarse_size': 0.5}


# subprocess.call("turtleFSI --problem aero_demo", shell=True)
