from lib.Solve import solve
from lib.settings import Settings
from parsers.parser import parse_raw

# path to the grid network RAW file
casename = 'testcases/GS-4_prior_solution.RAW'
#casename = 'testcases/IEEE-14_prior_solution.RAW'
#casename = 'testcases/IEEE-118_prior_solution.RAW'

raw_data = parse_raw(casename)

settings = Settings(debug=True, max_iters=30, limiting=False, use_sparse=True)

result = solve(raw_data, settings)

result = solve(raw_data, settings)

result.display()