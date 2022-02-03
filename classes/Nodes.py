import sys
sys.path.append("..")
import numpy as np
from itertools import count

class Nodes:    
    def __init__(self, name, phase = "A"):
        self.name = name
        self.phase = phase
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_index(self, index):
        self.index = index
