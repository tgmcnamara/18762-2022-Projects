from lib.parse_json import parse_json
from lib.assign_node_indexes import assign_node_indexes
from lib.initialize import initialize
from scripts.run_time_domain_simulation import run_time_domain_simulation
from scripts.process_results import process_results
import time

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
    t_final = SETTINGS['Simulation Time']
    tol = SETTINGS['Tolerance']  # NR solver tolerance
    max_iters = SETTINGS['Max Iters']  # maximum NR iterations
    step = 0.001
    # # # Assign system nodes # # #
    # We assign a node index for every node in our Y matrix and J vector.
    # In addition to voltages, nodes track currents of voltage sources and
    # other state variablesneeded for companion models or the model of the
    # induction motor.
    # You can determine the size of the Y matrix by looking at the total
    # number of nodes in the system.

    begin = time.perf_counter()
    size_Y = assign_node_indexes(devices)

    # # # Initialize solution vector # # #
    # TODO: STEP 1 - Complete the function to find your state vector at time t=0.
    V_init = initialize(devices, size_Y)

    # TODO: STEP 2 - Run the time domain simulation and return an array that contains
    #                time domain waveforms of all the state variables # # #
    V_waveform = run_time_domain_simulation(devices, V_init, size_Y, SETTINGS, step)

    end = time.perf_counter()
    tot = end - begin
    print("Performance Time: ")
    print(tot)
    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process results function to compute the relevant results (voltage and current
    # waveforms, steady state values, etc.), plot them, and compare your output to the waveforms produced by Simulink
    process_results(V_waveform, devices, SETTINGS, step)
