from scripts.solve import solve

# path to the grid network RAW file
casename = 'testcases/IM_circuit.json'#Change Plotting setting as well

# the settings for the solver
settings = {
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 5, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 0.5, # Total time to simulate: [0, tf]
    "Sparse": False, # Use sparse matrix formulation
    "Plots": "IM" #Use "IM" for IM plots use "RL" for RL plots
}

# run the solver
solve(casename, settings)
