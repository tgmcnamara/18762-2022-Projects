from scripts.solve import solve

# path to the grid network RAW file
casename = 'testcases/RL_circuit.json'

# the settings for the solver
settings = {
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 5, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 0.2, # Total time to simulate: [0, tf]
    "Time Step": .001, # Time step to use
    "Sparse": False # Use sparse matrix formulation
}

# run the solver
solve(casename, settings)