import sys
sys.path.append("..")
import numpy as np
from itertools import count

class Nodes:
    def __init__(self, name, phase):
        self.name = name
        self.phase = phase
        self.index = -1
        # You are welcome to / may be required to add additional class variables

    # Some suggested functions to implement,
    def assign_node_indexes(self,num):
        if (self.name == "gnd"):
            return 0
        else:
            self.index = num
            return 1
