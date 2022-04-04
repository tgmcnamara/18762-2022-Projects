import math
import time
from lib.settings import Settings
from parsers.parser import parse_raw
from lib.PowerFlow import PowerFlow
from lib.process_results import process_results
from lib.initialize import initialize
from itertools import count

def solve(raw_data, settings: Settings):
    print("Running power flow solver...")

    start_time = time.perf_counter_ns()

    buses = raw_data['buses']
    slack = raw_data['slack']
    transformers = raw_data['xfmrs']
    generators = raw_data['generators']

    node_index = count(0)

    # # # Assign System Nodes Bus by Bus # # #
    # We can use these nodes to have predetermined node number for every node in our Y matrix and J vector.
    for ele in buses + slack + transformers:
        ele.assign_nodes(node_index)

    # # # Initialize Solution Vector - V and Q values # # #
    # determine the size of the Y matrix by looking at the total number of nodes in the system
    size_Y = node_index.__next__()

    v_init = initialize(size_Y, buses, generators, slack, settings)

    # # # Run Power Flow # # #
    powerflow = PowerFlow(settings, raw_data, size_Y)

    (v_final, iteration_num) = powerflow.run_powerflow(v_init)

    print(f'Power flow solver converged after {iteration_num} iterations.')

    end_time = time.perf_counter_ns()

    duration_seconds = (end_time * 1.0 - start_time * 1.0) / math.pow(10, 9)

    print(f'Ran for {"{:.3f}".format(duration_seconds)} seconds')

    results = process_results(raw_data, v_final, duration_seconds)

    return results
