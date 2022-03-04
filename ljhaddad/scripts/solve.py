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

	# # # Assign system nodes # # #
	size_Y = assign_node_indexes(devices)
	
	# # # Initialize solution vector # # #
	V_init = initialize(devices, size_Y)

	# # # Run the time domain simulation and return an array # # #
	start = time.time()
	V_waveform = run_time_domain_simulation(devices, V_init, size_Y, SETTINGS)
	print(time.time() - start)
	# # # Process Results # # #
	process_results(V_waveform, devices, t_final)
