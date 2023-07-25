from Mesh.mesh_generation import generate_mesh
import subprocess

mesh_flag = False  # True to create the mesh from scratch
aero_flag = True
# Mesh parameters tuned in the mesh convergence analysis phase
delta = 1  # 2, 1, 0.5
len_delta = 0.75  # 1, 0.75, 0.5

# Mesh dimension
length = 15 * len_delta
outer_length = 30 * len_delta

# Mesh size
cylinder_size = 0.1 * delta
box_size = 0.5 * delta
coarse_size = 1 * delta

args_mesh = {'width': 5,
             'length': length,
             'bottom_distance': 2.5,
             'front_distance': 3,
             'outer_length': outer_length,
             # Size of the mesh
             'cylinder_size': cylinder_size,
             'box_size': box_size,
             'coarse_size': coarse_size,
             # Flaps parameters
             'beta': 0,
             'flap_len': 1.5,
             'flap_width': 0.2
             }

template_mesh = '../Mesh/geometry_2d.template_geo'

if mesh_flag:
    # Create the mesh
    generate_mesh(args_mesh, template_mesh)

    # Visualise the mesh
    # subprocess.call("gmsh %s" % "geometry_2d.msh")

# Aero simulation
if aero_flag:
    subprocess.call("turtleFSI --problem aero_demo", shell=True)
