import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class CurrentSources:
    # default object represents an independent current source
    def __init__(self, name, ip_node, in_node, amps):
        self.name = name
        self.ip_node = ip_node
        self.in_node = in_node
        self.amps = amps

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,):
        pass

    def stamp_open(self,):
        pass
       
    def __str__(self): 
        return "I-{}-{}".format(self.amps, id(self))
    
    def __repr__(self):
        return self.__str__()