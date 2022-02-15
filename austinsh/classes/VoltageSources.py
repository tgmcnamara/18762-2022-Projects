import numpy as np
from itertools import count
import classes.Nodes as Nodes
# from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class VoltageSources:
    def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
        self.name = name
        self.vp_node = vp_node
        self.vn_node = vn_node
        self.amp_ph_ph_rms = amp_ph_ph_rms
        self.phase_deg = phase_deg
        self.frequency_hz = frequency_hz
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        self.from_node_index = Nodes.node_index_dict[self.vp_node] 
        self.to_node_index = Nodes.node_index_dict[self.vn_node]
        return self.from_node_index, self.to_node_index
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_open(self,):
        pass
        
# voltage_3 = VoltageSources("N", "1a", "3a", 1, 0, 0)

# print(VoltageSources.assign_node_indexes(voltage_3))