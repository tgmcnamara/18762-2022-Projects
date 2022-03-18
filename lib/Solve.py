from lib.settings import Settings
from parsers.parser import parse_raw
from lib.PowerFlow import PowerFlow
from lib.process_results import process_results
from lib.initialize import initialize
from models.Buses import _node_index


def solve(raw_data, settings: Settings):
    # TODO: PART 1, STEP 0 - Initialize all the model classes in the models directory (models/) and familiarize
    #  yourself with the parameters of each model. Use the docs/DataFormats.pdf for assistance.

    # # # Parse the Test Case Data # # #
    # # # Assign Parsed Data to Variables # # #

    buses = raw_data['buses']
    slack = raw_data['slack']

    # # # Assign System Nodes Bus by Bus # # #
    # We can use these nodes to have predetermined node number for every node in our Y matrix and J vector.
    for ele in buses:
        ele.assign_nodes()

    # Assign any slack nodes
    for ele in slack:
        ele.assign_nodes()

    # # # Initialize Solution Vector - V and Q values # # #

    # determine the size of the Y matrix by looking at the total number of nodes in the system
    size_Y = _node_index.__next__()

    v_init = initialize(size_Y, buses, settings)

    # # # Run Power Flow # # #
    powerflow = PowerFlow(settings, raw_data)

    # TODO: PART 1, STEP 2 - Complete the PowerFlow class and build your run_powerflow function to solve Equivalent
    #  Circuit Formulation powerflow. The function will return a final solution vector v. Remove run_pf and the if
    #  condition once you've finished building your solver.
    v_final = powerflow.run_powerflow(v_init)

    # # # Process Results # # #
    # TODO: PART 1, STEP 3 - Write a process_results function to compute the relevant results (voltages, powers,
    #  and anything else of interest) and find the voltage profile (maximum and minimum voltages in the case).
    #  You can decide which arguments to pass to this function yourself.
    process_results(v_final)
