from lib.settings import Settings
from parsers.parser import parse_raw
from lib.PowerFlow import PowerFlow
from lib.process_results import process_results
from lib.initialize import initialize
from models.Buses import _node_index


def solve(raw_data, settings: Settings):
    buses = raw_data['buses']
    slack = raw_data['slack']
    transformers = raw_data['xfmrs']
    generators = raw_data['generators']

    # # # Assign System Nodes Bus by Bus # # #
    # We can use these nodes to have predetermined node number for every node in our Y matrix and J vector.
    for ele in buses + slack + transformers:
        ele.assign_nodes()

    # # # Initialize Solution Vector - V and Q values # # #
    # determine the size of the Y matrix by looking at the total number of nodes in the system
    size_Y = _node_index.__next__()

    v_init = initialize(size_Y, buses, generators, settings)

    # # # Run Power Flow # # #
    powerflow = PowerFlow(settings, raw_data)

    v_final = powerflow.run_powerflow(v_init)

    results = process_results(buses, v_final)

    return results
