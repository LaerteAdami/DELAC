"""
Problem file for running the 2D cylinder problem
"""

from dolfin import *
from os import path
from turtleFSI.problems import *
from turtleFSI.modules import *
import numpy as np

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
        # f_dist=2,  # distance from the inlet
        # b_dist=2,  # distance from the bottom wall
        H=4,  # Total height
        R=1,  # Radius of the circle
        L=22.5,  # Length of domain
        c_x=0,  # Center of the circle x-direction
        c_y=0,  # Center of the circle y-direction

        # Temporal variables
        T=100,  # End time [s]
        dt=0.1,  # Time step [s]
        theta=0.5,  # Temporal scheme: second-order Crank-Nicolson scheme

        # Physical constants ('FSI 3')
        u_inf=u_inf,  # Inlet velocity: 1.0 [m/s]
        rho_f=rho_f,  # Fluid density [kg/m3]
        Re=Re,  # Reynold number
        mu_f=mu_f,  # Fluid dynamic viscosity [Pa.s]

        # Problem specific
        folder="Results/TEST_FLAP",  # Name of the results folder
        solid="no_solid",  # Do not solve for the solid
        extrapolation="no_extrapolation",  # No displacement to extrapolate

        # Solver settings
        recompute=1,  # Compute the Jacobian matrix every iteration
        checkpoint_step=4
    ))
    default_variables["compiler_parameters"].update({"quadrature_degree": 5})

    return default_variables


def get_mesh_domain_and_boundaries(L, **namespace):
    # Read mesh
    xml_file = path.join(path.dirname(path.abspath(__file__)), "../Mesh", "NEW_geometry_2d.xml")
    mesh = Mesh(xml_file)

    # Define boundaries
    Inlet = AutoSubDomain(lambda x: near(x[0], -L / 2))
    Outlet = AutoSubDomain(lambda x: (near(x[0], +L / 2)))
    Walls = AutoSubDomain(lambda x: (x[1] >= L / 2) or (x[1] <= -L / 2))

    # Mark the boundaries
    All_boundaries = DomainBoundary()
    boundaries = MeshFunction("size_t", mesh, mesh.geometry().dim() - 1)
    boundaries.set_all(0)
    All_boundaries.mark(boundaries, 4)  # Square
    Inlet.mark(boundaries, 1)
    Walls.mark(boundaries, 2)
    Outlet.mark(boundaries, 3)

    # Define and mark domains
    domains = MeshFunction("size_t", mesh, mesh.geometry().dim())
    domains.set_all(1)

    # Save file with boundary labels
    # File("../Mesh/test_boundaries.pvd").write(boundaries)

    return mesh, domains, boundaries


def initiate(**namespace):
    # Coordinate for sampling statistics
    # coord = [c_x + R + f_dist, c_y]

    # Lists to hold displacement, forces, and time
    drag_list = []
    time_list = []

    # T = 2

    return dict(drag_list=drag_list, time_list=time_list)


def create_bcs(DVP, u_inf, boundaries, **namespace):
    no_slip = (0.0, 0.0)
    # Fluid velocity conditions
    u_inlet = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 1)
    u_wall = DirichletBC(DVP.sub(1), Constant((u_inf, 0)), boundaries, 2)
    u_square = DirichletBC(DVP.sub(1), (no_slip), boundaries, 4)

    # Pressure Conditions
    # p_out = DirichletBC(DVP.sub(2), 0, boundaries, 3)

    return dict(bcs=[u_square, u_inlet, u_wall])


def post_solve(t, dvp_, n, drag_list, time_list, mu_f, verbose, ds, **namespace):
    # Get deformation, velocity, and pressure
    d = dvp_["n"].sub(0, deepcopy=True)
    v = dvp_["n"].sub(1, deepcopy=True)
    p = dvp_["n"].sub(2, deepcopy=True)

    # Compute forces
    force = dot(sigma(v, p, d, mu_f), n)
    drag_list.append(-assemble(force[0] * ds(4)))
    time_list.append(t)

    # Print results
    if MPI.rank(MPI.comm_world) == 0 and verbose:
        print("Drag: {:e}".format(drag_list[-1]))


def finished(drag_list, time_list, results_folder, **namespace):
    # Store results when the computation is finished

    np.savetxt(path.join(results_folder, 'Drag.txt'), drag_list, delimiter=',')
    np.savetxt(path.join(results_folder, 'Time.txt'), time_list, delimiter=',')
