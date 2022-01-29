from classes.Settings import Settings
from scripts.solve import solve

# path to the grid network RAW file
casename = 'testcases/IM_circuit.json'

# the settings for the solver
settings = Settings(
	tolerance=1E-05, # Tolerance for Newton-Raphson
	maxNewtonIterations=5, # Maximum number of newton iterations for non-linear loop at given time step
    simulationTime=0.2, # Total time to simulate: [0, tf]
    useSparseMatrix=False # Use sparse matrix formulation
    )

# run the solver
solve(casename, settings)