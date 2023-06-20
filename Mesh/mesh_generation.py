import os
import subprocess


def generate_mesh(args, template):

    output = template

    cmd = 'gmsh -0 %s ' % output

    list_geometric_parameters = ['width', 'box_size', 'length',
                                 'bottom_distance', 'cylinder_size', 'front_distance',
                                 'outer_length', 'coarse_size']

    constants = " "

    for crrt_param in list_geometric_parameters:
        constants = constants + " -setnumber " + crrt_param + " " + str(args[crrt_param])

    print(constants)
    # Unrolled model
    subprocess.call(cmd + constants, shell=True)

    unrolled = '../Mesh/geometry_2d.geo_unrolled'

    dim = 2
    scale = 1

    # Create the mesh
    subprocess.call(['gmsh -format msh2 -%d -clscale %g %s' % (dim, scale, unrolled)], shell=True)

    mesh_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "geometry_2d.msh")

    root, _ = os.path.splitext(mesh_path)

    # Get the xml mesh
    xml_file = '.'.join([root, 'xml'])
    subprocess.call(['dolfin-convert %s %s' % (mesh_path, xml_file)], shell=True)
