
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
  
    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

    def assign_node_indexes_direct(self, from_index, to_index):
        self.from_index = from_index
        self.to_index = to_index

    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        Y[self.from_index, self.from_index] += 1/self.r
        Y[self.to_index, self.to_index] += 1/self.r

        Y[self.from_index, self.to_index] += -1/self.r
        Y[self.to_index, self.from_index] += -1/self.r





        

        