
import numpy as np
from itertools import count
from classes.Nodes import Nodes
#from classes.Nodes import Nodes.node_index_dict
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        self.from_index = -1
        self.to_index = -1

        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,val):#not sure if I implemented correctly
        if self.to_node == 'gnd':
            self.from_index = Nodes.node_index_dict[self.from_node]
        else:
            self.from_index = Nodes.node_index_dict[self.from_node]
            self.to_index = Nodes.node_index_dict[self.to_node]
        return val
        
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_mtx, J_mtx):#(TESTING THIS METHODE
        if self.to_node == 'gnd':
            Y_mtx[self.from_index,self.from_index] += 1/self.r #Yii index
            pass
        else:
            Y_mtx[self.from_index,self.from_index] += 1/self.r #Yii index
            Y_mtx[self.from_index,self.to_index] += -1/self.r #Yij index
            Y_mtx[self.to_index,self.from_index] += -1/self.r #Yji index
            Y_mtx[self.to_index,self.to_index] += 1/self.r #Yjj index
            J_mtx[self.from_index,0] +=0
