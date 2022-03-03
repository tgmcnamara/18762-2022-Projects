
import numpy as np
from itertools import count
from classes.Nodes import Nodes
from lib.stamp import stamp_resistor


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

    def get_nodes_connections(self):
        return [self.from_node, self.to_node]

    def assign_node_indexes_direct(self, from_index, to_index):
        self.from_index = from_index
        self.to_index = to_index

    def calculate_current(self, v, J, timestep):
        voltage = v[self.from_index] - v[self.to_index]

        return voltage / self.r

    def stamp_dense(self, Y, J, v_previous, runtime, timestep):
        stamp_resistor(Y, self.from_index, self.to_index, self.r)





        

        