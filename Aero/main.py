from Mesh.mesh_generation import generate_mesh
import subprocess

args_mesh = {'width': 5,
             'length': 15,
             'bottom_distance': 2.5,
             'front_distance': 3,
             'outer_length': 30,
             # Size of the mesh
             'cylinder_size': 0.1,
             'box_size': 0.5,
             'coarse_size': 1}

template_mesh = '../Mesh/geometry_2d.template_geo'

mesh_flag = False  # True is create the mesh from scratch

if mesh_flag:
    # Create the mesh
    generate_mesh(args_mesh, template_mesh)

    # Visualise the mesh
    # subprocess.call("gmsh %s" % "geometry_2d.msh")

# Aero simulation
subprocess.call("turtleFSI --problem aero_demo", shell=True)
