
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse


class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        # You are welcome to / may be required to add additional class variables

    # Some suggested functions to implement,
    def assign_node_indexes(self,):
        pass

    def stamp_sparse(self,):
        pass

    def stamp_dense(self, devices, Y_matrix):
    #put appropriate stamp into the Y_matrix
        nodes = devices['nodes']
        i = -1
        j = -1
        for node in nodes:
            if (node.name == self.from_node):
                i = node.index
            if (node.name == self.to_node):
                j = node.index
        if(i != -1):
            Y_matrix[i][i] += 1/(self.r)
        if(j != -1):
            Y_matrix[j][j] += 1/(self.r)
        if(j != -1) and (i != -1):
            Y_matrix[i][j] += -1/(self.r)
            Y_matrix[j][i] += -1/(self.r)

