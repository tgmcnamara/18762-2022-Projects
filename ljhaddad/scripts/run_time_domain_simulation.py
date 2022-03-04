import numpy as np
import scipy as sp
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
	curr_t = 0
	V_past = V_init
	# Loop over time steps
	while curr_t < SETTINGS['Simulation Time']:
		# Construct admittance matrix
		Y = np.zeros((size_Y, size_Y))
		# Construct solution vector
		J = np.zeros((size_Y, 1))
		
		# Stamp resistors
		for r in devices['resistors']:
			r.stamp_dense(Y)

		# Stamp Voltage sources
		for vs in devices['voltage_sources']:
			vs.stamp_dense(Y, J, curr_t)

		# Stamp inductors
		for l in devices['inductors']:
			l.stamp_dense(Y, J)

		# Stamp induction motors
		for m in devices['induction_motors']:
			m.stamp_dense(Y, J, V_past)

		# Solve via Newton-Raphson
		tol = np.ones((size_Y, 1))*SETTINGS['Tolerance']
		err = np.ones((size_Y, 1))
		vk = np.copy(V_past)
		iters = 0
		while np.any(err > tol):
			if iters > SETTINGS['Max Iters']:
				break
			# Create copies of the "base" matrices without
			# N-R updates
			Y_nr = np.copy(Y)
			J_nr = np.copy(J)
			for m in devices['induction_motors']:
				m.stamp_update(Y_nr, J_nr, vk)
			vk_old = np.copy(vk)
			# attempt with sparse matrices
			if SETTINGS['Sparse']:
				vk = spsolve(Y, J, use_umfpack=True)
				err = np.absolute(vk - vk_old)
				iters += 1
				continue
			vk = np.linalg.solve(Y_nr, J_nr)
			err = np.absolute(vk - vk_old)
			iters += 1
		
		# New state vector acquired
		v = np.reshape(vk, (-1, 1))
		
		# Append to the waveforms
		if curr_t == 0:
			V_waveform = V_init
			V_past = V_init
		else:
			V_waveform = np.append(V_waveform, v, axis=1)
			# Update state
			V_past = v
			for l in devices['inductors']:
				l.set_current_state(V_past, J_nr)

		# Increment simulation time
		curr_t += 0.001

	return V_waveform
