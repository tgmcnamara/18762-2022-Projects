import numpy as np
from itertools import count
from classes.Nodes import Nodes
import math
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

HERTZ_TO_RADIANS_PER_SECOND = 6.283

class VoltageSources:
    def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
        self.name = name
        self.vp_node = vp_node
        self.vn_node = vn_node
        self.amp_ph_ph_rms = amp_ph_ph_rms
        self.phase_deg = phase_deg
        self.frequency_hz = frequency_hz
        
        self.v_max = amp_ph_ph_rms * math.sqrt(2)

    def assign_node_indexes(self, nodeLookup: dict):
        self.vp_index = nodeLookup[self.vp_node]
        self.vn_index = nodeLookup[self.vn_node]

        modified_index = len(nodeLookup) + 1
        nodeLookup[self.name] = modified_index
        self.voltage_index = modified_index
        
    def stamp_dense(self, Y, J, v_previous, timestep):
        Y[self.voltage_index, self.vp_index] = 1
        Y[self.vp_index, self.voltage_index] = 1

        Y[self.voltage_index, self.vn_index] = -1
        Y[self.vn_index, self.voltage_index] = -1

        J[self.voltage_index] = math.cos(self.frequency_hz * HERTZ_TO_RADIANS_PER_SECOND * timestep)

    def stamp_sparse(self,):
        pass

    def stamp_open(self,):
        pass
        
