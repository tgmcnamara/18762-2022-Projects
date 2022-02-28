import sys
sys.path.append("..")
import numpy as np
import math
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
        self.tol = 0.00001
        self.max_iters = 4
        # You are welcome to / may be required to add additional class variables
        
        # SIMULATION VARIABLES
        # states of the induction motor
        self.my_circuit = None
        self.x = np.array([0,0,0,0,0])
        self.x_hist = np.array([0,0,0,0,0,0,0])
        self.input_nodes = {} # dictionary mapping voltage inputs to nodes in the circuit
        self.output_hist = np.zeros((6,1))
        self.delta_t = 0.1  
        self.voltage_inputs = [0,0,0] 
        self.timesteps = 0
        self.prev_vds = 0
        self.prev_vqs = 0
        
    def set_state(self, x):
        self.x = x

    def calc_Te(self):
        ids_hist = self.x_hist[:,0]
        iqs_hist = self.x_hist[:,1]
        #
        idr_hist = self.x_hist[:,2]
        iqr_hist = self.x_hist[:,3]
        
        Te = (3/2) * self.n_pole_pairs * self.lm * (idr_hist*iqs_hist - iqr_hist*ids_hist)
        return Te

    def NR_iterate(self, delta_t):
        self.delta_t = delta_t
        result = self.newtonRaphson(self.x,self.tol,self.max_iters)
        self.x = result
        # add vds and vqs
        result = np.hstack((result,np.array([self.prev_vds, self.prev_vqs])))
        #self.x = result
        self.x_hist = np.vstack((self.x_hist, result))
        self.timesteps = self.timesteps + 1
        return result
    
    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_t0(self,):
        pass
    
    def F(self,x,x_prev, voltages):
        phiqs = (self.lls + self.lm) * x_prev[1] + self.lm * x_prev[3]
        phids = (self.lls + self.lm) * x_prev[0] + self.lm * x_prev[2]
        phidr = (self.llr + self.lm) * x_prev[2] + self.lm * x_prev[0]
        phiqr = (self.llr + self.lm) * x_prev[3] + self.lm * x_prev[1]
        Te_ = (3/2) * self.n_pole_pairs * self.lm * (x_prev[2]*x_prev[1] - x_prev[3]*x_prev[0])
        #lambda_ = 0
        lambda_ = (2/3) * math.pi#2*math.pi*self.motor_freq
        vds = (2/3) * (math.cos(0)*voltages[0] + math.cos(-lambda_)*voltages[1] + math.cos(lambda_)*voltages[2])
        vqs = (2/3) * (math.sin(0)*voltages[0] + math.sin(-lambda_)*voltages[1] + math.sin(lambda_)*voltages[2])
        # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
        # x_prev: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
        # voltages: [0]v_a,[1]v_b,[2]v_c
        #fx1:ds,fx2:qs,fx3:dr,fx4:qr,fx5:wr,fx6:vds,fx7:vqs
        fx1 = ( -vds + self.rs * x[0] + (2/self.delta_t) * ((self.lls+self.lm)*x[0] + self.lm*x[2]) -
                self.prev_vds + self.rs*x_prev[0] - (2/self.delta_t) * phids)
        
        fx2 = ( -vqs + self.rs * x[1] + (2/self.delta_t) * ((self.lls+self.lm)*x[1] + self.lm*x[3]) -
                self.prev_vqs + self.rs * x_prev[1] - (2/self.delta_t) * phiqs)
        
        fx3 = ( self.rr * x[2] + ((self.llr + self.lm)*x[3] + self.lm*x[1])*x[4] + 
                (2/self.delta_t) * ((self.llr + self.lm)*x[2] + self.lm*x[0]) + self.rr*x_prev[2] + phiqr*x_prev[4] -
                (2/self.delta_t) * phidr)
        
        fx4 = ( self.rr * x[3] + ((self.llr + self.lm)*x[2] + self.lm*x[0])*x[4] +
                (2/self.delta_t) * ((self.llr + self.lm)*x[3] + self.lm*x[1]) + self.rr*x_prev[3] + phidr*x_prev[4] -
                (2/self.delta_t) * phiqr)
        
        fx5 = ( (3/2) * self.n_pole_pairs * self.lm * (x[2]*x[1] - x[3]*x[0]) - (self.d_fric + 2*self.j/self.delta_t)*x[4] +
                Te_ + (2*self.j/self.delta_t - self.d_fric)*x_prev[4] - 2*self.tm)
        
        #self.prev_vds = vds
        #self.prev_vqs = vqs
        
        return np.array([fx1,fx2,fx3,fx4,fx5])

    def init_J(self):
        j1 = [1,0,0,0,0]
        j2 = [0,1,0,0,0]
        j3 = [0,0,1,0,0]
        j4 = [0,0,0,1,0]
        j5 = [0,0,0,0,1]
        return np.vstack((j1,j2,j3,j4,j5))

    def J(self,x):
        # eqs 0 
        # variables x: [0]ids,[1]iqs,[2]idr,[3]iqr,[4]wr,[5]vds,[6]vqs
        j1 = [self.rs + (2/self.delta_t) * (self.lls + self.lm), 0, (2/self.delta_t)*self.lm, 0, 0]
        
        j2 = [0, self.rs + (2/self.delta_t) * (self.lls + self.lm), 0, (2/self.delta_t)*self.lm, 0]
        
        j3 = [(2/self.delta_t)*self.lm, self.lm*x[4], self.rr + (2/self.delta_t)*(self.llr + self.lm), (self.llr+self.lm)*x[4],
               ((self.llr+self.lm)*x[3]+self.lm*x[1])]
        
        j4 = [-self.lm*x[4], (2/self.delta_t)*self.lm, -(self.llr+self.lm)*x[4], self.rr+(2/self.delta_t)*(self.llr+self.lm),
              -((self.llr+self.lm)*x[2]+self.lm*x[0])]
        
        j5 = [(-3/2)*self.n_pole_pairs*self.lm*x[3], (3/2)*self.n_pole_pairs*self.lm*x[2], (3/2)*self.n_pole_pairs*self.lm*x[1],
              (-3/2)*self.n_pole_pairs*self.lm*x[0], -(self.d_fric + (2*self.j)/self.delta_t)]
        
        return np.vstack((j1,j2,j3,j4,j5))

    
    def newtonRaphson(self, x0,e,N):
        print('\n\n*** NEWTON RAPHSON METHOD IMPLEMENTATION ***')
        step = 1
        flag = 1
        condition = True
        x_prev = x0
        print("initial state", x0)
        x0 = x0 #+ 0.00001 * self.J(x_prev) @ x0
        while condition:
            
            if (self.timesteps >= 0):
                x1 = x0 - np.linalg.inv(self.J(x0)) @ self.F(x0,x_prev,self.voltage_inputs)
            else:
                x1 = x0 - np.linalg.inv(self.init_J()) @ self.F(x0,x_prev,self.voltage_inputs)
                
            print('Iteration:{}, x1 = {} and f(x1) = {}'.format(step,x1,self.F(x1,x_prev,self.voltage_inputs)))
            x0 = x1
            
            step = step + 1
            
            if step > N:
                flag = 0
                break
            
            condition = (abs(self.F(x1,x_prev,self.voltage_inputs)) > e).all()
        
        if flag==1:
            print('\nRequired root is:{}'.format(x1))
            print("did this function")
        else:
            print('\nNot Convergent.')
            
        return x1