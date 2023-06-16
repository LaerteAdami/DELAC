from Mesh.mesh_generation import generate_mesh
import subprocess

args_mesh = {'width': 4,
             'length': 22,
             'bottom_distance': 2,
             'front_distance': 2,
             'coarse_distance': 5,
             # Size of the mesh
             'cylinder_size': 0.05,
             'box_size': 0.2,
             'coarse_size': 0.5}

template_mesh = 'geometry_2d.template_geo'

mesh_flag = False  # True is create the mesh from scratch

if mesh_flag:
    # Create the mesh
    generate_mesh(args_mesh, template_mesh)

    # Visualise the mesh
    # subprocess.call("gmsh %s" % "geometry_2d.msh")

# Aero simulation
subprocess.call("turtleFSI --problem aero_demo", shell=True)
