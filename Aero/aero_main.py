from Mesh.mesh_generation import create_mesh
import subprocess
from utils import *

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


# template_mesh = '../Mesh/geometry_2d.template_geo'


def generate_mesh(template_mesh):
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
                 'flap_len': 1,
                 'flap_width': 0.1
                 }
    # Create the mesh
    create_mesh(args_mesh, template_mesh)

    print("##########################")
    print("####  MESH GENERATED  ####")
    print("##########################")

    # Visualise the mesh
    # subprocess.call("gmsh %s" % "geometry_2d.msh")


def aero_startup(T_startup, folder, train_agent):
    subprocess.call("turtleFSI --problem run_aero -T {} "
                    " --folder {} "
                    "--new-arguments T_control={} "
                    "train_agent={}".format(T_startup, folder, 0, train_agent), shell=True)
    print("##########################")
    print("### START UP COMPLETED ###")
    print("##########################")


def aero_step(restart_folder, rho, T_control, train_agent):
    subprocess.call("turtleFSI --problem run_aero "
                    "--restart-folder {} "
                    "--rho-s {} "
                    "--new-arguments T_control={} "
                    "train_agent={}".format(restart_folder, rho, T_control, train_agent), shell=True)


def aero_test():
    folder = "../Aero/Results/test_restart/t1"
    restart_folder = "../Aero/Results/test_restart/t1"
    T_startup = 0.5
    dt_control = 0.5
    counter = 1
    T_control = T_startup + counter * dt_control

    subprocess.call("turtleFSI --problem run_aero -T {} "
                    " --folder {} "
                    "--new-arguments T_control={}".format(T_startup, folder, 0), shell=True)

    create_history(restart_folder)
    subprocess.call("turtleFSI --problem run_aero "
                    "--restart-folder {} "
                    "--new-arguments T_control={}".format(restart_folder, T_control), shell=True)

    update_history(restart_folder)
