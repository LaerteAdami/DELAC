"""
Problem file for running the 2D cylinder problem with control flaps
"""

from dolfin import *
from os import path
from turtleFSI.problems import *
from turtleFSI.modules import *
import numpy as np
from mpi4py import MPI as pyMPI

parameters["ghost_mode"] = "shared_facet"


# _compiler_parameters = dict(parameters["form_compiler"])


def set_problem_parameters(default_variables, **namespace):
    # Overwrite or add new variables to 'default_variables'
    s = 1  # Side length [m]
    Re = 150  # Reynolds number [-]
    u_inf = 1.0  # Free-stream flow velocity in [m/s]
    rho_f = 1.225  # Fluid density [kg/m^3]
    mu_f = rho_f * u_inf * s / Re  # Fluid dynamic viscosity [Pa.s]

    default_variables.update(dict(

        # Geometric variables
        s=s,  # side length
        H=4,  # Total height
        R=1,  # Radius of the circle
        L=22.5,  # Length of domain
        c_x=0,  # Center of the circle x-direction
        c_y=0,  # Center of the circle y-direction
        flap=1.5,
        flap_width=0.2,

        # Temporal variables
        T=0.5,  # End time [s]
        dt=0.1,  # Time step [s]
        theta=0.5,  # Temporal scheme: second-order Crank-Nicolson scheme

        # Fluid physical constants
        u_inf=u_inf,  # Inlet velocity: 1.0 [m/s]
        rho_f=rho_f,  # Fluid density [kg/m3]
        Re=Re,  # Reynold number
        mu_f=mu_f,  # Fluid dynamic viscosity [Pa.s]

        # Solid physical constants
        rho_s=5e5,  # Solid density[kg/m3]
        # nu_s=0.281,  # Solid Poisson ratio [-]
        # mu_s=1E3,  # Shear modulus, CSM3: 0.5E6 [Pa]
        # lambda_s=4e5,  # Solid 1st Lame Coefficient [Pa]

        # Problem specific
        folder="Results/test_obs",  # Name of the results folder
        # solid="no_solid",  # Do not solve for the solid
        extrapolation="biharmonic",  # No displacement to extrapolate
        extrapolation_sub_type="constrained_disp_vel",  # Biharmonic type
        bc_ids=[1, 2, 3, 4],  # Ids of makers for the mesh extrapolation

        # Solver settings
        recompute=1,  # Compute the Jacobian matrix every iteration
        # checkpoint_step=4
    ))
    default_variables["compiler_parameters"].update({"quadrature_degree": 5})

    return default_variables


def get_mesh_domain_and_boundaries(L, s, flap, flap_width, **namespace):
    # Read mesh
    xml_file = path.join(path.dirname(path.abspath(__file__)), "../Mesh", "geometry_2d.xml")
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

    # Define and mark domains
    Flaps = AutoSubDomain(lambda x: near(x[0], s / 2 + flap) or
                                    (near(x[1], s / 2) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], s / 2 - flap_width) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], - s / 2 + flap_width) and s / 2 <= x[0] <= s / 2 + flap) or
                                    (near(x[1], - s / 2) and s / 2 <= x[0] <= s / 2 + flap)
                          )

    Flaps_wall_up = AutoSubDomain(lambda x: (near(x[0], s / 2) and (s / 2 - flap_width) <= x[1] <= s / 2))
    Flaps_wall_down = AutoSubDomain(lambda x: near(x[0], s / 2) and -s / 1 <= x[1] <= (-s / 2 + flap_width))

    # Mark the boundaries
    All_boundaries = DomainBoundary()
    boundaries = MeshFunction("size_t", mesh, mesh.geometry().dim() - 1)
    boundaries.set_all(0)
    All_boundaries.mark(boundaries, 7)
    Inlet.mark(boundaries, 1)
    Walls.mark(boundaries, 2)
    Outlet.mark(boundaries, 3)
    Square.mark(boundaries, 4)  # Square
    Flaps.mark(boundaries, 5)  # Flaps
    Flaps_wall_up.mark(boundaries, 6)  # Flap wall
    Flaps_wall_down.mark(boundaries, 6)  # Flap wall

    # Define and mark domains
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


def initiate(**namespace):
    # Coordinate for sampling statistics
    probes = [[-0.5, 0],
              [-1, 0]]

    # T = 2

    # Lists to hold displacement, forces, and time
    # Lists to hold results
    displacement_x_list = []
    displacement_y_list = []
    drag_list = []
    time_list = []

    pres_list = []

    return dict(displacement_x_list=displacement_x_list, displacement_y_list=displacement_y_list,
                drag_list=drag_list, time_list=time_list, probes=probes, pres_list=pres_list)


def create_bcs(DVP, u_inf, boundaries, extrapolation_sub_type, **namespace):
    no_slip = (0.0, 0.0)
    # Fluid velocity conditions
    u_inlet = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 1)
    u_wall = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 2)
    u_square = DirichletBC(DVP.sub(1), no_slip, boundaries, 4)
    u_flaps_wall = DirichletBC(DVP.sub(1), no_slip, boundaries, 6)

    # u_flaps = DirichletBC(DVP.sub(1), (no_slip), boundaries, 5)

    # Pressure Conditions
    # p_out = DirichletBC(DVP.sub(2), 0, boundaries, 3)

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
# the function mpi4py_comm and peval are used to overcome FEniCS limitation of
# evaluating functions at a given mesh point in parallel.
# https://fenicsproject.discourse.group/t/problem-with-evaluation-at-a-point-in
# -parallel/1188


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


################################################################################
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
