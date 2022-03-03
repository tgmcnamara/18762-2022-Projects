import numpy as np
import math
from itertools import count
from classes import Nodes
from classes import Resistors as r
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class VoltageSources:
    def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
        self.name = name
        self.vp_node = vp_node
        self.vn_node = vn_node
        self.amp_ph_ph_rms = amp_ph_ph_rms
        self.amp_voltage = self.amp_ph_ph_rms*(2**.5)/(3**.5)
        self.phase_deg = phase_deg
        self.frequency_hz = frequency_hz
        self.ang_frequency = 2*np.pi*self.frequency_hz

    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.vp_node] 
        self.to_node_index = Nodes.node_index_dict[self.vn_node]
        # Returns a tuple
        return self.from_node_index, self.to_node_index
    
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, y_matrix, j_matrix, t):
        i,j = self.assign_node_indexes()
        temp_column_y = np.zeros((len(y_matrix)))
        temp_row_y = np.zeros((len(y_matrix) + 1))
        if i != 0:
            temp_column_y[i] = 1
            temp_row_y[i] = 1
        elif j != 0:
            temp_column_y[j] = -1
            temp_row_y[j] = -1
        y_matrix = np.column_stack((y_matrix, np.vstack(temp_column_y)))
        y_matrix = np.vstack((y_matrix, temp_row_y))
        j_matrix = np.append(j_matrix, self.amp_voltage*math.sin((self.ang_frequency*t) - self.phase_deg))
        return y_matrix, j_matrix

    def stamp_open(self,):
        pass
        
# voltage_3 = VoltageSources("N", "1a", "3a", 1, 0, 0)

# print(VoltageSources.assign_node_indexes(voltage_3))

# Y_y_matrix = voltage_3.stamp_dense(r.Y_y_matrix)
# print(Y_y_matrix)