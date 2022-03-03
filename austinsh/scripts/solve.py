import sys
from turtle import settiltangle
from more_itertools import collapse, flatten
sys.path.append("..")
import numpy as np
from lib.parse_json import parse_json
from lib.initialize import initialize
from classes import Nodes
from classes import Resistors
import matplotlib.pyplot as plt
# from scripts.run_time_domain_simulation import run_time_domain_simulation
# from scripts.process_results import process_results
def solve(TESTCASE, SETTINGS):
    """Run the power flow solver.
    Args:
        TESTCASE (str): A string with the path to the network json file.
        SETTINGS (dict): Contains all the solver settings in a dictionary.
    Returns:
        None
    """

    # # # Parse the test case data # # #
    # TODO: STEP 0 - Initialize all the model classes in the models directory (models/) and familiarize
    # yourself with the parameters of each model.
    case_name = TESTCASE
    devices = parse_json(case_name)

    # # # Unpack parsed device objects in case you need them # # #
    nodes = devices['nodes']
    voltage_sources = devices['voltage_sources']
    resistors = devices['resistors']
    capacitors = devices['capacitors']
    inductors = devices['inductors']
    switches = devices['switches']
    induction_motors = devices['induction_motors']

    # # # Solver settings # # #
    t_final = SETTINGS['Simulation Time']
    tol = SETTINGS['Tolerance']  # NR solver tolerance
    max_iters = SETTINGS['Max Iters']  # maximum NR iterations
    t_initial = 0
    t = t_initial

    # # # Assign system nodes # # #
    # We assign a node index for every node in our Y matrix and J vector.
    # In addition to voltages, nodes track currents of voltage sources and
    # other state variables needed for companion models or the model of the 
    # induction motor.
    # You can determine the size of the Y matrix by looking at the total
    # number of nodes in the system.
    size_Y = Nodes.node_index_counter

    print(resistors)
    print(len(resistors))
    print(resistors[0])
    def solver(Y_matrix, J_matrix, vecotrs, t):
        # Start stamping the models
        for elem in range(len(resistors)):
            Y_matrix = resistors[elem].stamp_dense(Y_matrix)
            print(Y_matrix)
        for elem in range(len(inductors)):
            Y_matrix, J_matrix = inductors[elem].stamp_dense(Y_matrix, J_matrix, vectors, t)
            print(Y_matrix)
            print(J_matrix)
        for elem in range(len(voltage_sources)):
            Y_matrix, J_matrix = voltage_sources[elem].stamp_dense(Y_matrix, J_matrix, t)
        # Get rid of the ground row and column because otherwise it will create a singular
        # matrix and it is just the reference point anyways
        Y_matrix = np.delete(Y_matrix, 0, 1)
        Y_matrix = np.delete(Y_matrix, 0, 0)
        J_matrix = np.delete(J_matrix, 0, 0)
        # Solve the linear system for v(t) = Y^(-1)J
        solution = np.linalg.solve(Y_matrix, J_matrix)
        # Create a list of the solutions
        vectors.append(solution)
        # Incriment the time to the next time step
        t += SETTINGS["Time Step"]
        return vectors, t
    
    while t <= t_final:
        # Initialize a solution list
        if t == 0:
            vectors = []
        # Initialize the matrices Y and J to be stamped at the current timestep
        Y_matrix = np.zeros((size_Y, size_Y))
        J_matrix = np.zeros(size_Y)
        # Produce the list of solution vectors
        vectors, t = solver(Y_matrix, J_matrix, vectors, t)
    
    vectors = np.array(vectors)
    for i in range(vectors.shape[1] - 1):
        vector_adj = vectors[:,i]
        vector_adj = vector_adj.flat
        plt.plot(np.arange(t_initial, t_final, SETTINGS["Time Step"]), np.array(vector_adj))
    plt.show()

    # # # Initialize solution vector # # #
    # TODO: STEP 1 - Complete the function to find your state vector at time t=0.
    # V_init = initialize(devices, size_Y)

    # TODO: STEP 2 - Run the time domain simulation and return an array that contains
    #                time domain waveforms of all the state variables # # #
    # V_waveform = run_time_domain_simulation(devices, V_init, size_Y, SETTINGS)

    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process results function to compute the relevant results (voltage and current
    # waveforms, steady state values, etc.), plot them, and compare your output to the waveforms produced by Simulink
    # process_results(V_waveform, devices)