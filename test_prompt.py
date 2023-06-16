# import os
# os.system(' ')
import subprocess
import os
from os import path
from dolfin import *

print("Start")

args = {'width': 4,
        'length': 22,
        'bottom_distance': 2,
        'front_distance': 2,
        'coarse_distance': 5,
        # Size of the mesh
        'cylinder_size': 0.05,
        'box_size': 0.2,
        'coarse_size': 0.5}

print(args.keys())



print("Done")
