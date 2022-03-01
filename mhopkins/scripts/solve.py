from lib.parse_json import parse_json
from lib.assign_node_indexes import assign_node_indexes
from lib.initialize import initialize
from lib.stamp import *
from scripts.run_time_domain_simulation import run_time_domain_simulation
from scripts.process_results import process_results
import time
# my code
from lib.circuit import *

def solve(TESTCASE, SETTINGS):
    """Run the power flow solver.
    Args:
        TESTCASE (str): A string with the path to the network json file.
        SETTINGS (dict): Contains all the solver settings in a dictionary.
    Returns:
        None
    """
    # TODO: STEP 0 - Initialize all the model classes in the models directory (models/) and familiarize
    #  yourself with the parameters of each model.

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
    # these are uploaded into simulator object 
    t_final = SETTINGS['Simulation Time']
    tol = SETTINGS['Tolerance']  # NR solver tolerance
    max_iters = SETTINGS['Max Iters']  # maximum NR iterations
    

    # # # Assign system nodes # # #
    # stamping
    # We assign a node index for every node in our Y matrix and J vector.
    # In addition to voltages, nodes track currents of voltage sources and
    # other state variables needed for companion models or the model of the 
    # induction motor.
    # You can determine the size of the Y matrix by looking at the total
    # number of nodes in the system.
    node_indices, size_Y = assign_node_indexes(devices)
    print("node_indices", node_indices)
    print("circuit elements", resistors + capacitors + inductors + voltage_sources)
    
    t_start = time.time_ns()
    simulator = Simulator(SETTINGS, devices = devices, size_Y = size_Y, 
                           node_indices = node_indices)
    print("admittance matrix", simulator.Y)
    print("circuit", simulator.circuit)
    print("eq circuit", simulator.circuit_ecm)
    print("solving dict", simulator.solving_dict)
    simulator.iterate(sparse = False)
    print("solving dict", simulator.solving_dict)
    
    # # # Initialize solution vector # # #
    # TODO: STEP 1 - Complete the function to find your state vector at time t=0.
    V_init = initialize(devices, size_Y)

    # TODO: STEP 2 - Run the time domain simulation and return an array that contains
    #                time domain waveforms of all the state variables # # #
    V_waveform = run_time_domain_simulation(devices, V_init, size_Y, SETTINGS)
    
    t_end = time.time_ns()
    t_total = t_end - t_start
    print("total time solving the circuit:", t_total," nanoseconds")
    
    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process results function to compute the relevant results (voltage and current
    # waveforms, steady state values, etc.), plot them, and compare your output to the waveforms produced by Simulink
    process_results(simulator, SETTINGS)
    return t_total
