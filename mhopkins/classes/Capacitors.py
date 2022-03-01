import numpy as np
from itertools import count
from classes.Nodes import Nodes
#from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Capacitors:
    def __init__(self, name, from_node, to_node, c):
        self.name = name
        self.c = c
        self.from_node = from_node
        self.to_node = to_node
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, freq=None):
        if (freq == None):
            return self.stamp_open()
        else:
            return complex(1/(freq * self.c))

    # DC scenario
    def stamp_open(self):
        return np.inf
    
    
    def __str__(self):
        return "C-{}-{}".format(self.c, id(self))
    
    def __repr__(self):
        return self.__str__()