from classes.Devices import Devices
from classes.Settings import Settings
from lib.assign_node_indexes import assign_node_indexes
from lib.initialize import initialize
from lib.process_results import process_results
from lib.run_time_domain_simulation import execute_simulation

def solve(devices: Devices, settings: Settings = Settings()):

    # # # Assign system nodes # # #
    # We assign a node index for every node in our Y matrix and J vector.
    # In addition to voltages, nodes track currents of voltage sources and
    # other state variablesneeded for companion models or the model of the 
    # induction motor.
    # You can determine the size of the Y matrix by looking at the total
    # number of nodes in the system.
    (node_size, total_size) = assign_node_indexes(devices)
    
    # # # Initialize solution vector # # #
    # TODO: STEP 1 - Complete the function to find your state vector at time t=0.
    v_init = initialize(devices, node_size, total_size)

    # TODO: STEP 2 - Run the time domain simulation and return an array that contains
    #                time domain waveforms of all the state variables # # #
    v_waveform = execute_simulation(devices, v_init, settings)

    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process results function to compute the relevant results (voltage and current
    # waveforms, steady state values, etc.), plot them, and compare your output to the waveforms produced by Simulink
    results = process_results(v_waveform, devices, settings)

    return results