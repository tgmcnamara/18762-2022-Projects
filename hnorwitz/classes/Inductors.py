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
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_dim, d_t):
         Y_mtx= np.zeros((Y_dim,Y_dim))
         if self.to_node != 'gnd': #may need an or here for self.from_node
            Y_mtx[self.from_index,self.from_index] = 2/(d_t*self.l) #Yii index
            Y_mtx[self.from_index,self.to_index] = -2/(d_t*self.l) #Yij index
            Y_mtx[self.to_index,self.from_index] = -2/(d_t*self.l) #Yji index
            Y_mtx[self.to_index,self.to_index] = 2/(d_t*self.l) #Yjj index
         else:
            Y_mtx[self.from_index,self.from_index] = 2/(d_t*self.l) #Yii index
            Y_mtx[self.from_index,self.to_index] = 0 #Yij index
            Y_mtx[self.to_index,self.from_index] = 0 #Yji index
            Y_mtx[self.to_index,self.to_index] = 0 #Yjj index

         return Y_mtx
         #if to_node != gnd:
            #construct
            #[1/(2/L*deltat), -1/(2/L*deltat); -1/(2/L*deltat), 1/(2/L*deltat)]
            #[irow + icol=from_node, irow + jcol==to_node]
            #[jrow + icol=from_node, jrow + jcol==to_node]
            
            #idea for implementation
            #if node == ii:
            #   node[from_node][from_node]=1/(2/L*deltat)
            #   node[from_node][to_node] = -1/(2/L*deltat)
            #   node[to_node][from_node] = -1/(2/L*deltat)
            #   node[to_node][to_node] = 1/(2/L*deltat)
        #else:
            #[1/(2/L*deltat), 0; 0, 0]
        #pass

    def stamp_short(self,):#not sure what to do withi this
        #if it is a sort then the from_node and to_node have the same voltage
        #[1, 1; 1, 1]
        pass