import os
import subprocess

args = {'width': 4.1,
        'box_size': 0.5,
        'length': 22,
        'bottom_distance': 2,
        'cylinder_size': 0.2,
        'front_distance': 2,
        'coarse_distance': 5,
        'coarse_size': 1}

template = 'geometry_2d.template_geo'
'''Modify template according args and make gmsh generate the mesh'''
assert os.path.exists(template)

with open(template, 'r') as f:
    old = f.readlines()

output = template

cmd = 'gmsh -0 %s ' % output

list_geometric_parameters = ['width', 'box_size', 'length',
                             'bottom_distance', 'cylinder_size', 'front_distance',
                             'coarse_distance', 'coarse_size']

constants = " "

for crrt_param in list_geometric_parameters:
    constants = constants + " -setnumber " + crrt_param + " " + str(args[crrt_param])

print(constants)
# Unrolled model
subprocess.call(cmd + constants, shell=True)

unrolled = 'geometry_2d.geo_unrolled'

dim = 2
scale = 1

subprocess.call(['gmsh -%d -clscale %g %s' % (dim, scale, unrolled)], shell=True)
