import matplotlib.pyplot as plt
import numpy as np
from scripts.solve import solve

# path to the grid network RAW file
#casename = 'testcases/RL_circuit.json'
#casename = 'testcases/voltage_divider.json'
#casename = 'testcases/single_phase_RL_circuit.json'
#casename = 'testcases/single_phase_RC_circuit.json'
#casename = 'testcases/IM_circuit.json'
#casename = 'testcases/RL_circuit.json'
#casename = 'testcases/IM_circuit_debug.json'
casename = 'testcases/IM_circuit.json'
#casename = 'testcases/IM_circuit.json'

case_study = False
trials = 50

# the settings for the solver
settings = {
	"noi":[6,7,8], # used to plot nodes of interest
	"Plotting":True, # only make this False if performing a case study
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 5, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 0.7,# 0.2, # Total time to simulate: [0, tf]
    "Sparse": True # Use sparse matrix formulation
}

# run the solver
solve(casename, settings)

# perform a case study to measure the computational efficiency
if (case_study):
	# computational efficiency test study
	sparse_times_vector = []
	dense_times_vector = []
	for i in range(trials):
		settings["Sparse"] = True
		result = solve(casename, settings)
		sparse_times_vector.append(result)
	for i in range(trials):
		settings["Sparse"] = False
		result = solve(casename, settings)
		dense_times_vector.append(result)
	sparse_avg = np.sum(np.array(sparse_times_vector)/trials)
	dense_avg = np.sum(np.array(dense_times_vector)/trials)
	
	plt.plot(range(trials), sparse_times_vector, label="sparse")
	plt.plot(range(trials), dense_times_vector, label="dense")
	plt.plot(range(trials), trials * [sparse_avg], label="sparse avg.")
	plt.plot(range(trials), trials * [dense_avg], label="dense avg.")
	plt.ylabel("Time(nanoseconds)")
	plt.xlabel("Trial")	
	plt.legend()
	plt.title("Induction Motor circuit Comp. Efficiency Study")
	plt.show()
	