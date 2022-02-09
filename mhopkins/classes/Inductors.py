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
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, freq=None):
        if (freq == None):
            return self.stamp_short()
        else:
            return complex(freq*self.l)

    # DC scenario
    def stamp_short(self):
        return 0
    
    def __str__(self):
        return "L-{}-{}".format(self.l, id(self))
    
    def __repr__(self):
        return self.__str__()