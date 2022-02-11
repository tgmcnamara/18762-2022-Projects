import numpy as np
from itertools import count
from classes.Nodes import Nodes
from classes.Resistors import Resistors
#from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Capacitors:
    def __init__(self, name, from_node, to_node, c):
        self.name = name
        self.c = c
        self.from_node = from_node
        self.to_node = to_node
        # You are welcome to / may be required to add additional class variables   

    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]

        modified_index = len(nodeLookup)
        nodeLookup[self.name + "-1"] = modified_index
        self.extension_index_1 = modified_index
        modified_index += 1
        nodeLookup[self.name + "-2"] = modified_index
        self.extension_index_2 = modified_index

    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        
        companion_r = timestep / (2 * self.c)

        resistor = Resistors(self.name + "-companion-resistor", self.from_node, self.to_node, companion_r)
        resistor.assign_node_indexes_direct(self.from_index, self.extension_index_1)
        resistor.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

    def stamp_sparse(self,):
        pass

    def stamp_open(self,):
        pass