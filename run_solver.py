from classes.Settings import Settings
from lib.parse_json import parse_json
from lib.solve import solve

# path to the grid network RAW file
casefile = 'testcases/RL_circuit.json'

# the settings for the solver
settings = Settings()

devices = parse_json(casefile)

results = solve(devices, settings)