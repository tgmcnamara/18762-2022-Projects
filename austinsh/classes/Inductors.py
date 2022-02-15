import sys
sys.path.append("..")
import numpy as np
# from run_solver import settings
from itertools import count
from classes.Nodes import Nodes
from classes.Resistors import Resistors
# from lib.parse_json import parse_json
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l
        # The equivalent conductance for trapezoidal method
        # self.g_equiv = settings["Time Step"]/(2*self.l)
        # self.pre_current_comp = 1

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.from_node] 
        self.to_node_index = Nodes.node_index_dict[self.to_node]
        # Returns a tuple of 
        return self.from_node_index, self.to_node_index
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass
        for l in parse_json.devices["inductors"]:
            # Need to change the location of the matrix
            Resistors.stamp_dense(l, Resistors.Y_matrix)

        

    def stamp_short(self,):
        pass