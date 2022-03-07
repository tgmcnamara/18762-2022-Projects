# A set of settings to be the set constraints for each testcase. Can be
# adjusted for different results.
settings = {
	"Tolerance": 1E-05, # Tolerance for Newton-Raphson
	"Max Iters": 5, # Maximum number of newton iterations for non-linear loop at given time step
    "Simulation Time": 2.3, # Total time to simulate: [0, tf]
    "Time Step": .00001, # Time step to use
    "Sparse": False # Use sparse matrix formulation
}