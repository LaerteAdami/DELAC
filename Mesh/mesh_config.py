# Configuration file to create the mesh for the problem
#
# There are 3 cases, with corresponding inputs:
# - circle: radius, center
# - square: side length, center
# - polygon: vertices

import gmsh
import sys
import os, subprocess

