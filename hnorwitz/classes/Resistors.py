
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
        self.from_index = -1
        self.to_index = -1

        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,val):#not sure if I implemented correctly
        for i in range(val):
            if Nodes.index[i].name == self.from_node: #not sure how to call specific node and and compare it
                self.from_index = Nodes.index[i]
            if Nodes.index[i].name == self.to_node:
                self.to_index = Nodes.index[i]
        #if from_node = node
        #from_index = node_index
        #if to_node = node
        #to_index = node_index
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_dim):
        Y_mtx= np.zeros((Y_dim,Y_dim))
        if self.to_node != 'gnd': 
            Y_mtx[self.from_index,self.from_index] = 1/self.r #Yii index
            Y_mtx[self.from_index,self.to_index] = -1/self.r #Yij index
            Y_mtx[self.to_index,self.from_index] = -1/self.r #Yji index
            Y_mtx[self.to_index,self.to_index] = 1/self.r #Yjj index
        else:
            Y_mtx[self.from_index,self.from_index] = 1/self.r #Yii index
            Y_mtx[self.from_index,self.to_index] = 0 #Yij index
            Y_mtx[self.to_index,self.from_index] = 0 #Yji index
            Y_mtx[self.to_index,self.to_index] = 0 #Yjj index

        return Y_mtx