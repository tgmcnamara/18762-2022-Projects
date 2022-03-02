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
        self.index = -1
        # You are welcome to / may be required to add additional class variables

    # Some suggested functions to implement,
    def assign_node_indexes(self, num):
        self.index = num
        return 8

    def stamp_dq(self, devices, Y_matrix):
        ids = self.index
        iqs = self.index + 1
        ias = self.index + 5
        ibs = self.index + 6
        ics = self.index + 7

        Y_matrix[ias][ias] += 0.5*2/3
        Y_matrix[ias][ibs] += 0.5*2/3
        Y_matrix[ias][ics] += 0.5

        Y_matrix[ibs][ias] += 1*2/3 #cos(theta) = cos(0)
        Y_matrix[ibs][ibs] += np.cos(-np.pi*2/3)*2/3
        Y_matrix[ibs][ics] += np.cos(np.pi*2/3)*2/3
        Y_matrix[ibs][ids] += -1

        Y_matrix[ics][ias] += 0
        Y_matrix[ics][ibs] += np.sin(-np.pi*2/3)*2/3
        Y_matrix[ics][ics] += np.sin(np.pi*2/3)*2/3
        Y_matrix[ics][iqs] += -1

        nodes = devices['nodes']
        a = -1
        b = -1
        c = -1
        for node in nodes:
            if (node.name == self.phase_a_node):
                a = node.index
            if (node.name == self.phase_b_node):
                b = node.index
            if (node.name == self.phase_c_node):
                c = node.index
        if (a != -1):
            Y_matrix[a][ias] += -1
            Y_matrix[ids][a] += -1
        if (b != -1):
            Y_matrix[b][ibs] += -1
            Y_matrix[ids][b] += -2*np.cos(-2*np.pi/3)/3
            Y_matrix[iqs][b] += -2*np.sin(-2*np.pi/3)/3
        if (c != -1):
            Y_matrix[c][ics] += -1
            Y_matrix[ids][c] += -2*np.cos(2*np.pi/3)/3
            Y_matrix[iqs][c] += -2*np.sin(2*np.pi/3)/3



    def stamp_dense(self, devices, Y_matrix, J_vector, V_prev, step):
        ids = self.index
        iqs = ids + 1
        idr = iqs + 1
        iqr = idr + 1
        wr = iqr + 1
        dt = step

        Y_matrix[ids][ids] += self.rs + 2*(self.lss)/dt
        Y_matrix[ids][idr] += 2*self.lm/dt

        Y_matrix[iqs][iqs] += self.rs + 2*(self.lss)/dt
        Y_matrix[iqs][iqr] += 2*self.lm/dt

        Y_matrix[idr][ids] += 2*self.lm/dt
        Y_matrix[idr][iqs] += self.lm*V_prev[wr]
        Y_matrix[idr][idr] += self.rr + 2*(self.lrr)/dt
        Y_matrix[idr][iqr] += self.lrr*V_prev[wr]
        Y_matrix[idr][wr] += self.lrr*V_prev[iqr] + self.lm*V_prev[iqs]

        Y_matrix[iqr][ids] += -self.lm*V_prev[wr]
        Y_matrix[iqr][iqs] += 2*self.lm/dt
        Y_matrix[iqr][idr] += -self.lrr*V_prev[wr]
        Y_matrix[iqr][iqr] += self.rr + 2*(self.lrr)/dt
        Y_matrix[iqr][wr] += -(self.lrr*V_prev[idr] + self.lm*V_prev[ids])

        A = 3*self.n_pole_pairs*self.lm/2
        Y_matrix[wr][ids] += -A*V_prev[iqr]
        Y_matrix[wr][iqs] += A*V_prev[idr]
        Y_matrix[wr][idr] += A*V_prev[iqs]
        Y_matrix[wr][iqr] += -A*V_prev[ids]
        Y_matrix[wr][wr] += -(self.d_fric + 2*self.j/dt)

        #For J vector, I believe delta_matrix*v_prev - f should cancel out all prev it terms

    def stamp_time(self, devices, V_prev, J_vector, step):
        dt = step
        ids = self.index
        iqs = self.index + 1
        idr = self.index + 2
        iqr = self.index + 3
        wr = self.index + 4
        A = 3*self.n_pole_pairs*self.lm/2

        an = -1
        b = -1
        c = -1
        nodes = devices['nodes']
        for node in nodes:
            if (node.name == self.phase_a_node):
                an = node.index
            if (node.name == self.phase_b_node):
                b = node.index
            if (node.name == self.phase_c_node):
                c = node.index
        if(an != -1) and (b != -1) and (c != -1):
            vds = 2*(1*an + np.cos(-2*np.pi/3)*b + np.cos(2*np.pi/3)*c)/3
            vqs = 2*(np.sin(-2*np.pi/3)*b + np.sin(2*np.pi/3)*c)/3
            J_vector[ids] -= -vds
            J_vector[iqs] -= -vqs

        #should all be subtracted for -f
        #d/dt terms should have opposite sign convention from derivatives
        #since df/dt -> f(t+dt) - f(t)

        J_vector[ids] -= (self.rs - 2*(self.lss)/dt)*V_prev[ids]#lss term sign change
        J_vector[ids] -= -(2*self.lm/dt)*V_prev[idr]#sc

        J_vector[iqs] -= (self.rs - 2*(self.lss)/dt)*V_prev[iqs]#lss sc
        J_vector[iqs] -= -(2*self.lm/dt)*V_prev[iqr]#sc

        J_vector[idr] -= -(2*self.lm/dt)*V_prev[ids]#sc
        J_vector[idr] -= self.lm*V_prev[wr]*V_prev[iqs]
        J_vector[idr] -= (self.rr - 2*(self.lrr)/dt)*V_prev[idr]#lrr sc
        J_vector[idr] -= self.lrr*V_prev[wr]*V_prev[iqr]
        J_vector[idr] -= (self.lrr*V_prev[iqr] + self.lm*V_prev[iqs])*V_prev[wr]

        J_vector[iqr] -= -self.lm*V_prev[wr]*V_prev[ids]
        J_vector[iqr] -= -(2*self.lm/dt)*V_prev[iqs]#sc
        J_vector[iqr] -= -self.lrr*V_prev[wr]*V_prev[idr]
        J_vector[iqr] -= (self.rr - 2*(self.lrr)/dt)*V_prev[iqr]#lrr sc
        J_vector[iqr] -= -(self.lrr*V_prev[idr] + self.lm*V_prev[ids])*V_prev[wr]

        J_vector[wr] -= -A*V_prev[iqr]*V_prev[ids]
        J_vector[wr] -= A*V_prev[idr]*V_prev[iqs]
        J_vector[wr] -= A*V_prev[iqs]*V_prev[idr]
        J_vector[wr] -= -A*V_prev[ids]*V_prev[iqr]
        J_vector[wr] -= -(self.d_fric - 2*self.j/dt)*V_prev[wr]#jterm sc

