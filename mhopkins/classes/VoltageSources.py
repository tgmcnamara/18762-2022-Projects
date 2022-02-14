import numpy as np
import math
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class VoltageSources:
    def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
        self.name = name
        self.vp_node = vp_node
        self.vn_node = vn_node
        self.amp_ph_ph_rms = amp_ph_ph_rms
        self.phase_deg = phase_deg
        self.frequency_hz = frequency_hz
        self.DC = False
        self.ecm_type = ""
        self.ecm_val = 0
        print("voltage frequency", frequency_hz)
        # You are welcome to / may be required to add additional class variables   

    def get_nom_voltage(self):
        return self.amp_ph_ph_rms
    
    def get_current_voltage(self, t):
        if (self.DC):
            return self.get_nom_voltage()
        else:
            f = self.frequency_hz
            return 1/math.sqrt(2) * self.amp_ph_ph_rms * math.cos(2 * math.pi * f * t + self.phase_deg)
    
    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_open(self,):
        pass
    
    def __str__(self):
        return "V-{}-{}".format(self.amp_ph_ph_rms, id(self))
    
    def __repr__(self):
        return self.__str__()
        
