from scripts.solve import solve

# path to the grid network RAW file
#casename = 'testcases/RL_circuit.json'
#casename = 'testcases/voltage_divider.json'
#casename = 'testcases/single_phase_RL_circuit.json'
#casename = 'testcases/IM_circuit.json'
casename = 'testcases/RL_circuit.json'
#casename = 'testcases/IM_circuit_debug.json'

# the settings for the solver
settings = {
	"noi":[6,7,8], # nodes of interest for RL circuit
	#"noi":[9,10,11], # nodes of interest for RLC circuit
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 5, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 0.2,# 0.2, # Total time to simulate: [0, tf]
    "Sparse": False # Use sparse matrix formulation
}

# run the solver
solve(casename, settings)