import sys
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

def F(x,x_prev, voltages):
    phiqs = (self.lls + self.lm) * x_prev[1] + self.lm * x_prev[3]
    phids = (self.lls + self.lm) * x_prev[0] + self.lm * x_prev[2]
    phidr = (self.llr + self.lm) * x_prev[2] + self.lm * x_prev[0]
    phiqr = (self.llr + self.lm) * x_prev[3] + self.lm * x_prev[1]
    Te_ = (3/2) * self.n_pole_pairs * self.lm * (x_prev[2]*x_prev[1] - x_prev[3]*x_prev[0])
    #lambda_ = 0
    lambda_ = 2*math.pi*self.motor_freq
    
    # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
    # x_prev: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
    # voltages: [0]v_a,[1]v_b,[2]v_c
    #fx1:ds,fx2:qs,fx3:dr,fx4:qr,fx5:wr,fx6:vds,fx7:vqs
    fx1 = ( -x[5] + self.rs * x[0] + (2/self.delta_t) * ((self.lls+self.lm)*x[0] + self.lm*x[2]) -
            x_prev[5] + self.rs*x_prev[0] - (2/self.delta_t) * phids)
    
    fx2 = ( -x[6] + self.rs * x[1] + (2/self.delta_t) * ((self.lls+self.lm)*x[0] + self.lm*x[2]) -
            -x_prev[6] + self.rs * x_prev[1] - (2/self.delta_t) * phiqs)
    
    fx3 = ( self.rr * x[2] + ((self.llr + self.lm)*x[3] + self.lm*x[1])*x[4] + 
            (2/self.delta_t) * ((self.llr + self.lm)*x[2] + self.lm*x[0]) + self.rr*x_prev[2] + phiqr*x_prev[4] -
            (2/self.delta_t) * phidr)
    
    fx4 = ( self.rr * x[3] + ((self.llr + self.lm)*x[2] + self.lm*x[0])*x[4] +
            (2/self.delta_t) * ((self.llr + self.lm)*x[3] + self.lm*x[1]) + self.rr*x_prev[3] + phidr*x_prev[4] -
            (2/self.delta_t) * phiqr)
    
    fx5 = ( (3/2) * self.n_pole_pairs * self.lm * (x[2]*x[1] - x[3]*x[0]) - (self.d_fric + 2*self.j/self.delta_t)*x[4] +
            Te_ + (2*self.J/self.delta_t - self.d_fric)*x_prev[4] - 2*self.tm)
    
    fx6 = (2/3) * (math.cos(0)*voltages[0] + math.cos(-lambda_)*voltages[1] + math.cos(lambda_)*voltages[2])
    fx7 = (2/3) * (math.sin(0)*voltages[0] + math.sin(-lambda_)*voltages[1] + math.sin(lambda_)*voltages[2])
    
    return np.array([fx1,fx2,fx3,fx4,fx5,fx6,fx7])

def init_J():
    j1 = [1,0,0,0,0,0,0]
    j2 = [0,1,0,0,0,0,0]
    j3 = [0,0,1,0,0,0,0]
    j4 = [0,0,0,1,0,0,0]
    j5 = [0,0,0,0,1,0,0]
    j6 = [0,0,0,0,0,1,0]
    j7 = [0,0,0,0,0,0,1]
    return np.vstack((j1,j2,j3,j4,j5,j6,j7))

def J(x):
    # eqs 0 
    # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
    j1 = [self.rs + (2/self.delta_t) * (self.lls + self.lm), 0, (2/self.delta_t)*self.lm, 0, 0, -1, 0]
    
    j2 = [0, self.rs + (2/self.delta_t) * (self.lls + self.lm), 0, (2/self.delta_t)*self.lm, 0, 0, -1]
    
    j3 = [(2/self.delta_t)*self.lm, self.lm*x[4], self.rr - (2/self.delta_t)*(self.llr + self.lm), (self.llr+self.lm)*x[4],
           ((self.llr+self.lm)*x[3]+self.lm*x[1])]
    
    j4 = [-self.lm*x[4], (2/self.delta_t)*self.lm, -(self.llr+self.lm)*x[4], self.rr+(2/self.delta_t)*(self.llr+self.lm),
          ((self.llr+self.lm)*x[2]+self.lm*x[0])]
    
    j5 = [(-3/2)*self.n_pole_pairs*self.lm*x[3], (3/2)*self.n_pole_pairs*self.lm*x[2], (3/2)*self.n_pole_pairs*self.lm*x[1],
          (-3/2)*self.n_pole_pairs*self.lm*x[0], -(self.d_fric + (2*self.j)/self.delta_t)]
    
    j6 = [0, 0, 0, 0, 0, 1, 0]
    
    j7 = [0, 0, 0, 0, 0, 0, 1]
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