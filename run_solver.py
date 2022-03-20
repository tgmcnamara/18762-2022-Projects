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

# raw_data = {}
# raw_data['buses'] = [
#     Bus(1, None, 1, 0, None),
#     Bus(2, None, 1, 0, None),
#     Bus(3, None, 1, 0, None)
# ]

# raw_data['branches'] = [
#     Branches(1, 2, 0.01008,	0.0504,	0.1025, True, None, None, None),
#     Branches(2, 3, 0.01008,	0.0504,	0.1025, True, None, None, None)
# ]

# raw_data['slack'] = [
#     Slack(2, 1, 0, 0, 0)
# ]

# raw_data['generators'] = [
#     Generators(1, 100, 1, None, None, None, None, None, None, None, None)
# ]

#raw_data['loads']

settings = Settings(debug=True, max_iters=30)

solve(raw_data, settings)