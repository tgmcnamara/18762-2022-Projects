from lib.Solve import solve
from lib.settings import Settings
from parsers.parser import parse_raw

# path to the grid network RAW file
casename = 'testcases/IEEE-14_prior_solution.RAW'

raw_data = parse_raw(casename)

settings = Settings(debug=True, max_iters=30)

result = solve(raw_data, settings)

print("Results:")

for result in result.bus_results:
    print(result)