import sys
sys.path.append("..")
import numpy as np
from classes import Nodes

Y_matrix = np.zeros((5,5))

class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        self.g = 1/self.r
 
    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.from_node] 
        self.to_node_index = Nodes.node_index_dict[self.to_node]
        # Returns a tuple of 
        return self.from_node_index, self.to_node_index
    
    def stamp_sparse(self,):
        pass
    
    def stamp_dense(self, matrix):
        i,j = self.assign_node_indexes()
        if i == 0 or j == 0:
            if i == 0:
                i, j = j, i
            # i != 0, j == 0
            matrix[i,i] += self.g
        else:
            matrix[i,i] += self.g
            matrix[j,j] += self.g
            matrix[i,j] += -self.g
            matrix[j,i] += -self.g
        return matrix