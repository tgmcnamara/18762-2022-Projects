from classes.Settings import Settings
from lib.parse_json import parse_json
from lib.solve import solve

devices = parse_json('testcases/RL_circuit.json')
results = solve(devices, Settings(simulationTime=0.2, timestep=0.0001))

#examine results.