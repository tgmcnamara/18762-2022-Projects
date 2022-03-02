from classes.Settings import Settings
from lib.parse_json import parse_json
from lib.solve import solve

devices = parse_json('testcases/RL_circuit_debug.json')
results = solve(devices, Settings(simulationTime=1, timestep=0.0001))

#examine results.