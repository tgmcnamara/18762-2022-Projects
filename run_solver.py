from lib.Solve import solve
from lib.settings import Settings
from models.Branches import Branches
from models.Buses import Bus
from models.Generators import Generators
from models.Slack import Slack
from parsers.parser import parse_raw

# path to the grid network RAW file
casename = 'testcases/GS-4_prior_solution.RAW'

raw_data = parse_raw(casename)

settings = Settings(debug=True, max_iters=30)

results = solve(raw_data, settings)

for result in results:
    print(result)