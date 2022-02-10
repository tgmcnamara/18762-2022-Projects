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
        self.l_comp_index = -1
        self.l_curr_index =-1
        #self.Vlp_index = -1
        #self.Vln_index = -1
        
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        self.from_index = Nodes.node_index_dict[self.from_node]
        self.to_index = Nodes.node_index_dict[self.to_node]
        Nodes.index_counter += 1
        self.comp_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.c_curr_index = Nodes.index_counter
        
    #####    
        #Nodes.index_counter += 1
        #self.comp_index = Nodes.index_counter
        #self.from_index = Nodes.node_index_dict[self.from_node]
        #self.to_index = self.comp_index

        #if self.to_node == 'gnd': #this accounts for the voltage source from the inductor model that 
            #self.Vlp_index = self.comp_index
        #else:
            #self.Vlp_index = self.comp_index
            #self.Vln_index = Nodes.node_index_dict[self.to_index]    

        #Nodes.index_counter += 1 #
        #self.l_curr_index = Nodes.index_counter
    ######
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_mtx, J_mtx, d_t, prev, time): 
        Y_mtx[self.from_index,self.from_index] += d_t/(2*self.l) #Yii index
        Y_mtx[self.from_index,self.comp_index] += -d_t/(2*self.l) #Yij index
        Y_mtx[self.comp_index,self.from_index] += -d_t/(2*self.l) #Yji index
        Y_mtx[self.comp_index,self.comp_index] += d_t/(2*self.l) #Yjj index
 ######       
        #if self.to_node == 'gnd': #only one groud index so need to make sure accounting for which end is connected to ground
        #    Y_mtx[self.l_curr_index, self.Vlp_index] += 1 #voltage (extra row) (should this be stamped into Jmatrix)
        #    Y_mtx[self.Vlp_index, self.l_curr_index] += -1 #current(extra columb)
        #    J_mtx[self.Vlp_index,0] += 0
        #    J_mtx[self.l_curr_index,0] += Vn + (d_t/(2*self.l))*In #(I think these come from Vinit)
            #how am I supposed to know how to accuratly sellect Vn and In, do the corrospond to Vcp and c_curr

        #else: #voltage source not connected to a ground (struggling to figure this out)
        #    Y_mtx[self.Vlp_index,self.Vlp_index] = 1 #Yii index
        #    Y_mtx[self.Vlp_index,self.Vlp_index] = -1 #Yij index
        #    Y_mtx[self.Vln_index,self.Vlp_index] = -1 #Yji index
        #    Y_mtx[self.Vln_index,self.Vln_index] = 1 #Yjj index
         

    def stamp_short(self,):#not sure what to do withi this
        #if it is a sort then the from_node and to_node have the same voltage
        #[1, 1; 1, 1]
        pass