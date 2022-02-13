import numpy as np
from itertools import count
from classes.Nodes import Nodes
from lib.stamp import stamp_short

class Switches:
    def __init__(self, name, from_node, to_node, t_open, t_close):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.t_open = t_open
        self.t_close = t_close
        # You are welcome to / may be required to add additional class variables   

    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

        modified_index = len(nodeLookup)
        nodeLookup[self.name] = modified_index
        self.switch_index = modified_index
        
    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        if runtime >= self.t_open and runtime <= self.t_close:
            stamp_short(Y, J, self.from_index, self.to_index, self.switch_index)
        else:
            # if its an open circuit, then there's no relationship between the nodes.
            # instead, we make a 'dumby' function a 1 * vn = 1. Same as how we configure
            # the ground row.

            J[self.switch_index] = 1
            Y[self.switch_index, self.switch_index] = 1

    def stamp_sparse(self,):
        pass

    def stamp_open(self,):
        pass