import sys
sys.path.append("..")
import numpy as np
from lib.parse_json import parse_json
from classes import Nodes
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
    time_step = SETTINGS["Time Step"]
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

    def solver(Y_matrix, J_matrix, vecotrs, t, tol, max_iters, time_step, volt):
        # Start stamping the models
        for elem in range(len(resistors)):
            Y_matrix = resistors[elem].stamp_dense(Y_matrix)
        for elem in range(len(inductors)):
            Y_matrix, J_matrix = inductors[elem].stamp_dense(Y_matrix, J_matrix, vectors, t)
        for elem in range(len(voltage_sources)):
            Y_matrix, J_matrix, volt = voltage_sources[elem].stamp_dense(Y_matrix, J_matrix, t, volt)
        for elem in range(len(induction_motors)):
            reference = induction_motors[elem].stamp_dense(Y_matrix, J_matrix, vectors, t, tol, 
                                                            max_iters, time_step, volt)
        # Get rid of the ground row and column because otherwise it will create a singular
        # matrix and it is just the reference point anyways
        Y_matrix = np.delete(Y_matrix, 0, 1)
        Y_matrix = np.delete(Y_matrix, 0, 0)
        J_matrix = np.delete(J_matrix, 0, 0)
        if TESTCASE != "testcases/Simple_IM.json":
            # Solve the linear system for v(t) = Y^(-1)J
            solution = np.linalg.solve(Y_matrix, J_matrix)
            # Create a list of the solutions
            vectors.append(solution)
            # Incriment the time to the next time step
        else:
            vectors.append(reference)
        t += SETTINGS["Time Step"]
        return vectors, t
    
    while t <= t_final:
        # Initialize a solution list
        if t == 0:
            vectors = []
            volt = []
        # Initialize the matrices Y and J to be stamped at the current timestep
        Y_matrix = np.zeros((size_Y, size_Y))
        J_matrix = np.zeros(size_Y)
        # Produce the list of solution vectors
        vectors, t = solver(Y_matrix, J_matrix, vectors, t, tol, max_iters, time_step, volt)
    
    vectors = np.array(vectors)

    # for i in range(vectors.shape[1]):
    #     vector_adj = vectors[:,i]
    #     vector_adj = vector_adj.flat
    #     plt.plot(np.arange(t_initial, t_final, SETTINGS["Time Step"]), np.array(vector_adj))
    
    def get_by_name(name, legends, vectors):
        index = legends.index(name)
        vector_adj = vectors[:,index]
        vector_adj = vector_adj.flat
        return np.array(vector_adj)

    time = np.arange(t_initial, t_final, SETTINGS["Time Step"])

    


    if TESTCASE == "testcases/RL_circuit.json":
        legends = ["V1_a", "V2_a", "V1_b", "V2_b", "V1_c", "V2_c", "V3_a", "V4_a", 
                "V3_b", "V4_b", "V3_c", "V4_c", "IL_1a", "IL_1b", "IL_1c", "IL_2a",
                "IL_2b", "IL_2c", "Iv_a", "Iv_b", "Iv_c"]
        v_graph = get_by_name("V3_a", legends, vectors)
        plt.plot(time, v_graph)
        v_graph = get_by_name("V3_b", legends, vectors)
        plt.plot(time, v_graph)
        v_graph = get_by_name("V3_c", legends, vectors)
        plt.plot(time, v_graph)
        plt.legend(["V3_a", "V3_b", "V3_c"])
        plt.show()

        i_graph = get_by_name("IL_2a", legends, vectors)
        plt.plot(time, i_graph)
        i_graph = get_by_name("IL_2b", legends, vectors)
        plt.plot(time, i_graph)
        i_graph = get_by_name("IL_2c", legends, vectors)
        plt.plot(time, i_graph)
        plt.legend(["IL_2a", "IL_2b", "IL_2c"])
        plt.show()
    
    if TESTCASE == "testcases/Simple_IM.json":
        legends = ["Vds", "Vqs", "Ids", "Iqs", "Idr", "Iqr", "Wr"]
        induction_graph = get_by_name("Vds", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Vqs", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Ids", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Iqs", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Idr", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Iqr", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Wr", legends, vectors)
        plt.plot(time, induction_graph)
        plt.legend(legends)
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