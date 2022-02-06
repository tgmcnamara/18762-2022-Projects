import numpy as np
from itertools import count
from classes.Nodes import Nodes
#from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse
#third
class Capacitors:
    def __init__(self, name, from_node, to_node, c):
        self.name = name
        self.c = c
        self.from_node = from_node
        self.to_node = to_node
        self.from_index = -1
        self.to_index = -1
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,val):
         for i in range(val):
            if Nodes.index[i].name == self.from_node: #not sure how to call specific node and and compare it
                self.from_index = Nodes.index[i]
            if Nodes.index[i].name == self.to_node:
                self.to_index = Nodes.index[i]
        #not sure If I should add to counter and insert a voltage source for a capacitor

        
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,Y_dim, d_t):#do we need to include delta t
        Y_mtx= np.zeros((Y_dim,Y_dim))
        if self.to_node != 'gnd': #may need an or here for self.from_node
            Y_mtx[self.from_index,self.from_index] = d_t/(2*self.c) #Yii index
            Y_mtx[self.from_index,self.to_index] = -d_t/(2*self.c) #Yij index
            Y_mtx[self.to_index,self.from_index] = -d_t/(2*self.c) #Yji index
            Y_mtx[self.to_index,self.to_index] = d_t/(2*self.c) #Yjj index
        else:
            Y_mtx[self.from_index,self.from_index] = d_t/(2*self.c) #Yii index
            Y_mtx[self.from_index,self.to_index] = 0 #Yij index
            Y_mtx[self.to_index,self.from_index] = 0 #Yji index
            Y_mtx[self.to_index,self.to_index] = 0 #Yjj index

        return Y_mtx
        #if to_node != gnd:
            #construct
            #[1/(deltat/2c), -1/(deltat/2c); -1/(deltat/2c), 1/(deltat/2c)]
            #[irow + icol=from_node, irow + jcol==to_node]
            #[jrow + icol=from_node, jrow + jcol==to_node]
        #else:
            #[1/(deltat/2c), 0; 0, 0]

        #pass

    def stamp_open(self,):#not sure what to do
        pass