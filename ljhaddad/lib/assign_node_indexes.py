from classes.Nodes import Nodes
def assign_node_indexes(devices):
	# node_index_counter to be replaced by Nodes internal counter
	#node_index_counter = 0
    
	# loop through the provided nodes
	for n in devices['nodes']:
		n.assign_node_indexes()

	# loop through the resistor objects
	for r in devices['resistors']:
		r.assign_node_indexes()

	# loop through voltage sources
	for v in devices['voltage_sources']:
		v.assign_node_indexes()

	# loop through inductors
	for l in devices['inductors']:
		l.assign_node_indexes()

	# loop through induction motors
	for m in devices['induction_motors']:
		m.assign_node_indexes()

	return Nodes.index_counter
