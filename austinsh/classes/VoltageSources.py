import numpy as np
import math
from classes import Nodes
from classes import Resistors as r
from settings import settings

class VoltageSources:
    def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
        self.name = name
        self.vp_node = vp_node
        self.vn_node = vn_node
        self.amp_ph_ph_rms = amp_ph_ph_rms
        self.amp_voltage = self.amp_ph_ph_rms*(2**.5)/(3**.5)
        self.phase_deg = phase_deg
        self.phase_rad = self.phase_deg*np.pi/180
        self.frequency_hz = frequency_hz
        self.ang_frequency = 2*np.pi*self.frequency_hz
        park_angle = 0
        

    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.vp_node] 
        self.to_node_index = Nodes.node_index_dict[self.vn_node]
        # Returns a tuple
        return self.from_node_index, self.to_node_index
    
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, y_matrix, j_matrix, t, prev_volt):
        # Assigning indicies
        i,j = self.assign_node_indexes()
        # Creating temporary rows and columns to later increase the size of the Y matrix
        temp_column_y = np.zeros((len(y_matrix)))
        temp_row_y = np.zeros((len(y_matrix) + 1))
        # We do not need stamps for ground because it is a reference, so we just check
        # if one of the nodes are connected to ground or not
        if i != 0 and j != 0:
            temp_column_y[i] = 1
            temp_row_y[i] = 1
            temp_column_y[j] = -1
            temp_row_y[j] = -1
        elif i != 0:
            temp_column_y[i] = 1
            temp_row_y[i] = 1
        elif j != 0:
            temp_column_y[j] = -1
            temp_row_y[j] = -1
        # Increasing the size of the Y matrix with the new stamps
        y_matrix = np.column_stack((y_matrix, np.vstack(temp_column_y)))
        y_matrix = np.vstack((y_matrix, temp_row_y))
        # pre_volt is used as a initial point for previous time step values of the induction motor. Otherwise,
        # it has no use
        prev_volt = np.append(prev_volt, self.amp_voltage*math.sin((self.ang_frequency*(t - settings["Time Step"])) + self.phase_rad))
        # Adding the voltage source value to the J matrix
        j_matrix = np.append(j_matrix, self.amp_voltage*math.sin((self.ang_frequency*t) + self.phase_rad))
        return y_matrix, j_matrix, prev_volt

    def stamp_open(self,):
        pass