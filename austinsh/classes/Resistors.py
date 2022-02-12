
import numpy as np
from itertools import count

from sklearn.metrics import r2_score
from sympy import Ray3D
import Nodes
from lib.assign_node_indexes import assign_node_indexes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse
Y_matrix = np.zeros((4,4))
Stamp_Matrix = np.zero((4,4))

class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        # Assigning the from node index value to the resistor
        self.from_node_index = Nodes.node_index_dict[self.from_node] 
        self.to_node_index = Nodes.node_index_dict[self.to_node]
        # Returns a tuple of 
        return self.from_node_index, self.to_node_index
    
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        for index in range(len(Nodes.node_index_dict)):
            Y_matrix[Resistors.assign_node_indexes(self.stamp_dense)[0]][Resistors.assign_node_indexes(self.stamp)[1]] += -1/(Resistors.self.r)
            Y_matrix[Resistors.assign_node_indexes(self)[0]][Resistors.assign_node_indexes(self)[1]] += 1/self.r

r1 = Resistors("r1", "1a", "2a", .1)
r2 = Resistors("r1", "2a", "3a", .1)
r3 = Resistors("r1", "3a", "4a", .1)
r4 = Resistors("r1", "4a", "1a", .1)

print(Resistors.assign_node_indexes(r1))
print(Resistors.assign_node_indexes(r2)[0])
print(Resistors.stamp_dense(Y_matrix))