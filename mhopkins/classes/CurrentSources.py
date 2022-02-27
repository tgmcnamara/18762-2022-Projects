import numpy as np
from itertools import count
from classes.Nodes import Nodes
from OpenGL.GL.AMD import name_gen_delete
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class CurrentSources:
    # default object represents an independent current source
    def __init__(self, name, ip_node, in_node, amps):
        self.name = name
        self.ip_node = ip_node
        self.in_node = in_node
        self.amps = amps
        self.ecm_type = ""
        self.ecm_val = 0

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
    
class DynamicCurrentSource(CurrentSources):
    def __init__(self, ip_node, in_node, controller, variable):
        self.name = name
        self.ip_node = ip_node
        self.in_node = in_node 
        self.amps = controller.variable
        self.ecm_type = ""
        self.ecm_val = 0
        
    def __str__(self):
        return "DI-{}-{}".format(self.amps, id(self))
    
    def __repr__(self):
        return self.__str__()