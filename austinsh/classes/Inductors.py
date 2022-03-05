import sys
import os
sys.path.append(os.path.abspath("."))
from settings import settings
import numpy as np
from classes import Nodes
from classes import Resistors as r

inductor_counter = 0

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l
        # The equivalent conductance for trapezoidal method
        self.g_equiv = settings["Time Step"]/(2*self.l)
        global inductor_counter
        inductor_counter += 1
        
    
    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.from_node] 
        self.to_node_index = Nodes.node_index_dict[self.to_node]
        # Returns a tuple
        return self.from_node_index, self.to_node_index
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, y_matrix, j_matrix, vectors, t):
        i, j = self.assign_node_indexes()
        temp_column = np.zeros((len(y_matrix)))
        temp_row = np.zeros((len(y_matrix) + 1))
        if i != 0 and j != 0:
            temp_column[i] = 1
            temp_row[i] = self.g_equiv
            temp_column[j] = -1
            temp_row[j] = -self.g_equiv
        elif i != 0:
            temp_column[i] = 1
            temp_row[i] = self.g_equiv
        elif j != 0:
            temp_column[j] = -1
            temp_row[j] = -self.g_equiv
        temp_row[len(y_matrix)] = -1
        y_matrix = np.column_stack((y_matrix, np.vstack(temp_column)))
        y_matrix = np.vstack((y_matrix, temp_row))
        # Creating the initial conditions
        if t == 0:
            j_matrix = np.append(j_matrix, 0)
            if i != 0 and j != 0:
                y_matrix[len(y_matrix) - 1][i] = 1/.000000001
                y_matrix[len(y_matrix) - 1][j] = -1/.000000001
            elif i != 0:
                 y_matrix[len(y_matrix) - 1][i] = 1/.000000001
            elif j != 0:
                y_matrix[len(y_matrix) - 1][j] = -1/.000000001
        else:
            index = int(t/settings["Time Step"]) -1
            if j != 0 and i != 0:
                j_v_stamp = self.g_equiv*(vectors[index][i-1]-vectors[index][j-1])
            elif i != 0:
                j_v_stamp = self.g_equiv*(vectors[index][i-1])
            elif j != 0:
                j_v_stamp = self.g_equiv*(-vectors[index][j-1])
            j_curr_stamp = vectors[index][len(y_matrix) - 2]
            j_matrix = np.append(j_matrix, -(j_v_stamp + j_curr_stamp))
        return y_matrix, j_matrix