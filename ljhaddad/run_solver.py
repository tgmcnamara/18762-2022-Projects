from scripts.solve import solve

# path to the grid network RAW file
casename = 'testcases/RL_circuit.json'

# the settings for the solver
settings = {
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 6, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 1.0, # Total time to simulate: [0, tf]
    "Sparse": False # Use sparse matrix formulation
}

# run the solver
solve(casename, settings)
