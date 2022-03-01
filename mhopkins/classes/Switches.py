import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse
import pickle

class Switches:
    def __init__(self, name, from_node, to_node, t_open, t_close):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.t_open = t_open
        self.t_close = t_close
        self.state = 0 #[0 is closed, 1 is open]
        
        # You are welcome to / may be required to add additional class variables   

    def update(self,t,t_prev):
        if (t > self.t_open and t_prev < self.t_open):
            self.state = 1
        elif ((t > self.t_close) and (t_prev < self.t_close)):
            self.state = 0
            
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
        return "Sw-{}-{}-{}".format(self.t_open, self.t_close, id(self))
    
    def __repr__(self):
        return self.__str__()