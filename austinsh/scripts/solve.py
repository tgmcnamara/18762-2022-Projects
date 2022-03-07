import sys
sys.path.append("..")
import numpy as np
from lib.parse_json import parse_json
from classes import Nodes
import matplotlib.pyplot as plt
import time as duration

def solve(TESTCASE, SETTINGS):
    start_time = duration.time()
    """Run the power flow solver.
    Args:
        TESTCASE (str): A string with the path to the network json file.
        SETTINGS (dict): Contains all the solver settings in a dictionary.
    Returns:
        None
    """

    # # # Parse the test case data # # #
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
            # Add the solution values from the simple IM model to the vectors list
            # to later be graphed
            vectors.append(reference)
        # Incriment the time
        t += SETTINGS["Time Step"]
        return vectors, t
    
    while t <= t_final:
        # Initialize a solution list
        if t == 0:
            # vectors is the solutions to later be graphed and volt is a temporary
            # list for the induction motor
            vectors = []
            volt = []
        # Initialize the matrices Y and J to be stamped at the current timestep
        Y_matrix = np.zeros((size_Y, size_Y))
        J_matrix = np.zeros(size_Y)
        # Produce the list of solution vectors
        vectors, t = solver(Y_matrix, J_matrix, vectors, t, tol, max_iters, time_step, volt)
    
    # Convert the list of arrays into one array
    vectors = np.array(vectors)
    
    # Get the values to be graphed based on the name of the value
    def get_by_name(name, legends, vectors):
        index = legends.index(name)
        vector_adj = vectors[:,index]
        vector_adj = vector_adj.flat
        return np.array(vector_adj)

    end = duration.time()
    print("\nThe simulation took", (end - start_time) ,"seconds to finish.")
    input("\npress ENTER")

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
        plt.xlabel("Time (s)")
        plt.ylabel("Current (V)")
        plt.title("Voltage of RL Circuit Nodes 3", fontdict = {"family":"serif", "size":20})
        plt.show()

        i_graph = get_by_name("IL_2a", legends, vectors)
        plt.plot(time, i_graph)
        i_graph = get_by_name("IL_2b", legends, vectors)
        plt.plot(time, i_graph)
        i_graph = get_by_name("IL_2c", legends, vectors)
        plt.plot(time, i_graph)
        plt.legend(["IL_2a", "IL_2b", "IL_2c"])
        plt.xlabel("Time (s)")
        plt.ylabel("Current (A)")
        plt.title("Current Through the RL Circuit", {"family":"serif", "size":20})
        plt.show()
    
    if TESTCASE == "testcases/Simple_IM.json":
        legends = ["Vds", "Vqs", "Ids", "Iqs", "Idr", "Iqr", "Wr", "Te"]
        induction_graph = get_by_name("Ids", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Iqs", legends, vectors)
        plt.plot(time, induction_graph)
        plt.xlabel("Time (s)")
        plt.ylabel("Stator Current (A)")
        plt.title("Stator Current of the Induction Motor", {"family":"serif", "size":20})
        plt.legend(["Ids", "Iqs"])
        plt.show()

        induction_graph = get_by_name("Idr", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Iqr", legends, vectors)
        plt.plot(time, induction_graph)
        plt.xlabel("Time (s)")
        plt.ylabel("Rotor Current (A)")
        plt.title("Rotor Current of the Induction Motor", {"family":"serif", "size":20})
        plt.legend(["Idr", "Iqr"])
        plt.show()

        induction_graph = get_by_name("Wr", legends, vectors)
        plt.plot(time, induction_graph)
        induction_graph = get_by_name("Te", legends, vectors)
        plt.plot(time, induction_graph)
        plt.xlabel("Time (s)")
        plt.ylabel("Rotor Angular Frequency (rads/sec) and Electrical Torque")
        plt.title("Angular Rotor Frequency and Electrical Torque of the Induction Motor", {"family":"serif", "size":16})
        plt.legend(["Wr", "Te"])
        plt.show()