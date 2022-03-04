import numpy as np

def initialize(devices, size_Y):
	# Create variable to track size of dummy admittance matrix
	size_Yd = size_Y

	# Next, loop through inductors and expand Yd to add voltage sources
	for l in devices['inductors']:
		l.set_current_index(size_Yd)
		size_Yd += 1
	
	# Create a temporary admittance matrix and solution vector
	Y = np.zeros((size_Yd, size_Yd))
	J = np.zeros((size_Yd, 1))

	# Stamp the matrices
	for r in devices['resistors']:
		r.stamp_dense(Y)

	for vs in devices['voltage_sources']:
		vs.stamp_dense(Y, J, 0)

	for l in devices['inductors']:
		l.stamp_short(Y, J)

	for m in devices['induction_motors']:
		m.stamp_t0(Y, J)

	# Get dummy initial solution vector
	v = np.linalg.solve(Y, J)

	# Extract the inductor currents and store them with 
	# the inductor objects
	for l in devices['inductors']:
		l.set_initial_state(v)

	# For energy storage, this portion will:
		# Create an admittance matrix with open/shorts
		# Solve for the state vector given time-invariant
		# voltage source
		# Return the V_init vector shaped for circuit with
		# companion models
	V_init = np.copy(v[:size_Y, :])
	return V_init
