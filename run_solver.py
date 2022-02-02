from classes.Settings import Settings
from scripts.solve import solve_from_file

# path to the grid network RAW file
casefile = 'testcases/IM_circuit.json'

# the settings for the solver
settings = Settings()

# run the solver
solve_from_file(casefile, settings)