from lib.Solve import solve
from lib.settings import Settings
from parsers.parser import parse_raw

# path to the grid network RAW file
casename = 'testcases/PEGASE-13659_flat_start.RAW'

raw_data = parse_raw(casename)

settings = Settings()

solve(raw_data, settings)