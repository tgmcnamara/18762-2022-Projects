import sys
from classes.CurrentSources import CurrentSources

from classes.Resistors import Resistors
sys.path.append("..")
import numpy as np

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l  

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
        conductance = timestep / (2 * self.l)

        companion_r = 1 / conductance

        resistor = Resistors(self.name + "-companion-resistor", self.from_node, self.to_node, companion_r)
        resistor.assign_node_indexes_direct(self.from_index, self.extension_index_1)
        resistor.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

        previous_voltage = v_previous[self.from_index] - v_previous[self.extension_index_1]

        previous_current = J_previous[self.extension_index_1]

        companion_i = previous_current + conductance * previous_voltage
        
        current_source = CurrentSources(self.name + "-companion-current-source", self.from_node, self.to_node, companion_i)
        current_source.assign_node_indexes_direct(self.from_index, self.extension_index_1)
        current_source.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

        # We place the short on its own row so that it doesn't interfere with other components attached to the other
        # side of the node.
        Y[self.extension_index_2, self.extension_index_1] = 1
        Y[self.extension_index_2, self.to_index] = -1

        Y[self.extension_index_1, self.extension_index_2] = 1
        Y[self.to_index, self.extension_index_2] = -1

        J[self.extension_index_2] = 0

    def stamp_sparse(self,):
        pass

    def stamp_short(self,):
        pass