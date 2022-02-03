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
        self.frequency_rad_per_sec = frequency_hz * HERTZ_TO_RADIANS_PER_SECOND
        self.phase_rad = phase_deg * math.pi / 180

    def assign_node_indexes(self, nodeLookup: dict):
        self.vp_index = nodeLookup[self.vp_node]
        self.vn_index = nodeLookup[self.vn_node]

        modified_index = len(nodeLookup)
        nodeLookup[self.name] = modified_index
        self.current_index = modified_index
        
    def stamp_dense(self, Y, J, v_previous, J_previous, runtime, timestep):
        Y[self.current_index, self.vp_index] = 1
        Y[self.vp_index, self.current_index] = 1

        Y[self.current_index, self.vn_index] = -1
        Y[self.vn_index, self.current_index] = -1

        J[self.current_index] = self.v_max * math.cos(self.frequency_rad_per_sec * runtime + self.phase_rad)

    def stamp_sparse(self,):
        pass

    def stamp_open(self,):
        pass
        
class CurrentSensors(VoltageSources):
    def __init__(self, node_1, node_2, index):
        VoltageSources.__init__(self, "currentsensor-" + str(index), node_1, node_2, 0, 0, 0)