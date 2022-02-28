from classes.Devices import Devices
from classes.Settings import Settings
from lib.assign_node_indexes import assign_node_indexes
from lib.initialize import initialize
from lib.matrixprovider import MatrixProvider
from lib.process_results import process_results
from lib.simulator import Simulator
import time
import math

def solve(devices: Devices, settings: Settings = Settings()):

    print("Running solver...")

    start_time = time.perf_counter_ns()

    Y_size = assign_node_indexes(devices)
    
    v_init = initialize(devices, Y_size)

    matrixprovider = MatrixProvider(settings.useSparseMatrix, Y_size)

    simulator = Simulator(devices, settings, Y_size, matrixprovider)

    (v_waveform, J_waveform) = simulator.execute_simulation(v_init)

    end_time = time.perf_counter_ns()

    total_time_seconds = (end_time * 1.0 - start_time * 1.0) / math.pow(10, 9)

    print(f'Solver execution complete. Ran for {total_time_seconds} seconds.')

    results = process_results(v_waveform, J_waveform, devices, settings)

    return results