
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse


class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_nodes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_open(self,):
        pass