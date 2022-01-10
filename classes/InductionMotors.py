import sys
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class InductionMotors:
    def __init__(
        self,
        name,
        phase_a_node,
        phase_b_node,
        phase_c_node,
        power_nom,
        v_nom,
        motor_freq,
        lm,
        rs,
        rr,
        lls,
        llr,
        j_im,
        tm,
        d_fric,
        n_poles):
        self.name = name
        self.phase_a_node = phase_a_node
        self.phase_b_node = phase_b_node
        self.phase_c_node = phase_c_node
        self.power_nom = power_nom
        self.v_nom = v_nom
        self.motor_freq = motor_freq
        self.lm = lm
        self.rs = rs
        self.rr = rr
        self.lls = lls
        self.llr = llr
        self.lss = self.lls + self.lm
        self.lrr = self.llr + self.lm
        self.j_im = j_im
        self.tm = tm
        self.d_fric = d_fric
        self.n_poles = n_poles
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_nodes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_open(self,):
        pass