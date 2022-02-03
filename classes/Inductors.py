import sys
from classes.CurrentSources import CurrentSources

from classes.Resistors import Resistors
sys.path.append("..")
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l  
        # You are welcome to / may be required to add additional class variables   

    def assign_node_indexes(self, nodeLookup: dict):
        self.from_index = nodeLookup[self.from_node]
        self.to_index = nodeLookup[self.to_node]
        
    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        companion_r = timestep / (2 * self.l)
        resistor = Resistors(self.name + "-companion-resistor", self.from_node, self.to_node, companion_r)
        resistor.assign_node_indexes_direct(self.from_index, self.to_index)
        resistor.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

        previous_voltage = v_previous[self.to_index] - v_previous[self.from_index]
        #this is a hack that will be very broken the second another current supplying element is on this node.
        #todo: generate a new 'private' node for the inductor that gives it its own
        #J vector scratch space.
        previous_current = J_previous[self.from_index]
        companion_i = previous_current + timestep / (2 * self.l) * previous_voltage
        current_source = CurrentSources(self.name + "-companion-current-source", self.from_node, self.to_node, companion_i)
        current_source.assign_node_indexes_direct(self.from_index, self.to_index)
        current_source.stamp_dense(Y, J, v_previous, J_previous, runtime, timestep)

    def stamp_sparse(self,):
        pass

    def stamp_short(self,):
        pass