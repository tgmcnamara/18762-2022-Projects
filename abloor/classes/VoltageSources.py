import numpy as np
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
        self.index = -1
        # You are welcome to / may be required to add additional class variables

    # Some suggested functions to implement,
    def assign_node_indexes(self, num):
        self.index = num
        return 1

    def stamp_sparse(self,):
        pass

    def stamp_dense(self, devices, Y_matrix):
        v = self.index
        nodes = devices['nodes']
        i = -1
        j = -1
        for node in nodes:
            if (node.name == self.vp_node):
                i = node.index
            if (node.name == self.vn_node):
                j = node.index
        if(i != -1):
            Y_matrix[v][i] += 1
            Y_matrix[i][v] += 1

        if(j != -1):
            Y_matrix[v][j] += -1
            Y_matrix[j][v] += -1


    def stamp_J(self, J_time, time):
        v = self.index
        J_time[v][0] = np.sqrt(2)*self.amp_ph_ph_rms*np.cos(np.pi*(self.frequency_hz*time + self.phase_deg)/180)

