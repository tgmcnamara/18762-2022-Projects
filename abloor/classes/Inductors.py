import sys
sys.path.append("..")
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l
        self.index = -1
        # You are welcome to / may be required to add additional class variables

    # Some suggested functions to implement,
    def assign_node_indexes(self,num):
    #create room for 2 eqs to account for VS current measuring
        self.index = num
        return 2

    def stamp_sparse(self,):
        pass

    def stamp_dense(self, devices, Y_matrix, step):
    #stamp invariant values into the Y_matrix
        c = self.index
        v = self.index + 1
        nodes = devices['nodes']
        i = -1
        j = -1
        g = step/(2*self.l)
        for node in nodes:
            if (node.name == self.from_node):
                i = node.index
            if (node.name == self.to_node):
                j = node.index

        Y_matrix[c][v] += 1
        Y_matrix[v][c] += 1

        if (i != -1):
            Y_matrix[i][i] += g

        if (j != -1):
            Y_matrix[j][j] += g
            Y_matrix[j][v] += -1
            Y_matrix[v][j] += -1

        if (i != -1) and (j != -1):
            Y_matrix[j][i] += -g
            Y_matrix[i][j] += -g


    def stamp_time(self, devices, V_init, J_time, step):
    #stamp time dependent values into the J vector
        c = self.index
        v = self.index + 1
        nodes = devices['nodes']
        i = -1
        j = -1
        g = step/(2*self.l)
        for node in nodes:
            if (node.name == self.from_node):
                i = node.index
            if (node.name == self.to_node):
                j = node.index

        if (i != -1):
            J_time[i] += -V_init[v] - g*V_init[i]
            J_time[c] += V_init[v] + g*V_init[i]
            #induc curr and measured v curr go in opp dir

        if (j != -1):
            J_time[c] += -g*V_init[j]

        if (i != -1) and (j != -1):
            J_time[i] += g*V_init[j]




