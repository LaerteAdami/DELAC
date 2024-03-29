from Mesh.mesh_generation import create_mesh
import subprocess

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


def generate_mesh(template_mesh):
    """
    Generates the mesh given the parameters (same parameters of geometry_2d.template_geo)
    """
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
    """
    Start up procedure at the beginning of every episode
    """

    subprocess.call("turtleFSI --problem run_aero -T {} "
                    " --folder {} "
                    "--new-arguments T_control={} "
                    "train_agent={}".format(T_startup, folder, 0, train_agent), shell=True)
    print("##########################")
    print("### START UP COMPLETED ###")
    print("##########################")


def aero_step(restart_folder, rho, T_control, train_agent):
    """
    Calls the aerodynamic solver between two actions
    """
    subprocess.call("turtleFSI --problem run_aero "
                    "--restart-folder {} "
                    "--rho-s {} "
                    "--new-arguments T_control={} "
                    "train_agent={}".format(restart_folder, rho, T_control, train_agent), shell=True)


def aero_test():
    folder = "../Aero/Results/TESTTESTTEST/t1"
    T_startup = 1
    # subprocess.call("turtleFSI --problem test_run_aero -T {} "
    #                " --folder {} ".format(T_startup, folder), shell=True)

    subprocess.call("turtleFSI --problem test_run_aero -T {} "
                    " --folder {} "
                    "--new-arguments T_control={} "
                    "train_agent={}".format(T_startup, folder, 0, True), shell=True)
