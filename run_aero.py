"""
Problem file for running the 2D cylinder problem with control flaps

The main structure is taken from https://github.com/KVSlab/turtleFSI/blob/master/turtleFSI/problems/turtle_demo.py
It has been modified for the problem considered
"""

from dolfin import *
from os import path
from turtleFSI.problems import *
from turtleFSI.modules import *
import numpy as np
from mpi4py import MPI as pyMPI

parameters["ghost_mode"] = "shared_facet"


def set_problem_parameters(default_variables, **namespace):
    # Overwrite or add new variables to 'default_variables'
    s = 1  # Side length [m]
    Re = 150  # Reynolds number [-]
    u_inf = 1.0  # Free-stream flow velocity in [m/s]
    rho_f = 1.225  # Fluid density [kg/m^3]
    mu_f = rho_f * u_inf * s / Re  # Fluid dynamic viscosity [Pa.s]

    default_variables.update(dict(

        # Geometric variables
        s=s,  # Side length
        H=4,  # Total height
        L=22.5,  # Length of domain
        c_x=0,  # Center of the square x-direction
        c_y=0,  # Center of the square y-direction
        flap=1,  # Length of the flap
        flap_width=0.1,  # Width of the flap

        # Temporal variables
        T=0.1,  # End time [s]
        T_control=0.1,  # Time interval of control [s]
        dt=0.1,  # Numerical time step [s]
        theta=0.5,  # Temporal scheme: second-order CN scheme

        # Fluid physical constants
        u_inf=u_inf,  # Inlet velocity: 1.0 [m/s]
        rho_f=rho_f,  # Fluid density [kg/m3]
        Re=Re,  # Reynold number
        mu_f=mu_f,  # Fluid dynamic viscosity [Pa.s]

        # Solid physical constants
        rho_s=5e5,  # Solid density[kg/m3]

        # Problem specific
        folder="Results/TEST",  # Name of the default results folder
        sub_folder="t1",  # Name of the default results sub-folder
        extrapolation="biharmonic",  # Bi-harmonic extrapolation of displacements
        extrapolation_sub_type="constrained_disp_vel",  # Bi-harmonic type
        bc_ids=[1, 2, 3, 4],  # Ids of makers for the mesh extrapolation

        # Solver settings
        recompute=2,  # Compute the Jacobian matrix every iteration
        checkpoint_step=5,
        save_step=1e10,
        verbose=False
    ))
    default_variables["compiler_parameters"].update({"quadrature_degree": 5})

    return default_variables


def get_mesh_domain_and_boundaries(L, s, flap, flap_width, **namespace):
    # Read mesh
    xml_file = path.join(path.dirname(path.abspath(__file__)), "Mesh", "geometry_2d.xml")
    mesh = Mesh(xml_file)

    # Define boundaries
    Inlet = AutoSubDomain(lambda x: near(x[0], -L / 2))
    Outlet = AutoSubDomain(lambda x: (near(x[0], +L / 2)))
    Walls = AutoSubDomain(lambda x: (x[1] >= L / 2) or (x[1] <= -L / 2))

    # Define square, neglecting flaps
    Square = AutoSubDomain(lambda x: ((near(x[1], -s / 2) or
                                       near(x[1], s / 2)) and x[0] < s / 2) or
                                     near(x[0], -s / 2) or
                                     near(x[0], s / 2)
                           )

    # Define flaps boundaries
    Flaps = AutoSubDomain(lambda x: near(x[0], s / 2 + flap) or
                                    (near(x[1], s / 2) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], s / 2 - flap_width) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], - s / 2 + flap_width) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], - s / 2) and s / 2 <= x[0] <= s / 2 + flap)
                          )

    # Define walls between the square and the flaps
    Flaps_wall_up = AutoSubDomain(lambda x: (near(x[0], s / 2) and (s / 2 - flap_width) <= x[1] <= s / 2))
    Flaps_wall_down = AutoSubDomain(lambda x: near(x[0], s / 2) and -s / 1 <= x[1] <= (-s / 2 + flap_width))

    # Mark the boundaries
    All_boundaries = DomainBoundary()
    boundaries = MeshFunction("size_t", mesh, mesh.geometry().dim() - 1)
    boundaries.set_all(0)
    All_boundaries.mark(boundaries, 7)
    Inlet.mark(boundaries, 1)  # Inlet
    Walls.mark(boundaries, 2)  # Up and down walls
    Outlet.mark(boundaries, 3)  # Outlet
    Square.mark(boundaries, 4)  # Square
    Flaps.mark(boundaries, 5)  # Flaps
    Flaps_wall_up.mark(boundaries, 6)  # Flap wall
    Flaps_wall_down.mark(boundaries, 6)  # Flap wall

    # Define flap domains
    Flaps_up = AutoSubDomain(lambda x: (s / 2 + flap >= x[0] >= s / 2 >= x[1] >= s / 2 - flap_width))
    Flaps_down = AutoSubDomain(lambda x: s / 2 <= x[0] <= s / 2 + flap and -s / 2 <= x[1] <= -s / 2 + flap_width)

    domains = MeshFunction("size_t", mesh, mesh.geometry().dim())
    domains.set_all(1)
    Flaps_up.mark(domains, 2)
    Flaps_down.mark(domains, 2)

    # Save file with boundary labels
    # File("../Mesh/mesh_boundaries.pvd").write(boundaries)
    # File("../Mesh/mesh_domains.pvd").write(domains)

    return mesh, domains, boundaries


def initiate(T_new, T):
    # Coordinate for sampling statistics
    # SELECT THE CORRECT CASE ACCORDING TO LINE 26 OF MAIN.PY
    probes = [[2, -0.5],  # 1
              [2, 0],  # 2
              [2, 0.5],  # 3
              [2.5, -0.5],  # 4
              [2.5, 0],  # 5
              [2.5, 0.5],  # 6
              [3, -0.5],  # 7
              [3, 0],  # 8
              [3, 0.5],  # 9
              [3.5, -0.5],  # 10
              [3.5, 0],  # 11
              [3.5, 0.5],  # 12
              [4, -0.5],  # 13
              [4, 0],  # 14
              [4, 0.5]  # 15
              ]
    probes = [[2, 0],  # 1
              [2.5, 0],  # 2
              [3, 0],  # 3
              [3.5, 0],  # 4
              [4, 0]  # 5
              ]

    if T_new != 0:
        T = float(T_new)
    else:
        T = T

    # Lists to hold results - displacements along x and y, drag, time and pressures
    displacement_x_list = []
    displacement_y_list = []
    drag_list = []
    time_list = []

    pres_list = []

    return dict(T=T, displacement_x_list=displacement_x_list, displacement_y_list=displacement_y_list,
                drag_list=drag_list, time_list=time_list, probes=probes, pres_list=pres_list)


def create_bcs(DVP, u_inf, boundaries, extrapolation_sub_type, **namespace):
    no_slip = (0.0, 0.0)  # No penetration, no slip condition
    # Fluid velocity conditions
    u_inlet = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 1)
    u_wall = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 2)
    u_square = DirichletBC(DVP.sub(1), no_slip, boundaries, 4)
    u_flaps_wall = DirichletBC(DVP.sub(1), no_slip, boundaries, 6)

    bcs = [u_square, u_inlet, u_wall, u_flaps_wall]

    d_wall = DirichletBC(DVP.sub(0), no_slip, boundaries, 2)
    d_inlet = DirichletBC(DVP.sub(0), no_slip, boundaries, 1)
    d_outlet = DirichletBC(DVP.sub(0), no_slip, boundaries, 3)
    d_square = DirichletBC(DVP.sub(0), no_slip, boundaries, 4)
    d_flaps_wall = DirichletBC(DVP.sub(0), no_slip, boundaries, 6)
    for i in [d_wall, d_inlet, d_outlet, d_square, d_flaps_wall]:
        bcs.append(i)

    # Boundary conditions on the displacement / extrapolation
    if extrapolation_sub_type == "constrained_disp_vel":

        w_wall = DirichletBC(DVP.sub(3), no_slip, boundaries, 2)
        w_inlet = DirichletBC(DVP.sub(3), no_slip, boundaries, 1)
        w_outlet = DirichletBC(DVP.sub(3), no_slip, boundaries, 3)
        w_square = DirichletBC(DVP.sub(3), no_slip, boundaries, 4)
        w_flaps_wall = DirichletBC(DVP.sub(3), no_slip, boundaries, 6)

        for i in [w_wall, w_inlet, w_outlet, w_square, w_flaps_wall]:
            bcs.append(i)

    return dict(bcs=bcs)

################################################################################
# The next two methods are taken as they are from
# https://github.com/KVSlab/turtleFSI/blob/master/turtleFSI/problems/turtle_demo.py
def mpi4py_comm(comm):
    """Get mpi4py communicator"""
    try:
        return comm.tompi4py()
    except AttributeError:
        return comm


def peval(f, x):
    """Parallel synced eval"""
    try:
        yloc = f(x)
    except RuntimeError:
        yloc = np.inf * np.ones(f.value_shape())

    comm = mpi4py_comm(f.function_space().mesh().mpi_comm())
    yglob = np.zeros_like(yloc)
    comm.Allreduce(yloc, yglob, op=pyMPI.MIN)

    return yglob


def post_solve(t, dvp_, n, drag_list, time_list, probes, pres_list, mu_f, verbose, ds, **namespace):
    # Get deformation, velocity, and pressure
    d = dvp_["n"].sub(0, deepcopy=True)
    v = dvp_["n"].sub(1, deepcopy=True)
    p = dvp_["n"].sub(2, deepcopy=True)

    # Compute forces
    force = dot(sigma(v, p, d, mu_f), n)
    drag_list.append(-assemble(force[0] * ds(4)))
    time_list.append(t)

    for coord in probes:
        p_eval = peval(d, coord)
        pres_list.append(p_eval[0])

    # Print results
    if verbose:
        print("Drag: {:e}".format(drag_list[-1]))


def finished(drag_list, time_list, pres_list, results_folder, **namespace):
    # Store results when the computation is finished

    np.savetxt(path.join(results_folder, 'Drag.txt'), drag_list, delimiter=',')
    np.savetxt(path.join(results_folder, 'Time.txt'), time_list, delimiter=',')
    np.savetxt(path.join(results_folder, 'Pressure.txt'), pres_list, delimiter=',')
