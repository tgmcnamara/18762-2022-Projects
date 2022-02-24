import sys
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

def F(x,x_prev):
    phiqs = (self.lls + self.lm) * x_prev[1] + self.lm * x_prev[3]
    phids = (self.lls + self.lm) * x_prev[0] + self.lm * x_prev[2]
    # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
    fx1 = ( -x[5] + self.rs * x[0] + (2/self.delta_t) * ((self.lls+self.lm)*x[0] + self.lm*x[2]) -
            x_prev[5] + self.rs*x_prev[0] - (2/self.delta_t) * phids)
    fx2 = 0
    fx3 = 0
    fx4 = 0
    fx5 = 0
    fx6 = 0
    fx7 = 0
    return np.array([fx1,fx2,fx3,fx4,fx5])

def J(x):
    # eqs 0 
    # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
    j1 = 0
    j2 = 0
    j3 = 0
    j4 = 0
    j5 = 0
    j6 = 0
    j7 = 0
    return np.vstack((j1,j2,j3,j4,j5,j6,j7))


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
        j,
        tm,
        d_fric,
        n_pole_pairs):
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
        self.j = j
        self.tm = tm
        self.d_fric = d_fric
        self.n_pole_pairs = n_pole_pairs
        self.lss = self.lls + self.lm
        self.lrr = self.llr + self.lm
        # You are welcome to / may be required to add additional class variables
        
        # SIMULATION VARIABLES
        # states of the induction motor
        self.my_circuit = None
        self.x = np.array([1,2])
        self.input_nodes = {} # dictionary mapping voltage inputs to nodes in the circuit
        self.output_hist = np.zeros((6,1))
        self.delta_t = 0.1   
        
    def set_state(self, x):
        self.x = x

    def NR_iterate(self, delta_t):
        self.delta_t = delta_t
        pass
    
    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_t0(self,):
        pass