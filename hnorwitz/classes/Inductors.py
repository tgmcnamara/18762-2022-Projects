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

    def stamp_dense(self,l, to_node, from_node):
         if to_node != gnd:
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
        else:
            #[1/(2/L*deltat), 0; 0, 0]
        pass

    def stamp_short(self,):#not sure what to do withi this
        #if it is a sort then the from_node and to_node have the same voltage
        #[1, 1; 1, 1]
        pass